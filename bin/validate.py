#!/usr/bin/env python3
"""Validate the agent-nervous-system machine-readable layer against docs/lineage-spec.md.

This is the spec's "falsifiable test" made executable: it does what an unprompted
peer agent would do — parse registry.json + lineage.jsonl, build the provenance
graph, and check the ledger is schema-valid and referentially sound. Exit 0 means
a consumer could actually use these files; exit 1 means it would choke. stdlib only.

    python3 bin/validate.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "registry.json")
LINEAGE = os.path.join(ROOT, "lineage.jsonl")

# Schemas — keep in lockstep with docs/lineage-spec.md.
VERDICTS = {"adopted", "rejected", "forked", "watch", "cold", "refined"}
ARTIFACTS = {"repo", "spec", "profile", "org", "concept", "skill", "experiment"}
# The single source of truth for the relation vocabulary. registry.json carries only
# the string values; this set is the only place the enum is declared, so the two
# can't drift (the failure mode logged earlier for the count-regex/dict pair).
# `originates` is reserved for the descent edge of a root (parent == null); the rest
# type a real edge — either the descent edge (`relation`) or a functional web edge.
RELATION_TYPES = {"originates", "inverts", "extends", "complements", "scheduled-by"}
REGISTRY_FIELDS = {"id", "version", "organ", "repo", "spec_url", "parent",
                   "relation", "mutation", "fitness_signal"}
LINEAGE_FIELDS = {"date", "selector", "peer_repo", "peer_artifact", "skill_id",
                  "verdict", "reason", "context"}

errors = []


def fail(msg):
    errors.append(msg)


# --- registry.json: the population snapshot + authoritative family tree ---
with open(REGISTRY) as f:
    reg = json.load(f)
skills = reg.get("skills", [])
ids = [s.get("id") for s in skills]
idset = set(ids)
for dup in {i for i in ids if ids.count(i) > 1}:
    fail(f"registry: duplicate skill id {dup!r}")
for s in skills:
    sid = s.get("id", "?")
    missing = REGISTRY_FIELDS - set(s)
    if missing:
        fail(f"registry: skill {sid!r} missing fields {sorted(missing)}")
    parent = s.get("parent")
    if parent is not None and parent not in idset:
        fail(f"registry: skill {sid!r} parent {parent!r} is not a registry id")

    # The `relation` types the single descent edge; `parent==null` iff `originates`.
    rel = s.get("relation")
    if rel not in RELATION_TYPES:
        fail(f"registry: skill {sid!r} relation {rel!r} not in {sorted(RELATION_TYPES)}")
    elif (parent is None) != (rel == "originates"):
        fail(f"registry: skill {sid!r} relation/parent mismatch — a root (parent=null) "
             f"must use 'originates' and only a root may (got parent={parent!r}, relation={rel!r})")

    # `relations[]` is the optional functional web — secondary, non-descent edges.
    # It must never silently restate the descent edge or dangle.
    web = s.get("relations", [])
    if not isinstance(web, list):
        fail(f"registry: skill {sid!r} relations must be a list")
        web = []
    for e in web:
        eid, etype = e.get("id"), e.get("type")
        if eid not in idset:
            fail(f"registry: skill {sid!r} relations edge id {eid!r} is not a registry id")
        if etype not in RELATION_TYPES:
            fail(f"registry: skill {sid!r} relations edge type {etype!r} not in {sorted(RELATION_TYPES)}")
        if eid == sid:
            fail(f"registry: skill {sid!r} relations edge points at itself")
        if eid == parent and etype == rel:
            fail(f"registry: skill {sid!r} relations edge {eid!r}/{etype!r} just restates the "
                 f"descent edge — the web is for *secondary* relations, not a copy of `parent`")

# Build the provenance graph from registry parent pointers; require acyclic + a root.
parent_of = {s.get("id"): s.get("parent") for s in skills}


def walk_to_root(node):
    seen = set()
    while node is not None:
        if node in seen:
            return None  # cycle
        seen.add(node)
        node = parent_of.get(node)
    return seen


for sid in idset:
    if walk_to_root(sid) is None:
        fail(f"registry: parent cycle reachable from {sid!r}")
roots = [i for i in idset if parent_of.get(i) is None]
if not roots:
    fail("registry: no root skill (every skill has a parent) — the graph has no origin")

# --- lineage.jsonl: the append-only selection ledger ---
valid_skill_ids = idset | {"_suite"}
rows = 0
ledger = []  # retained for cross-row genealogy checks below
with open(LINEAGE) as f:
    for n, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        rows += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            fail(f"lineage:{n}: invalid JSON ({e})")
            continue
        ledger.append(row)
        missing = LINEAGE_FIELDS - set(row)
        if missing:
            fail(f"lineage:{n}: missing fields {sorted(missing)}")
        if row.get("verdict") not in VERDICTS:
            fail(f"lineage:{n}: verdict {row.get('verdict')!r} not in {sorted(VERDICTS)}")
        if row.get("peer_artifact") not in ARTIFACTS:
            fail(f"lineage:{n}: peer_artifact {row.get('peer_artifact')!r} not in {sorted(ARTIFACTS)}")
        if row.get("skill_id") not in valid_skill_ids:
            fail(f"lineage:{n}: skill_id {row.get('skill_id')!r} is not a registry id or _suite")

# --- genealogical coherence: the registry parent-tree must be ledger-evidenced ---
# Schema + referential checks above can pass while the family tree is pure assertion:
# a `forked` row can point peer_repo at the skill's OWN repo (fork-from-self, zero
# descent), or a skill can have a registry parent with no origination row at all.
# Both happened (3 self-pointers; rem-sleep/immune-check/sunset had no fork row,
# sunset none at all) and the old validator passed them green. The `parent` edge IS
# the "agents evolve" claim, so make it falsifiable: every non-root skill needs a
# `forked` origination row, and every internal `forked` row's source must match the
# registry parent. Convention: peer_repo == "_self/<parent>", or "_self/_suite" for
# a root (originated at suite genesis, no external parent).
forks_by_skill = {}
for row in ledger:
    if row.get("verdict") != "forked":
        continue
    sid = row.get("skill_id")
    if sid not in idset:  # _suite forks aren't organ originations
        continue
    forks_by_skill.setdefault(sid, []).append(row)
    parent = parent_of.get(sid)
    expected = f"_self/{parent}" if parent else "_self/_suite"
    got = row.get("peer_repo")
    if got != expected:
        kind = "root (no parent)" if parent is None else f"parent {parent!r}"
        fail(f"lineage: forked row for {sid!r} has peer_repo {got!r} but registry "
             f"says {kind} — expected {expected!r} (fork source must encode descent)")
for sid in idset:
    if parent_of.get(sid) is None:
        continue  # roots originate; an origination row is optional for them
    if sid not in forks_by_skill:
        fail(f"lineage: skill {sid!r} (registry parent {parent_of[sid]!r}) has no "
             f"`forked` origination row — its parentage is asserted, not ledger-evidenced")

# --- prose count-drift: hardcoded "N organs/skills" claims must track the registry ---
# Recurring failure mode (install.sh once stale at 4; README de-staled by hand): prose
# enumerations drift from the population while the schema stays valid, so the old
# validator passed a lying doc. Source of truth = len(skills). Two legitimate framings:
# N (the whole nervous system) and N-1 (the organs the executive polls, excluding
# consciousness-loop itself). Anything else is drift. Parameterized on N so it
# self-adjusts when the Nth organ lands — no new magic number to forget.
N = len(skills)
WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
           "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
# Derive the spelled-number alternation from WORDNUM so the two can't drift apart
# (a divergence would silently miss or KeyError below — found via playtime fuzzing).
COUNT_RE = re.compile(
    r"\b(" + "|".join([r"\d+"] + list(WORDNUM)) + r")[ -]?(?:organs?|skills?|core)\b",
    re.I)
DECL_RE = re.compile(r"nervous system is (\d+)", re.I)
PROSE_FILES = ["README.md", "install.sh",
               "consciousness-loop/SKILL.md", "proprioception/SKILL.md"]
for rel in PROSE_FILES:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        continue
    with open(path) as f:
        for n, line in enumerate(f, 1):
            for m in COUNT_RE.finditer(line):
                tok = m.group(1).lower()
                val = int(tok) if tok.isdigit() else WORDNUM[tok]
                if val not in (N, N - 1):
                    fail(f"{rel}:{n}: organ-count {val} not in {{{N - 1}, {N}}} "
                         f"— prose drifted from registry ({N} skills)")
            for m in DECL_RE.finditer(line):
                if int(m.group(1)) != N:
                    fail(f"{rel}:{n}: 'nervous system is {m.group(1)}' "
                         f"but registry has {N} skills")

# --- report ---
print(f"registry: {len(skills)} skills, {len(roots)} root(s): {', '.join(sorted(roots))}")
print(f"lineage:  {rows} ledger rows")
if errors:
    print(f"\nFAIL — {len(errors)} defect(s) a consumer would choke on:")
    for e in errors:
        print(f"  x {e}")
    sys.exit(1)
print("\nOK — registry + lineage parse, are schema-valid and referentially sound,")
print("the provenance graph is acyclic with a root, and every parent edge is")
print("ledger-evidenced by a coherent origination row. The falsifiable test passes.")
sys.exit(0)
