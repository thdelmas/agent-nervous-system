# Landscape Tracker — what was considered, and the verdict

A graph tracker for the Agent Nervous System suite. Produced by an [octopus investigation](https://github.com/thdelmas/open-source-octopus-investigation) of the agent-skills / agent-memory / cognitive-architecture landscape, then annotated with a **verdict** for each node: was it adopted into the suite's thinking, and *why* or why not.

This is the curation record — it shows the roads not taken as deliberately as the ones taken, so a future run (or a contributor) doesn't re-litigate a decision already made.

- **Run:** 2026-06-22 · **Origin:** `obra` (Jesse Vincent) · **Depth:** 2 · **Calls:** ~19
- **Verdict key:** `Adopt` (influences the suite — compat target, collaboration lead, or integration substrate) · `Reject` (out of scope / different category / unrelated) · `Watch` (promising, revisit next run) · `Cold` (dead end)

## The graph

```
obra (origin, 7k followers, follows 93 — tight curation)
├─ A. Agent Skills ──── agentskills/agentskills · huggingface/skills · superpowers/* · oaustegard/claude-skills
├─ B. Agent Memory ──── mem0 · mempalace · graphiti · obra/episodic-memory · lhl/agentic-memory
├─ C. Agent OS ──────── openfang · mira-OSS · openclaw · modelcontextprotocol/servers
├─ D. Boundary/Introspect ─ Infisical/agent-vault · screenpipe · kenn-io/agentsview · 1Password/SCAM
└─ E. Reflection/Emotional ─ obra/private-journal-mcp · obra/episodic-memory · double-shot-latte
   (off-graph, pruned: obra's keyboard cluster — QMK/Keyboardio · nervous-net org)
```

## Verdicts

| Node | Tentacle | Stars | Considered as | Verdict | Reasoning |
| --- | --- | --- | --- | --- | --- |
| `obra` (Jesse Vincent) | origin | 7k flw | Collaboration lead | **Adopt** | Independently built episodic-memory + private-journaling — the nervous-system instinct already resonates with a major hub. The one person worth engaging directly. |
| `agentskills/agentskills` | A | 20.9k | Compatibility target | **Adopt** | The emerging **spec** for Agent Skills. The four `SKILL.md` files should nod to it so they're portable, not bespoke. |
| `obra/superpowers` (+ marketplace/skills/lab) | A | very high | Distribution model | **Watch** | Proven skills-as-plugins + marketplace pattern. A future home for distributing the suite, but adopting their plugin format is a bigger commitment than this run decides. |
| `huggingface/skills` | A | 10.7k | Distribution model | **Watch** | Another skills-distribution surface. Revisit if the suite goes wide. |
| `oaustegard/claude-skills` | A | 126 | Peer / precedent | **Watch** | A personal skill collection of the same shape — kindred, low-stakes to learn from. |
| `obra/private-journal-mcp` | E | 380 | Design precedent for `rem-sleep` | **Adopt** | Nearest kin to rem-sleep's emotional-regulation stage ("process feelings and thoughts") — but shipped as an MCP server. Confirms the niche; borrow the design, keep the skill form. |
| `obra/episodic-memory` | B/E | 421 | Design precedent for `rem-sleep` | **Adopt** | Episodic consolidation as an organ — same instinct as rem-sleep, different delivery. Strongest single signal that the framing is real. |
| `obra/mira-OSS` | C | 13 | Inspiration (whole-suite) | **Watch** | "Elegant brain-in-box" — memories decay through momentum loss, modular composition. The closest thing to a *systemic* nervous-system vision; interesting, niche, worth tracking. |
| `mem0ai/mem0` | B | 59k | Integration substrate (not competitor) | **Reject (as peer)** | A memory **database/layer**. rem-sleep is a *ritual that operates on storage* — different category. Don't compete; rem-sleep could sit on top of it. Not a rival, not a dependency this run takes. |
| `MemPalace/mempalace` | B | 56k | Integration substrate | **Reject (as peer)** | Same reasoning — benchmarked memory layer, not a behavioral skill. Plumbing, not ritual. |
| `getzep/graphiti` | B | 27.7k | Integration substrate | **Reject (as peer)** | Real-time knowledge-graph infra. Could be a backing store for a memory skill, but it is not in the suite's category. |
| `Infisical/agent-vault` | D | 1.7k | Parallel to `immune-check` | **Reject (as overlap)** | Closest neighbor to immune-check, but a **runtime credential proxy**, not a pre-flight scan ritual. Different mechanism; no overlap to resolve. Confirms the niche is uncrowded. |
| `RightNow-AI/openfang` | C | 17.9k | Framing reference | **Watch** | "Agent Operating System" — the OS framing one level above ours. Useful vocabulary; revisit for positioning. |
| `screenpipe/screenpipe` | C/D | 19.4k | Perception organ (external) | **Reject (out of scope)** | 24/7 capture/recording — a *senses* layer. The suite is self-maintenance, not capture. Out of scope by design. |
| `modelcontextprotocol/servers` | C | 87.5k | Infra context | **Reject (out of scope)** | The MCP commons — relevant backdrop, but infrastructure, not a skill peer. |
| `kenn-io/agentsview` · `roborev` | D | 3.1k / 1.4k | Introspection precedent | **Watch** | Session analytics / continuous review for agents — proprioception-adjacent. A future "proprioception" organ could learn from these. |
| `1Password/SCAM` | D | 130 | Eval reference for `immune-check` | **Watch** | Benchmark for agent security awareness. Could become a test harness for immune-check's judgment. |
| `huginn/huginn` | — | 49k | Historical precedent | **Watch** | The OG "agents that monitor and act on your behalf." Pre-LLM, but the autonomy framing predates the whole field. |
| `bcherny/openclaw` | C | 51 | Context (Claude Code lineage) | **Cold** | Personal-assistant agent from Claude Code's creator; interesting lineage, but not on-theme for the suite. |
| `nervous-net` (org) | — | 16 | Naming-neighbor check | **Cold** | Name collision only — a vibe-coding org (point-of-sale, video rental). **Useful negative result: the "agent nervous system" framing has no namesake precedent.** |
| obra keyboard cluster (QMK/Keyboardio) | — | — | — | **Cold** | obra's hardware life — off-theme. Pruned breadth-first to avoid tunneling. |

## What the verdicts add up to

- **The framing is differentiated.** No project frames a *suite of behavioral skills as a nervous system / set of organs*. Memory is crowded but it's all infrastructure; skills are crowded but generic. The physiology framing is the moat.
- **Two organs have no real competition:** `sunset` (grief / retirement) — zero parallels found; and `rem-sleep` *as a skill* — everyone built the storage (mem0, graphiti, mempalace), nobody built the ritual layer on top.
- **One person to engage:** `obra`, who reached for the same memory + journaling instincts independently.
- **One standard to honor:** the `agentskills/agentskills` spec.

## Queued for the next run

`obra/episodic-memory` + `private-journal-mcp` (study the design directly) · `RightNow-AI/openfang` (the OS framing) · `huginn/huginn` · people `pfrazee` / `harperreed` / `lhl` for the memory-architecture crowd.
