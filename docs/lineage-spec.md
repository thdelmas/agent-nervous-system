# Lineage & Registry Spec (v0.1)

Two machine-readable files let a **second agent** observe this suite's evolution and act on it — discover skills, trace their lineage, and decide whether to copy a mutation — **without the maintainer in the loop**. That last clause is the whole point: until an unprompted script can consume these files and pull a skill, the "agents evolve" thesis is narration. These files are the mechanism that makes it testable.

## Why these files exist (the model)

Improvement here spreads by **memetic transmission**, not Darwinian evolution: variation is *willed* and *fitness-biased* (people try to make good skills; copying errors don't), and it's inherited **horizontally by imitation**, not vertically by reproduction. That's Lamarckian.

But at population scale — thousands of builders choosing in unrelated contexts — individual determinism washes into an aggregate that is **stochastic, not random**. The difference is load-bearing:

- *Random* (Darwin's mutations) = undirected with respect to fitness.
- *Stochastic-but-biased* (this system) = high-variance noise riding on a **persistent gradient** (shared pressures: cost, attention, platform-compat). Noise + drift = a directed walk.

You cannot predict any single adopt/reject decision. You **can** measure the distribution and the gradient under it. That is what `lineage.jsonl` captures — and why the `context` field matters most: apparent randomness is usually determinism in hidden variables (like weather). `context` records the situational frame that, once known, dissolves the noise back into signal.

## `registry.json` — the population snapshot

A single object. A peer fetches it to discover what skills exist *now*.

| Field | Type | Meaning |
| --- | --- | --- |
| `registry_version` | semver | Schema version of this file. |
| `selector_model` | string | `memetic` — how variation propagates (see above). |
| `skills[]` | array | One entry per live skill. |

Each `skills[]` entry:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable skill identifier (the replicator's name). |
| `version` | semver | Current version. Bump on any behavior change. |
| `organ` | string | Functional role (perception / memory / defense / grief / …). |
| `repo` | string | `owner/name` of the skill's own repo. |
| `spec_url` | url | Raw URL of the skill's `SKILL.md` — what a copier actually pulls. |
| `parent` | string \| null | `id` of the single skill this one descended from. `null` = root of a lineage. This pointer *is* the family tree — exactly one descent edge per skill. |
| `relation` | enum | The *type* of the `parent` edge: `originates` (root; required iff `parent` is null), `inverts`, `extends`, or `complements`. Stops the descent edge from silently conflating three different derivations. |
| `mutation` | string | One line: what's novel versus the parent. |
| `relations` | array | **Optional.** The functional web — secondary, *non-descent* edges as `{id, type}` (`type` from the same enum, typically `scheduled-by` / `complements`). Lets an organ record a real second link (e.g. playtime `inverts` rem-sleep by descent **and** is `scheduled-by` consciousness-loop) without forging a second parent. A consumer that only wants descent ignores this field entirely. |
| `fitness_signal` | string | The measurable outcome this skill should be judged by — **realized cost/benefit, not stars.** |

### Descent vs. the functional web (why two fields, not a DAG)

`parent`/`relation` is the **descent spine**: one privileged edge answering "what did this copy from," kept singular because the memetic-evolution thesis is a falsifiable claim about *inheritance* — a consumer must build the provenance tree in one pass without adjudicating which of several edges counts. `relations[]` is the **functional topology**: a many-to-many web of how organs interact at runtime (the executive polls all seven each tick → `scheduled-by`; the loop is the wake-phase to rem-sleep's sleep-phase → `complements`). They answer different questions — *what did this inherit* vs *what does this interact with* — so they are different fields. Collapsing both into a multi-parent `derives_from[]` was rejected: it dissolves the single-descent claim the whole layer exists to test. The validator enforces the split — `relation` matches root-ness, and no `relations[]` edge may dangle, self-loop, or merely restate the descent edge.

## `lineage.jsonl` — the selection ledger

Append-only. **One JSON object per line**, one line per adopt/reject/watch/cold decision. Never edit past rows; corrections are new rows. The *rejections* are as valuable as the adoptions — they're the negative dataset of what didn't survive selection here, and why.

| Field | Type | Meaning |
| --- | --- | --- |
| `date` | `YYYY-MM-DD` | When the decision was made. |
| `selector` | string | Who/what made the call (the selection happens here, not in the "genome"). |
| `peer_repo` | string | The observed peer (`owner/name` or org). |
| `peer_artifact` | string | What was observed: `repo` / `spec` / `profile` / `org` / `concept` (a body of prior-art/literature, not a single repo) / `skill` (an existing skill, peer or internal) / `experiment` (an internal probe/sim). |
| `skill_id` | string | Which suite skill it bears on; `_suite` for suite-wide. Must resolve to a `registry.json` `id` or `_suite`. |
| `verdict` | enum | `adopted` \| `rejected` \| `forked` \| `watch` \| `cold` \| `refined`. |
| `reason` | string | Why — the rationale. |
| `context` | string | The situational frame of the choice. **This is the field that makes a locally-deterministic choice legible** — the signal under the apparent noise. |

### Verdict semantics

- `adopted` — the trait (idea/design/compat target) was copied into the suite's thinking.
- `forked` — taken but modified; expect a new `registry` entry with this peer as conceptual `parent`. For an **internal** fork (one suite organ derived from another) the `peer_repo` must encode the descent: `_self/<parent-id>` matching the new skill's registry `parent`, or `_self/_suite` when the new skill is a registry root (originated at suite genesis, no parent). A `forked` row whose `peer_repo` points at the skill's *own* repo carries zero genealogy and is rejected by the validator.
- `rejected` — deliberately *not* copied. Records why a mutation didn't propagate **here** (often category mismatch, not low quality).
- `watch` — promising; revisit next observation round.
- `cold` — dead end (off-theme, name-collision, irrelevant).
- `refined` — an **in-place improvement to an existing suite skill** (internal self-improvement), distinct from `forked` (which spawns a *new* skill). The selection event is the suite acting on itself, not on an external peer.

### Genealogy & internal-origin rows

Two clarifications the consumption protocol depends on:

- **`registry.json` is the authoritative family tree.** The `parent` pointers there are the genealogy; build the provenance graph from them. A `lineage.jsonl` `forked` row records the *selection event* (a new skill was taken-and-modified) — look up its parent in the registry by `skill_id`, don't expect a `parent` edge on the row.
- **Every non-root skill must carry its evidence.** The registry `parent` edge is the "agents evolve" claim; a claim with no ledger row behind it is assertion, not record. So each non-root skill needs at least one `forked` **origination row** (`skill_id` = the skill, `peer_repo` = `_self/<parent>` per above). Roots originate at genesis, so an origination row is optional for them — but if present it uses `_self/_suite`. The validator fails on a missing origination row or a fork source that doesn't match the registry parent.
- **Internal-origin rows** use a `_self/<name>` `peer_repo` (e.g. `_self/rem-sleep`, `_self/playtime-sim`, `_self/_suite`) and `peer_artifact` of `spec` / `skill` / `experiment` / `concept`. These are the suite observing *itself* — origination forks and the rows `proprioception` (the feedback organ) emits. They are first-class ledger entries, not external peer verdicts.

## The consumption protocol (the falsifiable test)

A second agent should be able to, unprompted:

1. `GET registry.json` → list skills, versions, `spec_url`s.
2. `GET lineage.jsonl` → stream decisions; build the provenance graph from `parent` pointers and `forked`/`adopted` rows.
3. Score candidates by `fitness_signal` (realized outcome), not popularity.
4. Decide: pull a skill's `spec_url`, or record its own `rejected` row with `context`.

**If no script can do steps 1–4 today, the evolution story is narration.** When one does — when a peer copies a mutation from here without the maintainer involved — selection has moved from the human to the population, and the thesis is live.

## Adversarial note

A public selection ledger is gameable: fake rejections, poisoned lineage, sybil fitness, strategic non-disclosure as a moat. Treat ingested lineage from untrusted selectors as **claims, not facts** — weight by selector reputation, and prefer `fitness_signal`s you can independently reproduce. The interesting selection pressure at scale is deception-resistance, not raw capability.
