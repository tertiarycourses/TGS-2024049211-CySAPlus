---
name: gdrive-push
description: Push the current WSQ courseware (slides PPT/PDF, Learner Guide, Lesson Plan, assessments) to the user's Google Drive courseware folder, auto-archiving old versions. Use when the user runs /gdrive-push or asks to upload/push courseware to Google Drive. ALWAYS requires the user-supplied Drive folder link.
---

# GDrive Push — WSQ courseware to Google Drive

Uploads the course's current artifacts into the right subfolders of a Google Drive
courseware folder, moving all superseded files into an `archive` subfolder first.
**Upload-only: nothing on Drive is ever deleted.**

## HARD RULE — user input required

**NEVER push without the user-provided Google Drive folder link.** If the user did not
include the courseware folder link (e.g. `/gdrive-push <link>`), ASK for it first
(AskUserQuestion) and wait. Do not fall back to a remembered, default, or previously
used folder. Confirm the link before the first real (non-dry-run) push of a session.

## Routing

| Drive subfolder (created if missing) | Files pushed |
|---|---|
| Master Trainer Slides | slide deck `.pptx` + `.pdf` (current version only) |
| Learner Guide | `LG-*.docx` + `LG-*.pdf` + the slides `.pdf` |
| Lesson Plan | `LP-*.docx` + `LP-*.pdf` |
| Assessment | all `assessment/*.docx` (WA + PP papers and answer keys) |
| Activities | the whole `labs/` tree (structure preserved) |

**Change detection — only changed files are pushed.** Every file's MD5 is compared
with the Drive copy first; identical files are skipped (no re-upload, no archiving).
The labs sync uses `rclone sync --checksum --backup-dir Activities/archive`, so
unchanged lab files are skipped and replaced/removed ones are MOVED to the archive,
never deleted.

**Archiving — each courseware folder ends up holding ONLY the current files.**
Before uploading, EVERY pre-existing file that is not identical to a pushed file —
old versions, differently-named old decks, Google-native Docs/Slides — is MOVED
server-side into that folder's `archive/` subfolder. The archive folder is
**created if absent**, and any existing `Archive`/`archives` variant is **renamed
to the canonical lowercase `archive`** (case-only renames via a two-step move).
A file that cannot be moved is reported as a WARNING and skipped, never deleted.
Target subfolders are matched case-insensitively (an existing "Assessments" folder
is reused, not duplicated).

Every uploaded file is then set to **"anyone with the link can view"** (via
`rclone link`, which creates the reader permission) and its view link is printed —
include the links in the report to the user.

## How to run

```bash
python3 <this-skill-dir>/gdrive_push.py "<drive-folder-link>" --repo "<course repo>" --dry-run   # preview
python3 <this-skill-dir>/gdrive_push.py "<drive-folder-link>" --repo "<course repo>"             # real push
```

Always run `--dry-run` first and show the user the plan; then do the real push.
Report per-folder what was archived and uploaded.

## Transport / prerequisites

The script talks to Google Drive **directly via rclone** (remote name `gdrive`,
override with env `GDRIVE_REMOTE`). All Drive operations are upload (`copyto`) or
server-side move to Archive (`moveto`) — there is no delete anywhere.

- One-time setup if the remote is missing: `brew install rclone` then
  `rclone config create gdrive drive scope=drive` and complete the Google sign-in
  in the browser (use the account that owns the courseware folder).
- The `--drive-root-folder-id` flag scopes every call to the user-supplied folder,
  so the script cannot touch anything outside it.
