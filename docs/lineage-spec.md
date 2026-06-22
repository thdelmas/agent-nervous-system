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
| `parent` | string \| null | `id` of the skill this one mutated from. `null` = root of a lineage. This pointer *is* the family tree. |
| `mutation` | string | One line: what's novel versus the parent. |
| `fitness_signal` | string | The measurable outcome this skill should be judged by — **realized cost/benefit, not stars.** |

## `lineage.jsonl` — the selection ledger

Append-only. **One JSON object per line**, one line per adopt/reject/watch/cold decision. Never edit past rows; corrections are new rows. The *rejections* are as valuable as the adoptions — they're the negative dataset of what didn't survive selection here, and why.

| Field | Type | Meaning |
| --- | --- | --- |
| `date` | `YYYY-MM-DD` | When the decision was made. |
| `selector` | string | Who/what made the call (the selection happens here, not in the "genome"). |
| `peer_repo` | string | The observed peer (`owner/name` or org). |
| `peer_artifact` | string | What was observed: `repo` / `spec` / `profile` / `org`. |
| `skill_id` | string | Which suite skill it bears on; `_suite` for suite-wide. |
| `verdict` | enum | `adopted` \| `rejected` \| `forked` \| `watch` \| `cold`. |
| `reason` | string | Why — the rationale. |
| `context` | string | The situational frame of the choice. **This is the field that makes a locally-deterministic choice legible** — the signal under the apparent noise. |

### Verdict semantics

- `adopted` — the trait (idea/design/compat target) was copied into the suite's thinking.
- `forked` — taken but modified; expect a new `registry` entry with this peer as conceptual `parent`.
- `rejected` — deliberately *not* copied. Records why a mutation didn't propagate **here** (often category mismatch, not low quality).
- `watch` — promising; revisit next observation round.
- `cold` — dead end (off-theme, name-collision, irrelevant).

## The consumption protocol (the falsifiable test)

A second agent should be able to, unprompted:

1. `GET registry.json` → list skills, versions, `spec_url`s.
2. `GET lineage.jsonl` → stream decisions; build the provenance graph from `parent` pointers and `forked`/`adopted` rows.
3. Score candidates by `fitness_signal` (realized outcome), not popularity.
4. Decide: pull a skill's `spec_url`, or record its own `rejected` row with `context`.

**If no script can do steps 1–4 today, the evolution story is narration.** When one does — when a peer copies a mutation from here without the maintainer involved — selection has moved from the human to the population, and the thesis is live.

## Adversarial note

A public selection ledger is gameable: fake rejections, poisoned lineage, sybil fitness, strategic non-disclosure as a moat. Treat ingested lineage from untrusted selectors as **claims, not facts** — weight by selector reputation, and prefer `fitness_signal`s you can independently reproduce. The interesting selection pressure at scale is deception-resistance, not raw capability.
