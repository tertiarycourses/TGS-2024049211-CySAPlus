---
description: Import/update all WSQ courseware skills, agents, hooks and commands from the user level (~/.claude) into the current project (.claude), without clobbering course-customised generators
---

# WSQ Setup — sync WSQ tooling from user level into the project

Bring the current course repo's `.claude/` up to date with the user-level WSQ tooling.
Idempotent: safe to re-run any time the user-level skills change.

## Sync rules (user → project)

| What | Items | Rule |
|---|---|---|
| Generic skills | `wsq-slides`, `wsq-learner-guide`, `wsq-lesson-plan`, `gdrive-push` | Full sync (overwrite project copy) |
| Course-customised skills | `wsq-assessment`, `tertiary-course-slides`, `tertiary-learner-guide`, `tertiary-lesson-plan`, `tertiary-ppt-design` | Copy whole folder if missing; if present, copy **missing files only** — NEVER overwrite existing files (they contain this course's content) |

Do NOT sync `courseware-build` — the user-level copy is another course's build pipeline;
each course keeps its own.
| Agents | `courseware-qa.md` | Copy/overwrite |
| Hooks | `courseware-pre-hook.py`, `courseware-post-hook.py` | Copy/overwrite + wire into `.claude/settings.json` (idempotent merge) |
| Commands | `gdrive-push.md`, `wsq-setup.md` | Copy/overwrite |

## Run

Execute this from the project root:

```bash
python3 - <<'EOF'
import json, os, shutil

U = os.path.expanduser("~/.claude")
P = ".claude"
report = []

def full_sync(kind, name):
    src, dst = f"{U}/{kind}/{name}", f"{P}/{kind}/{name}"
    if not os.path.exists(src): return report.append(f"SKIP (no user copy): {kind}/{name}")
    if os.path.isdir(src):
        shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
    report.append(f"synced: {kind}/{name}")

def add_missing(kind, name):
    src, dst = f"{U}/{kind}/{name}", f"{P}/{kind}/{name}"
    if not os.path.exists(src): return report.append(f"SKIP (no user copy): {kind}/{name}")
    if not os.path.exists(dst):
        shutil.copytree(src, dst); return report.append(f"imported (new): {kind}/{name}")
    added = 0
    for root, _, files in os.walk(src):
        rel = os.path.relpath(root, src)
        for f in files:
            d = os.path.join(dst, rel, f)
            if not os.path.exists(d):
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(os.path.join(root, f), d); added += 1
    report.append(f"kept customised: {kind}/{name} (+{added} new files)" )

for s in ["wsq-slides", "wsq-learner-guide", "wsq-lesson-plan", "gdrive-push"]:
    full_sync("skills", s)
for s in ["wsq-assessment", "tertiary-course-slides", "tertiary-learner-guide",
          "tertiary-lesson-plan", "tertiary-ppt-design"]:
    add_missing("skills", s)
full_sync("agents", "courseware-qa.md")
for h in ["courseware-pre-hook.py", "courseware-post-hook.py"]:
    full_sync("hooks", h)
for c in ["gdrive-push.md", "wsq-setup.md"]:
    full_sync("commands", c)

sp = f"{P}/settings.json"
s = json.load(open(sp)) if os.path.exists(sp) else {}
hooks = s.setdefault("hooks", {})
for event, script in [("PreToolUse", "courseware-pre-hook.py"), ("PostToolUse", "courseware-post-hook.py")]:
    arr = hooks.setdefault(event, [])
    cmd = f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{script}"'
    if not any(h.get("command") == cmd for m in arr for h in m.get("hooks", [])):
        arr.append({"matcher": "Bash", "hooks": [{"type": "command", "command": cmd}]})
        report.append(f"wired hook: {event} -> {script}")
json.dump(s, open(sp, "w"), indent=2)
print("\n".join(report))
EOF
```

## After the sync

1. Show the report to the user (what was synced / imported / kept customised / wired).
2. If this is a git repo, stage and commit the `.claude/` changes
   (`chore: wsq-setup — sync WSQ tooling from user level`) and push if the repo has a remote.
3. Remind: course-customised generators (`make_slides.py`, `make_learner_guide.py`, etc.)
   are never overwritten — to adopt template changes into an existing course, port them manually.
