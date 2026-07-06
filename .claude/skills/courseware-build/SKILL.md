---
name: courseware-build
description: One-command aligned build of the full WSQ courseware set for this course — the versioned Slides deck (PPTX+PDF), Learner Guide (DOCX+MD+PDF) and Lesson Plan (DOCX+PDF), all aligned to the hands-on labs with slide-number cross-references. Use when regenerating or updating the courseware after editing course content.
---

# Courseware Build (aligned, one command)

Regenerates every courseware artifact for this course from a single source of
truth so the Slides, Learner Guide and Lesson Plan never diverge.

## Run
```bash
bash .claude/skills/courseware-build/build_courseware.sh      # LibreOffice or MS Office
# or, on Windows with MS Office:
python .claude/skills/courseware-build/build_courseware.py
```

## What it does
1. `_shared/build_slides.py` → `courseware/<Course Title>-v<N>.pptx` (writes `manifest.json` with slide numbers).
2. `_shared/build_lg.py` → `courseware/LG-<Course Title>.docx` + `.md` (+ diagrams in `courseware/images/`).
3. `_shared/build_lp.py` → `courseware/LP-<Course Title>.docx` (reads `manifest.json` for the Slides column).
4. Renders all PDFs (LibreOffice `soffice`, else MS Office COM via pywin32).

## Where the content lives
- `_shared/config.py` — course metadata (title, code, TSC K/A, learning outcomes, domains, versions, per-lab environment, diagram→lab map).
- `_shared/labs/*.md` — the 30 hands-on lab sources (parsed for step-by-step content).
- `_shared/images/*.png` — reference diagrams embedded per lab.
- `_shared/assets/` — `tertiary_logo.png`, `cysa_logo.png` (course badge).
- `_shared/brand.py` / `brand_doc.py` — the Tertiary Infotech house design system (PPT + DOCX).

## House rules
Follows the `tertiary-ppt-design`, `tertiary-course-slides`, `tertiary-learner-guide`
and `tertiary-lesson-plan` skills (white theme, Arial, brand colours #1F6FEB/#0FB980,
cover + version-control + footers). Bump the version in `config.py` on every content change.
