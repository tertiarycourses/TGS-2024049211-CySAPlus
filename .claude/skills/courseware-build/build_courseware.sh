#!/usr/bin/env bash
# Single-command aligned build of all courseware for this WSQ course.
# Generates the versioned PPT + Learner Guide + Lesson Plan (DOCX) with
# slide-number-aligned content, then renders PDFs. Output -> courseware/.
#
# Content lives in .claude/skills/_shared (config.py + labs/ + images/).
# PDF rendering uses LibreOffice if present, else MS Office COM (Windows).
set -euo pipefail
cd "$(dirname "$0")/../../.."          # repo root
python3 ".claude/skills/_shared/build_all.py"
