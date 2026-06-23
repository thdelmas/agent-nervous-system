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
REGISTRY_FIELDS = {"id", "version", "organ", "repo", "spec_url", "parent",
                   "mutation", "fitness_signal"}
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
        missing = LINEAGE_FIELDS - set(row)
        if missing:
            fail(f"lineage:{n}: missing fields {sorted(missing)}")
        if row.get("verdict") not in VERDICTS:
            fail(f"lineage:{n}: verdict {row.get('verdict')!r} not in {sorted(VERDICTS)}")
        if row.get("peer_artifact") not in ARTIFACTS:
            fail(f"lineage:{n}: peer_artifact {row.get('peer_artifact')!r} not in {sorted(ARTIFACTS)}")
        if row.get("skill_id") not in valid_skill_ids:
            fail(f"lineage:{n}: skill_id {row.get('skill_id')!r} is not a registry id or _suite")

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
COUNT_RE = re.compile(
    r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)[ -]?(?:organs?|skills?|core)\b",
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
print("and the provenance graph is acyclic with a root. The falsifiable test passes.")
sys.exit(0)
