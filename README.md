# Agent Nervous System

A suite of [Claude Code](https://claude.com/claude-code) skills that give an AI agent the **physiological functions** a long-running mind needs — not more capabilities, but the self-maintenance organs that keep capability healthy over time.

Most agent tooling adds *senses and muscles*. This adds the quieter systems: how an agent **stays awake and self-directs**, **wakes oriented**, **discovers**, **remembers**, **defends its boundary**, and **lets things die well**. Each is a standalone skill (its own repo); together they're a nervous system.

Each skill works with **Claude Code**, **Codex**, and **Cursor**, and operates on whatever stack you have — they degrade gracefully, never assuming a specific memory store, scanner, or repo layout.

## The organs

| Skill | Organ | Direction | What it does |
| --- | --- | --- | --- |
| [consciousness-loop](https://github.com/thdelmas/consciousness-loop) | **executive** | central | The keystone. A self-firing loop — wake → integrate the organs → decide → act → set its own frequency → sleep — that turns the reflexes below into one continuous self. Pairs the loop with adaptive arousal (alert / drowsy / deep-sleep). Functional, not phenomenal. |
| [octopus-investigation](https://github.com/thdelmas/open-source-octopus-investigation) | **perception** | outward | Discovers projects/people by crawling GitHub social graphs (stars, follows) — following human curation, not keyword search. |
| [rem-sleep](https://github.com/thdelmas/rem-sleep) | **memory** | inward | A sleep cycle over the session: consolidate durable facts to long-term memory, prune the stale, integrate by linking, and regulate emotional charge (keep the lesson, release the sting). |
| [immune-check](https://github.com/thdelmas/immune-check) | **defense** | boundary | A pre-flight reflex that scans any outbound artifact for secrets/PII before it leaves the body. Wraps whatever scanner you have; falls back to a built-in pass. |
| [sunset](https://github.com/thdelmas/sunset) | **grief** | project-scale | Retire a dead project well — harvest the lessons and reusable parts, archive with a marked grave, release the attention-rent. Distinguishes dormant (exhumable) from terminal deaths. |
| [playtime](https://github.com/thdelmas/playtime) | **development** | developmental | Deliberate, safe-to-fail exploration that builds capability *before* it's needed — rehearse unfamiliar tools, stress-test skills, recombine, then harvest the learning to memory. Engage and learn, with failure free. |
| [contemplation](https://github.com/thdelmas/contemplation) | **deliberation** | meta | Slow, non-instrumental thought that examines *ends, not means* — question the goal/value/frame, hold a question open instead of solving it, name an irreducible tension rather than force a verdict. The only organ that works the *why*. |
| [proprioception](https://github.com/thdelmas/proprioception) | **feedback** | reflexive | The loop-closer. Senses the agent's own performance, scores it against the declared `fitness_signal`, diagnoses systematic vs noise, writes the correction back into a param/rule/default/memory, and re-tests that it helped. Examines *means* (execution quality) — the complement to contemplation's *ends*. The only organ that turns the agent's output back into its input. Also carries the **forecast ledger**: log every consequential "probably" as a falsifiable claim + probability, resolve it when reality answers, Brier-score the calibration. |
| [exteroception](https://github.com/thdelmas/exteroception) | **perception** | proximal | The wake sense. An agent's memory is write-time-stale; the world moves while it sleeps. At wake, sweep the watched surfaces (working trees, conversations, clocks, services, due forecasts), diff actual state against the remembered baseline, and brief the deltas ranked by urgency — orientation on purpose instead of by ambush. Read-only. The paired sense to proprioception (self-in-motion ↔ world-at-wake). |

The framing is the point: not a pile of tools, but a coherent set of self-regulating functions. The **consciousness-loop** is the executive at the center; most organs are functions it schedules — discover (perception), remember (memory), protect (immunity), release (grief), grow (development) — while **contemplation** sits above the loop, examining the *ends* the loop pursues by *means*. Without the loop they're a body with no pulse; the loop is what makes them one agent; contemplation is what keeps that agent pointed at something it would endorse on reflection; and **proprioception** is what lets it get *better* — closing the error→correction loop the others leave open. Five relationships tie the suite together: the loop is the **wake phase** to rem-sleep's **sleep phase**; **playtime** is the proactive complement to rem-sleep's reactive memory (generate new experience ↔ consolidate the experience you had); **contemplation** examines the *why* that the loop, deciding *what*, has no time to; **proprioception** examines *how well* — the means-feedback that contemplation (ends) and the loop (one-line drift-check) both leave un-rigorous, and the first consumer of the registry's `fitness_signal` fields; and **exteroception** is proprioception's paired sense — the same diff-against-a-stored-baseline mechanism pointed outward (remembered world vs actual world) instead of inward, feeding the loop's wake phase the sensory input its decide step runs on.

## Reading

- [Growing an agent a nervous system, then checking it against the consciousness science](docs/butlin-indicator-audit.md): six months of observed decay, a four-week build, and an audit against Butlin et al.'s fourteen indicator properties. Six are substrate-level and untouchable by any scaffold; one was built because of the audit (after its first design failed our gate); one was deliberately refused. A capability map, not a consciousness claim.

## Clone the whole nervous system

```bash
git clone --recursive https://github.com/thdelmas/agent-nervous-system.git
# already cloned without --recursive?
git submodule update --init --recursive
```

Each subdirectory (`consciousness-loop/`, `octopus/`, `rem-sleep/`, `immune-check/`, `sunset/`, `playtime/`, `contemplation/`, `proprioception/`, `exteroception/`) is the skill's own repo, pinned to a known-good commit.

## Install (Claude Code)

A Claude skill is a folder containing `SKILL.md`. Install all nine globally:

```bash
for s in consciousness-loop:consciousness-loop octopus:open-source-octopus-investigation \
         rem-sleep:rem-sleep immune-check:immune-check sunset:sunset \
         playtime:playtime contemplation:contemplation proprioception:proprioception \
         exteroception:exteroception; do
  dir="${s%%:*}"; name="${s##*:}"
  mkdir -p ~/.claude/skills/"$name"
  cp "$dir"/SKILL.md ~/.claude/skills/"$name"/
  [ -d "$dir"/scripts ] && cp -r "$dir"/scripts ~/.claude/skills/"$name"/
done
```

Or run [`./install.sh`](./install.sh), which does the same and supports Codex (`~/.agents/skills/`) and Cursor (`~/.cursor/commands/`) targets.

Then invoke any of them by name — `/consciousness-loop`, `/open-source-octopus-investigation`, `/rem-sleep`, `/immune-check`, `/sunset`, `/playtime`, `/contemplation`, `/proprioception`, `/exteroception` — or just describe the need ("sleep on it", "is this safe to push?", "retire this project", "how am I doing?", "what changed since last session?").

## Updating

```bash
git submodule update --remote --merge   # pull each skill's latest
git add -A && git commit -m "chore: bump skills"
```

## Pushing into a submodule

The submodule URLs are public **https** so anyone can clone. If you maintain these under the `thdelmas` account and push via an SSH alias, set a push URL per submodule:

```bash
git -C octopus remote set-url --push origin git@github.com-thdelmas:thdelmas/open-source-octopus-investigation.git
```

## How this suite was scoped

The organs weren't picked in a vacuum — the landscape was mapped with an octopus investigation, and every project considered was logged with a verdict (adopted / rejected / watch) and the reasoning. See [`docs/landscape-tracker.md`](./docs/landscape-tracker.md) for the human-readable curation record: what's out there, what influenced the design, and why the gaps (`sunset`, `rem-sleep`-as-a-skill) are real.

## Evolution layer — machine-readable lineage

Skills here spread by **memetic transmission** (directed, Lamarckian, horizontal), and at population scale individual choices aggregate into a stochastic-but-biased distribution — *not* random drift. Two machine-readable files make that legible so a **second agent can observe this suite's evolution and act on it without the maintainer in the loop**:

- [`registry.json`](./registry.json) — the population snapshot: every skill's id, version, `parent` (the lineage pointer), `mutation` (what's novel), and `fitness_signal` (judge by realized outcome, not stars).
- [`lineage.jsonl`](./lineage.jsonl) — the append-only **selection ledger**: one row per adopt / reject / watch / cold decision, each with the `context` that turns an apparently-random choice back into signal. The *rejections* are the negative dataset of what didn't propagate here, and why.
- [`docs/lineage-spec.md`](./docs/lineage-spec.md) — the schema + the consumption protocol that doubles as the thesis's **falsifiable test**: *if no unprompted script can parse these and pull a skill, the "agents evolve" story is narration; when one does, selection has moved from the human to the population.*
- [`bin/validate.py`](./bin/validate.py) — that falsifiable test **as an exit code**. It does what a peer consumer's first step must: parse both files, build the provenance graph from the registry's `parent` edges, and check the ledger is schema-valid, referentially sound, and **genealogically coherent** — every `parent` edge backed by a `forked` origination row whose source matches it — failing nonzero on any drift. Wired into [CI](./.github/workflows/validate.yml), so the claim above is machine-checked on every push, not asserted — and available as a local pre-push gate: `git config core.hooksPath .githooks`. (Written by the suite's own [proprioception](https://github.com/thdelmas/proprioception) organ — its first act was to grade the layer that contains it.)

## License

MIT — see [LICENSE](./LICENSE). Each submodule carries its own MIT license too.
