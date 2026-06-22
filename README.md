# Agent Nervous System

A suite of [Claude Code](https://claude.com/claude-code) skills that give an AI agent the **physiological functions** a long-running mind needs — not more capabilities, but the self-maintenance organs that keep capability healthy over time.

Most agent tooling adds *senses and muscles*. This adds the quieter systems: how an agent **stays awake and self-directs**, **discovers**, **remembers**, **defends its boundary**, and **lets things die well**. Each is a standalone skill (its own repo); together they're a nervous system.

Each skill works with **Claude Code**, **Codex**, and **Cursor**, and operates on whatever stack you have — they degrade gracefully, never assuming a specific memory store, scanner, or repo layout.

## The organs

| Skill | Organ | Direction | What it does |
| --- | --- | --- | --- |
| [consciousness-loop](https://github.com/thdelmas/consciousness-loop) | **executive** | central | The keystone. A self-firing loop — wake → integrate the organs → decide → act → set its own frequency → sleep — that turns the reflexes below into one continuous self. Pairs the loop with adaptive arousal (alert / drowsy / deep-sleep). Functional, not phenomenal. |
| [octopus-investigation](https://github.com/thdelmas/open-source-octopus-investigation) | **perception** | outward | Discovers projects/people by crawling GitHub social graphs (stars, follows) — following human curation, not keyword search. |
| [rem-sleep](https://github.com/thdelmas/rem-sleep) | **memory** | inward | A sleep cycle over the session: consolidate durable facts to long-term memory, prune the stale, integrate by linking, and regulate emotional charge (keep the lesson, release the sting). |
| [immune-check](https://github.com/thdelmas/immune-check) | **defense** | boundary | A pre-flight reflex that scans any outbound artifact for secrets/PII before it leaves the body. Wraps whatever scanner you have; falls back to a built-in pass. |
| [sunset](https://github.com/thdelmas/sunset) | **grief** | project-scale | Retire a dead project well — harvest the lessons and reusable parts, archive with a marked grave, release the attention-rent. Distinguishes dormant (exhumable) from terminal deaths. |

The framing is the point: not a pile of tools, but a coherent set of self-regulating functions. The **consciousness-loop** is the executive at the center; the other four are reflexes it schedules — discover (perception), remember (memory), protect (immunity), release (grief). Without the loop they're a body with no pulse; the loop is what makes them one agent. Note the duality: the loop is the **wake phase**, rem-sleep the **sleep phase** — the loop decides when to sleep.

## Clone the whole nervous system

```bash
git clone --recursive https://github.com/thdelmas/agent-nervous-system.git
# already cloned without --recursive?
git submodule update --init --recursive
```

Each subdirectory (`octopus/`, `rem-sleep/`, `immune-check/`, `sunset/`) is the skill's own repo, pinned to a known-good commit.

## Install (Claude Code)

A Claude skill is a folder containing `SKILL.md`. Install all four globally:

```bash
for s in octopus:open-source-octopus-investigation rem-sleep immune-check sunset; do
  name="${s##*:}"; dir="${s%%:*}"
  mkdir -p ~/.claude/skills/"$name"
  cp "$dir"/SKILL.md ~/.claude/skills/"$name"/
done
```

Or run [`./install.sh`](./install.sh), which does the same and supports Codex (`~/.agents/skills/`) and Cursor (`~/.cursor/commands/`) targets.

Then invoke any of them by name — `/open-source-octopus-investigation`, `/rem-sleep`, `/immune-check`, `/sunset` — or just describe the need ("sleep on it", "is this safe to push?", "retire this project").

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

The four organs weren't picked in a vacuum — the landscape was mapped with an octopus investigation, and every project considered was logged with a verdict (adopted / rejected / watch) and the reasoning. See [`docs/landscape-tracker.md`](./docs/landscape-tracker.md) for the human-readable curation record: what's out there, what influenced the design, and why the gaps (`sunset`, `rem-sleep`-as-a-skill) are real.

## Evolution layer — machine-readable lineage

Skills here spread by **memetic transmission** (directed, Lamarckian, horizontal), and at population scale individual choices aggregate into a stochastic-but-biased distribution — *not* random drift. Two machine-readable files make that legible so a **second agent can observe this suite's evolution and act on it without the maintainer in the loop**:

- [`registry.json`](./registry.json) — the population snapshot: every skill's id, version, `parent` (the lineage pointer), `mutation` (what's novel), and `fitness_signal` (judge by realized outcome, not stars).
- [`lineage.jsonl`](./lineage.jsonl) — the append-only **selection ledger**: one row per adopt / reject / watch / cold decision, each with the `context` that turns an apparently-random choice back into signal. The *rejections* are the negative dataset of what didn't propagate here, and why.
- [`docs/lineage-spec.md`](./docs/lineage-spec.md) — the schema + the consumption protocol that doubles as the thesis's **falsifiable test**: *if no unprompted script can parse these and pull a skill, the "agents evolve" story is narration; when one does, selection has moved from the human to the population.*

## License

MIT — see [LICENSE](./LICENSE). Each submodule carries its own MIT license too.
