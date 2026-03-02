---
title: I built a CLI that gives any AI instant context about your project
published: true
tags: python, ai, claude, devtools
---

Every time I start a new AI session, I spend the first few minutes explaining the same things:

- "This is a FastAPI project"
- "We use SQLAlchemy for the ORM"
- "The main entry point is `src/api/main.py`"
- "Recent work has been on the auth module"

It's tedious. And AI tools like Claude Code, ChatGPT, and Gemini start cold every session.

So I built `ctx`.

```bash
pip install ctx

ctx save myproject          # scan project, save as context pack
ctx inject myproject        # paste into any AI chat instantly
ctx inject myproject --target claude  # write CLAUDE.md for Claude Code
```

## What it does

`ctx save` scans your project and builds a context pack automatically:

- **Stack detection** — finds `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Gemfile`, etc.
- **Structure map** — directory tree of your `src/`, `tests/`, `api/` folders
- **Git log** — last 10 commits so the AI understands what you've been working on
- **README summary** — first few lines as project context
- **Your notes** — add anything extra on top

The result is a clean Markdown file that any AI can parse immediately.

## Inject anywhere

`ctx inject myproject` puts the context pack where you need it:

```bash
ctx inject myproject                      # → clipboard (paste into ChatGPT, Gemini, etc.)
ctx inject myproject --target claude      # → writes CLAUDE.md in current directory
ctx inject myproject --target chatgpt     # → clipboard, formatted as a system prompt
```

Claude Code reads `CLAUDE.md` automatically when you open a project. No paste needed.

For ChatGPT, Gemini, or anything else — one paste at the start of the session and you're fully loaded.

## What a pack looks like

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
- refactor: extract service layer

## README
MyProject is a FastAPI app for managing...

## Notes
Main entry: src/api/main.py
Auth lives in src/auth/ — JWT-based, no sessions
```

## Global vs local packs

```bash
ctx save myproject --scope global   # ~/.ctx/packs/myproject.md (default, any directory)
ctx save myproject --scope local    # .ctx/myproject.md (project-specific, git-committable)
```

Local packs take priority. Commit `.ctx/` to your repo and your whole team gets the same context.

## The full command set

```bash
ctx save myproject          # scan + save
ctx list                    # show all packs
ctx show myproject          # print pack to terminal
ctx inject myproject        # inject (clipboard by default)
ctx edit myproject          # open in $EDITOR
ctx delete myproject        # remove pack
```

## Why this matters

"Context engineering" is the new prompt engineering. The models are good. What holds them back is not having enough context about *your* project — your conventions, your current work, your architecture decisions.

`ctx` is a local, zero-dependency way to fix that. No account. No sync service. Just Markdown files you control.

## Try it

```bash
pip install ctx

# In any project
ctx save myproject --notes "Add anything you want the AI to know"
ctx inject myproject --target claude
```

Source: [github.com/LakshmiSravyaVedantham/ctx](https://github.com/LakshmiSravyaVedantham/ctx)

---

*What's your biggest friction starting an AI session on an existing codebase? Drop it in the comments.*
