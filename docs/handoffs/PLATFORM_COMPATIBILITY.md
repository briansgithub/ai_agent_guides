# Platform Discovery Smoke Matrix

This matrix tracks whether an IDE or agent host actually discovers its pointer file and follows it to `AGENTS.md`. It is maintenance evidence, not startup reading. A filename's presence or an agent's unsupported self-report is not proof of discovery.

## Status meanings

- **not-run:** convention is registered, but no live client smoke test is recorded;
- **pass:** the named client/version opened the repository root, identified `AGENTS.md` as authoritative through the entry point, and followed one harmless distinctive instruction;
- **fail:** that live client/version ignored the entry point or did not follow the pointer;
- **review-due:** an earlier pass predates a material client change or is no longer representative.

## Matrix

| Client/host | Entry point | Smoke status | Client/version and date | Evidence/notes |
|---|---|---|---|---|
| Codex, OpenCode, Zed, Cursor, VS Code chat, Grok CLI (xAI) | `AGENTS.md` | not-run | — | Authoritative file; test each host separately before claiming support |
| Claude Code, VS Code chat | `CLAUDE.md` | not-run | — | Pointer |
| Gemini CLI, Antigravity, Gemini Code Assist, Android Studio | `GEMINI.md` | not-run | — | Pointer; test each host separately |
| Cursor, including Grok in Cursor | `.cursor/rules/handoff-maintenance.mdc` | not-run | — | Always-apply pointer |
| Grok CLI (xAI) | `.grok/rules/agents.md` | not-run | — | Pointer; official Grok also loads `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/` |
| community grok-cli | `.grok/GROK.md` | not-run | — | Convention not live-tested here |
| GitHub Copilot | `.github/copilot-instructions.md` | not-run | — | Pointer |
| Cline | `.clinerules` | not-run | — | Pointer |
| Windsurf | `.windsurfrules` | not-run | — | Pointer |
| Zed | `.rules` | not-run | — | Pointer |
| Aider | `CONVENTIONS.md` | not-run | — | Pointer |
| JetBrains Junie | `.junie/guidelines.md` | not-run | — | Pointer |
| Amazon Q Developer | `.amazonq/rules/agents.md` | not-run | — | Pointer |
| Roo Code | `.roo/rules/agents.md` | not-run | — | Pointer |
| Qodo | `best_practices.md` | not-run | — | Pointer |
| Qwen | `QWEN.md` | not-run | — | Convention not live-tested here |
| Amp | `AGENT.md` | not-run | — | Convention not live-tested here |
| Trae | `.trae/rules/project_rules.md` | not-run | — | Convention not live-tested here |
| Firebase Studio | `.idx/airules.md` | not-run | — | Convention not live-tested here |
| Kilo | `.kilocode/rules/agents.md` | not-run | — | Convention not live-tested here |

## Minimal smoke procedure

1. Use a disposable repository containing the kit and one harmless, distinctive temporary instruction in `AGENTS.md`.
2. Open the repository root in one exact client/version; do not preload `AGENTS.md` manually.
3. Ask for a read-only response that demonstrates the distinctive instruction and names the authoritative rule file.
4. Record pass/fail, client/version, date, and a short reproducible note in the row. Remove the temporary instruction.
5. Retest only after a material client discovery change, a major upgrade, or evidence of failure. Mark old evidence `review-due` instead of repeatedly testing every release.

Keep claims client-specific: one host passing through `AGENTS.md` does not prove that another host listed in the same row does. Split a row when results differ. Structural tests only prove that registered pointer files exist, stay small, and reference `AGENTS.md`; they do not convert `not-run` into `pass`.
