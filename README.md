# ctx

**Save project context packs and inject them into any AI session in one command.**

```bash
pip install ctx

ctx save myproject          # scan + save current project as a context pack
ctx inject myproject        # copy to clipboard — paste into ChatGPT, Gemini, etc.
ctx inject myproject --target claude  # write CLAUDE.md — Claude Code reads it automatically
```

## How it works

1. **Save:** `ctx save myproject` scans your codebase — detects stack, maps structure, reads recent git commits, summarizes README. You can add custom notes on top.

2. **Inject:** `ctx inject myproject` puts the context pack wherever you need it.
   - `--target claude` → writes `CLAUDE.md` in the current directory (Claude Code auto-reads it)
   - `--target clipboard` → copies to clipboard for ChatGPT, Gemini, or any AI chat
   - `--target chatgpt` → same, formatted as a system prompt

## Install

```bash
pip install ctx
```

## Usage

```bash
# Save context packs
ctx save myproject                       # interactive — scans + prompts for notes
ctx save myproject --notes "FastAPI app" # non-interactive
ctx save myproject --scope local         # save in .ctx/ (git-committable)
ctx save myproject --scope global        # save in ~/.ctx/packs/ (default)

# Inject context
ctx inject myproject                          # → clipboard
ctx inject myproject --target claude          # → CLAUDE.md
ctx inject myproject --target chatgpt         # → clipboard (system prompt format)

# Manage packs
ctx list                  # show all packs (local + global)
ctx show myproject        # print pack to terminal
ctx edit myproject        # open in $EDITOR
ctx delete myproject      # remove pack
```

## What gets captured

```markdown
# myproject

## Stack
- Python
- Detected from: pyproject.toml

## Structure
src/
  api/
  models/
tests/

## Recent commits
- feat: add user auth
- fix: resolve migration conflict

## README
MyProject is a FastAPI app for...

## Notes
(your custom notes)
```

## Storage

- **Global:** `~/.ctx/packs/<name>.md` — available from any directory (default)
- **Local:** `.ctx/<name>.md` — project-specific, git-committable

Local packs take priority over global when names conflict.

## Requirements

- Python 3.10+
- `pbcopy` / `xclip` / `xsel` for clipboard support (usually pre-installed)

## License

MIT
