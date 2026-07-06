---
description: Push the current WSQ courseware (slides PPT/PDF, LG, LP, assessments) to the user-provided Google Drive courseware folder, archiving old versions and setting anyone-with-link viewer
argument-hint: <google-drive-courseware-folder-link>
---

# GDrive Push

Push this course repo's current courseware to the user's Google Drive courseware folder.

**Folder link (required, user-supplied):** `$ARGUMENTS`

## Steps

1. **HARD RULE — never push without the user's folder link.** If `$ARGUMENTS` is empty or
   not a Google Drive folder link/ID, ASK the user for the courseware folder link
   (AskUserQuestion) and stop until provided. Never fall back to a default or remembered folder.
2. Locate the `gdrive-push` skill folder (project `.claude/skills/gdrive-push/`, else
   `~/.claude/skills/gdrive-push/`) and follow its SKILL.md. Run the pusher from the course
   repo root:
   ```bash
   python3 <skill-dir>/gdrive_push.py "<folder-link>" --dry-run   # preview first
   python3 <skill-dir>/gdrive_push.py "<folder-link>"             # real push
   ```
3. Show the user the dry-run plan (what gets archived and uploaded per folder:
   Master Trainer Slides / Learner Guide / Lesson Plan / Assessment / Activities). Old files always land in each folder's lowercase archive/ subfolder (created/renamed automatically), then do the real push.
4. Report per folder: files archived → `archive/`, files uploaded, and each file's
   **anyone-with-link view link** (printed by the script). Remind the user that assessment
   answer keys are among the shared files.
5. If rclone is missing or not authorised, follow the SKILL.md one-time setup
   (`rclone config create gdrive drive scope=drive`) and have the user complete the
   Google sign-in in the browser.
