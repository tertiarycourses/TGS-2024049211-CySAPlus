#!/usr/bin/env python3
"""Push WSQ courseware + labs DIRECTLY to the user's Google Drive courseware folder via
rclone, archiving old versions. Upload-and-move only — nothing on Drive is ever deleted.

Usage:  python3 gdrive_push.py <drive-folder-link-or-id> [--repo DIR] [--dry-run]

Routing (folders matched case-insensitively under the given root; created if missing):
  Master Trainer Slides : slides .pptx + .pdf
  Learner Guide         : LG .docx + .pdf, plus the slides .pdf
  Lesson Plan           : LP .docx + .pdf
  Assessment            : all assessment .docx (question papers + answer keys)
  Activities            : the whole labs/ tree (rclone sync with --backup-dir)

Change detection: files whose MD5 already matches the Drive copy are SKIPPED (no
re-upload, no archiving). Only changed/new files are pushed.

Archiving: in each courseware folder, EVERY pre-existing file that is not identical
to a file being pushed (old versions, old names, Google-native docs) is MOVED
server-side into that folder's "archive" subfolder first. The archive folder is
created if absent, and any "Archive"/"archives" variant is renamed to the canonical
lowercase "archive". For labs, changed/removed files are MOVED to Activities/archive
by rclone's --backup-dir. Nothing is ever deleted.

Every newly uploaded courseware file is set to "anyone with the link can view".

Prerequisite (one-time): `rclone config create gdrive drive scope=drive`.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

REMOTE = os.environ.get("GDRIVE_REMOTE", "gdrive")


def rc(args, root, parse=False, ok_codes=(0,)):
    cmd = ["rclone", *args, "--drive-root-folder-id", root]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in ok_codes:
        err = r.stderr.strip()
        if "couldn't fetch token" in err or "didn't find section" in err:
            raise SystemExit(f"rclone is not authorised yet.\nRun once:  rclone config create {REMOTE} drive scope=drive\n"
                             f"and complete the Google sign-in in the browser.\n\nrclone said: {err[:300]}")
        raise SystemExit(f"rclone {' '.join(args[:2])} failed: {err[:600]}")
    return json.loads(r.stdout or "[]") if parse else (r.stdout + r.stderr)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_dirs(root, path=""):
    return rc(["lsjson", f"{REMOTE}:{path}", "--dirs-only"], root, parse=True)


def list_files(root, path):
    return rc(["lsjson", f"{REMOTE}:{path}", "--files-only", "--hash"], root, parse=True)


def find_or_create_dir(root, parent_path, canonical, hint, dry):
    dirs = list_dirs(root, parent_path)
    match = next((d for d in dirs if d["Name"].strip().lower() == canonical.lower()), None) \
        or next((d for d in dirs if hint in d["Name"].strip().lower()), None)
    if match:
        d = match
        return (f"{parent_path}/{d['Name']}" if parent_path else d["Name"]), d["Name"], False
    path = f"{parent_path}/{canonical}" if parent_path else canonical
    if not dry:
        rc(["mkdir", f"{REMOTE}:{path}"], root)
    return path, canonical, True


def ensure_archive(root, folder_path, dry):
    """Return <folder>/archive, creating it if absent and renaming any Archive/archives
    variant to the canonical lowercase 'archive'."""
    for d in list_dirs(root, folder_path):
        name = d["Name"]
        if not name.strip().lower().startswith("archiv"):
            continue
        if name == "archive":
            return f"{folder_path}/archive"
        print(f"    rename: {name}/  ->  archive/")
        if not dry:
            if name.lower() == "archive":  # case-only rename needs a two-step move
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{folder_path}/__archive_tmp__"], root)
                rc(["moveto", f"{REMOTE}:{folder_path}/__archive_tmp__", f"{REMOTE}:{folder_path}/archive"], root)
            else:
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{folder_path}/archive"], root)
        return f"{folder_path}/archive"
    print("    create: archive/")
    if not dry:
        rc(["mkdir", f"{REMOTE}:{folder_path}/archive"], root)
    return f"{folder_path}/archive"


def push_folder(root, folder_path, files, dry):
    """Push files into folder_path. Unchanged files are kept in place; EVERY other
    pre-existing file in the folder (old versions, old names, Google-native docs)
    is moved to <folder>/archive first. Nothing is ever deleted."""
    archive_path = ensure_archive(root, folder_path, dry)
    remote_files = list_files(root, folder_path)
    keep, to_upload = set(), []
    for path in files:
        fn = os.path.basename(path)
        same = next((f for f in remote_files if f["Name"] == fn), None)
        if same and (same.get("Hashes") or {}).get("md5") == md5(path):
            print(f"    unchanged: {fn} — skipped")
            keep.add(fn)
        else:
            to_upload.append(path)
    for f in remote_files:
        name = f["Name"]
        if name in keep:
            continue
        print(f"    archive: {name}  ->  archive/")
        if not dry:
            try:
                rc(["moveto", f"{REMOTE}:{folder_path}/{name}", f"{REMOTE}:{archive_path}/{name}"], root)
            except SystemExit as e:
                print(f"      WARNING: could not archive '{name}' — {str(e)[:200]}; continuing")
    for path in to_upload:
        fn = os.path.basename(path)
        print(f"    upload:  {fn}")
        if not dry:
            rc(["copyto", path, f"{REMOTE}:{folder_path}/{fn}"], root)
            link = rc(["link", f"{REMOTE}:{folder_path}/{fn}"], root).strip()
            print(f"      view link (anyone with the link): {link}")


def push_labs(root, labs_dir, dry):
    folder_path, real_name, created = find_or_create_dir(root, "", "Activities", "activit", dry)
    arch_name = "archive"
    excludes = {arch_name}
    if not created:
        # remember every archiv* variant so a pending (dry-run) rename can't leak
        # the old archive's contents into the sync plan
        excludes |= {d["Name"] for d in list_dirs(root, folder_path)
                     if d["Name"].strip().lower().startswith("archiv")}
        ensure_archive(root, folder_path, dry)
    print(f"  {real_name}{' (will be created)' if created else ''}:  syncing labs/ "
          f"(changed files only; replaced/removed files -> {real_name}/{arch_name}/)")
    args = ["sync", labs_dir, f"{REMOTE}:{folder_path}",
            "--backup-dir", f"{REMOTE}:{folder_path}/{arch_name}",
            "--exclude", ".DS_Store",
            "--checksum", "-v", "--stats-log-level", "NOTICE"]
    for e in excludes:
        args += ["--exclude", f"/{e}/**"]
    if dry:
        args.append("--dry-run")
    out = rc(args, root)
    moved, copied = [], []
    for line in out.splitlines():
        m = re.search(r"(?:INFO|NOTICE)\s*:\s*(.+?):\s*(Copied|Moved|Skipped copy|Skipped move)", line)
        if not m:
            continue
        name, action = m.group(1), m.group(2)
        (copied if "opy" in action or "opied" in action else moved).append(name)
    for name in sorted(set(moved)):
        print(f"    archive: {name}  ->  {arch_name}/")
    for name in sorted(set(copied)):
        print(f"    upload:  {name}")
    print(f"    labs sync: {len(set(copied))} file(s) uploaded, {len(set(moved))} archived "
          f"(unchanged files skipped automatically)")


def newest(pattern):
    hits = sorted(glob.glob(pattern), key=os.path.getmtime)
    return hits[-1] if hits else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    repo = "."
    if "--repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--repo") + 1]
        args = [a for a in args if a != repo]
    if not args:
        raise SystemExit("Usage: gdrive_push.py <drive-folder-link-or-id> [--repo DIR] [--dry-run]\n"
                         "The Google Drive courseware folder link MUST be supplied by the user.")
    m = re.search(r"folders/([A-Za-z0-9_-]{10,})", args[0])
    root = m.group(1) if m else args[0]

    cw = os.path.join(repo, "courseware")
    deck_ppt = newest(os.path.join(cw, "*-v*.pptx"))
    if not deck_ppt:
        raise SystemExit(f"No versioned slide deck found in {cw}")
    deck_pdf = os.path.splitext(deck_ppt)[0] + ".pdf"
    lg_docx = newest(os.path.join(cw, "LG-*.docx")); lg_pdf = newest(os.path.join(cw, "LG-*.pdf"))
    lp_docx = newest(os.path.join(cw, "LP-*.docx")); lp_pdf = newest(os.path.join(cw, "LP-*.pdf"))
    assessments = sorted(glob.glob(os.path.join(repo, "assessment", "*.docx")))

    routing = [
        ("Master Trainer Slides", "master trainer", [deck_ppt, deck_pdf]),
        ("Learner Guide", "learner guide", [lg_docx, lg_pdf, deck_pdf]),
        ("Lesson Plan", "lesson plan", [lp_docx, lp_pdf]),
        ("Assessment", "assess", assessments),
    ]
    print(f"Root folder: {root}{'  (DRY RUN — no changes will be made)' if dry else ''}")
    for canonical, hint, files in routing:
        files = [f for f in files if f and os.path.exists(f)]
        if not files:
            print(f"  {canonical}: no local files found — skipped"); continue
        folder_path, real_name, created = find_or_create_dir(root, "", canonical, hint, dry)
        print(f"  {real_name}{' (will be created)' if created else ''}:")
        push_folder(root, folder_path, files, dry)

    labs_dir = os.path.join(repo, "labs")
    if os.path.isdir(labs_dir):
        push_labs(root, labs_dir, dry)
    else:
        print("  Activities: no labs/ folder found — skipped")
    print("Done." if not dry else "Dry run complete — nothing was modified.")


if __name__ == "__main__":
    main()
