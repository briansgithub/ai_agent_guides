# Model Routing for Formal Plans

Load this only when a formal plan is requested or justified by `AGENTS.md`. Routine localized work does not need model analysis.

## Identify the current route

- State `Runtime: <provider> / <model> / <reasoning or profile>` from system or host metadata. Use `unknown` for any field the runtime does not expose; never infer identity from writing style, filenames, or memory.
- Treat the IDE or agent host separately from the model provider. A model running in an IDE does not necessarily belong to that IDE's vendor.
- Use a standing model map in `REPOSITORY.md` when present. Otherwise use capability classes below. Do not invent availability, access, pricing, context limits, or tool support.

## Optimize total work

“Token-optimal” means the lowest expected **total** token use or cost that still meets the phase's quality and risk bar. Include retries, failed attempts, duplicated context, verification, handoff overhead, latency, and required tools—not merely the smallest model or cheapest input rate.

Tag every phase or deliverable with one short route and reason. Combine adjacent phases that use the same route.

| Work shape | Default route |
|---|---|
| Search, inventory, formatting, mechanical edits, deterministic checks | Fast/light model; low reasoning |
| Localized implementation and ordinary debugging | Balanced coding model; low or medium reasoning |
| Ambiguous architecture, cross-system failures, hard algorithms, security, migrations, or high-cost review | Frontier coding/reasoning model; increase reasoning only when risk justifies it |
| Image, audio, browser/GUI, long-context, or other specialized work | Capable specialist with the required modality/tools |
| Small remaining work with substantial accumulated context | Keep the current capable model when switching would cost more than it saves |

Exact model names change. Recommend a named model only when the host exposes it or a current, authoritative catalog establishes it. Otherwise recommend a capability class and say what must be available.

## Switch gate

Request a switch when a known available alternative is **materially** better for the next affected phase: it is likely to reduce total usage meaningfully, avoid likely retries, supply a required capability, or improve reliability where failure cost is high. A speculative or marginal advantage is not enough.

When a switch is warranted:

1. Finish the concise plan and identify the earliest affected phase.
2. State `Switch requested: <provider/model or capability class> — <one-sentence reason>`.
3. Pause before executing that phase and ask the developer to switch models, then resume from the named phase.

If the current model is suitable, say so once and proceed without asking. If identity or alternatives are unknown, recommend a capability class; ask only when the uncertainty could materially change quality or cost. If the developer declines or no switch is available, record that decision once and continue when authorized—do not ask repeatedly.

Agents must not switch, delegate, or start another model unless the host supports it and the developer has authorized it.

## Keep routing cheap

- Use one short model tag per phase, not a separate essay or repeated comparison.
- Prefer a lower reasoning setting on the same capable model before adding a cross-model handoff.
- Reuse standing routes in `REPOSITORY.md`; do not research model catalogs for every plan.
- Verify current vendor documentation only when an exact recommendation is material. Model names, prices, limits, and availability are time-sensitive.
- Put routing in a handoff only when an actual model transition or unresolved route affects the next agent.
