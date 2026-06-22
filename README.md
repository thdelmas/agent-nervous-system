# Agent Nervous System

A suite of [Claude Code](https://claude.com/claude-code) skills that give an AI agent the **physiological functions** a long-running mind needs — not more capabilities, but the self-maintenance organs that keep capability healthy over time.

Most agent tooling adds *senses and muscles*. This adds the quieter systems: how an agent **discovers**, **remembers**, **defends its boundary**, and **lets things die well**. Each is a standalone skill (its own repo); together they're a nervous system.

Each skill works with **Claude Code**, **Codex**, and **Cursor**, and operates on whatever stack you have — they degrade gracefully, never assuming a specific memory store, scanner, or repo layout.

## The organs

| Skill | Organ | Direction | What it does |
| --- | --- | --- | --- |
| [octopus-investigation](https://github.com/thdelmas/open-source-octopus-investigation) | **perception** | outward | Discovers projects/people by crawling GitHub social graphs (stars, follows) — following human curation, not keyword search. |
| [rem-sleep](https://github.com/thdelmas/rem-sleep) | **memory** | inward | A sleep cycle over the session: consolidate durable facts to long-term memory, prune the stale, integrate by linking, and regulate emotional charge (keep the lesson, release the sting). |
| [immune-check](https://github.com/thdelmas/immune-check) | **defense** | boundary | A pre-flight reflex that scans any outbound artifact for secrets/PII before it leaves the body. Wraps whatever scanner you have; falls back to a built-in pass. |
| [sunset](https://github.com/thdelmas/sunset) | **grief** | project-scale | Retire a dead project well — harvest the lessons and reusable parts, archive with a marked grave, release the attention-rent. Distinguishes dormant (exhumable) from terminal deaths. |

The framing is the point: not a pile of tools, but a coherent set of self-regulating functions. Discover (perception) → remember (memory) → protect (immunity) → release (grief).

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

The four organs weren't picked in a vacuum — the landscape was mapped with an octopus investigation, and every project considered was logged with a verdict (adopted / rejected / watch) and the reasoning. See [`docs/landscape-tracker.md`](./docs/landscape-tracker.md) for the curation record: what's out there, what influenced the design, and why the gaps (`sunset`, `rem-sleep`-as-a-skill) are real.

## License

MIT — see [LICENSE](./LICENSE). Each submodule carries its own MIT license too.
