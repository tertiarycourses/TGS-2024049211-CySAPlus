---
name: wsq-assessment
description: Generate WSQ course assessments as professionally formatted Word documents (.docx) — a Written Assessment (WA) that tests KNOWLEDGE and a practical instrument that tests PRACTICAL ability, each as a question paper PLUS a model-answer / marking guide. Two builders are provided. build_assessment.py produces WA (SAQ) + PP (Practical Performance): the WA is open-ended short-answer knowledge questions drawn from the course slides, and the PP is activity-based practical tasks (LO1..LOn) whose model answers are the in-class lab build steps; both carry the WSQ house COVER PAGE (same as the Lesson Plan / Learner Guide — course title + logos + UEN); assessments have the cover page only (no version-control record). build_wsq_assessment.py is the alternate WA + Case Study (CS) variant. ALL questions are OPEN-ENDED (no multiple choice). Use when creating or revising assessments, written/practical/case-study questions, answer keys, or marking guides for a WSQ course.
---

# WSQ Assessment → DOCX (Written + Practical/Case-Study)

Generate two WSQ assessment instruments, each as a **question paper** and a matching **model-answer / marking guide** (four DOCX total). Pick the builder that matches the course's assessment design:

| Builder | Instruments | Best for |
|---------|-------------|----------|
| **`build_assessment.py`** (primary) | **WA (SAQ)** knowledge + **PP (Practical Performance)** activity tasks | Hands-on courses where the practical is graded on tasks the learner built in class (e.g. the n8n / Tertiary courses). Carries the **WSQ house cover page** (course title + Tertiary & course logos + UEN), identical to the Lesson Plan / Learner Guide — cover page only, no version-control record. |
| **`build_wsq_assessment.py`** (alternate) | **WA** knowledge + **CS (Case Study)** one coherent scenario | Courses assessed via a single written case study rather than discrete practical tasks. |

## Hard rules (do not break)
- **NO multiple choice. Every question is OPEN-ENDED.** Short-answer with a ruled/boxed answer space; never emit a)/b)/c)/d) options.
- **The Written Assessment (WA) tests KNOWLEDGE.** Every question must be answerable from the course **slides / modules**. Tag each with a knowledge code (K1, K2, …) and cite the source in the answer key.
- **The practical instrument tests PRACTICAL ability.** For **PP**, each task maps to a learning outcome (LO1, LO2, …) and to an **activity the learner did in class**; the model answer **is the lab build steps** (name the exact triggers/actions and cite the activity). For **CS**, use **one coherent scenario** built from the in-class activities.
- **Everything is "covered in class."** Do not test content that is not in the slides or labs.
- **Keep the question/task count stable** when revising an existing assessment — update the wording and answers, don't change the count, unless asked.

## How to use `build_assessment.py` (WA + PP)
The script lives **in this skill** and runs **in place** — do NOT copy it into the course repo. It auto-detects the course repo root by walking up from its own location to the nearest dir containing a `.git` folder (or both `courseware/` and `assessment/`), and writes the four DOCX into `<repo>/assessment/`. Override with `REPO=/path/to/course` if needed.

1. Ensure the sibling **tertiary-lesson-plan** skill is installed — the script reuses its **`prodoc.py`** for the cover page + version control + page numbers (the import auto-falls-back from the project `.claude/skills/` to `~/.claude/skills/`).
2. Edit the **CONFIG** block: `TITLE`, `Q_VER`/`A_VER` (single standardised version string, e.g. `"v5"`), `ORG_LOGO`, `COURSE_LOGO`.
3. Fill the two content lists **from the course materials**:
   - `WRITTEN` — `(criterion, context, question, [model-answer points])`. Read the concept slides and turn each key concept into one open-ended knowledge question. Keep it to the concepts actually taught.
   - `SCENARIO` + `PRACTICAL` — one continuous scenario, then `(label, criterion, task_prompt, box_caption, [model build-step points])` per task. Each task maps to one LO and to a class activity; the model points **are** the lab procedure (cite the activity numbers).
4. Run it in place — from the project copy of the skill:
   `python3 .claude/skills/wsq-assessment/build_assessment.py`
   (or `REPO=/path/to/course python3 ~/.claude/skills/wsq-assessment/build_assessment.py`). It writes into `<repo>/assessment/`:
   `WA (SAQ) - <Title> - <VER>.docx`, `Answer to WA (SAQ) - <Title> - <VER>.docx`,
   `PP Assessment - <Title> - <VER>.docx`, `Answer to PP Assessment - <Title> - <VER>.docx`.
5. Assessments are delivered as **DOCX only** — do not generate PDFs for the assessment set.
6. Keep the question paper and its answer key on the **same version string** (e.g. both `v5`) to avoid confusion.

## Document format (WSQ house style)
- **Cover page** — same as the Lesson Plan / Learner Guide (Tertiary Infotech Academy logo, UEN, instrument name, "For", course logo, course title, TGS ref, "Conducted by", version). Cover page only — assessments do **not** include a Document Version Control Record.
- **Question paper** — centred title block; **A: Trainee Information** (name, last 3 NRIC digits + alphabet, date); **B: Instructions to Candidate**; **C:** the questions/tasks with **boxed answer space**; and a **For Official Use Only** block (Grade C / NYC, assessor name/NRIC/date/signature).
- **Answer document** — the model answers / marking guide: each question/task with "Suggestive answers (not exhaustive):" bullet points (WA cites the slide/module; PP lists the lab build steps and cites the activities).
- Body is **Arial 11**; every page has the copyright + page-number footer.

## Criterion tagging
- Written knowledge items → `K1, K2, …`.
- Practical/case-study tasks → `LO1, LO2, …` (or `A1, A2, …`). Keep the same numbering across the question paper and its answer key.

## Quality checklist before saving
- [ ] Zero multiple-choice questions anywhere.
- [ ] Every WA question traces to a slide/module; every PP/CS answer traces to a class activity/lab.
- [ ] One coherent PP scenario (not disconnected mini-cases).
- [ ] Cover page present (no version-control record); question paper has Trainee Information, Instructions, boxed answers, and For Official Use Only.
- [ ] Answer-key wording is guidance ("award the mark where the candidate covers…"), not a rigid script.
- [ ] Old/mismatched assessment files (previous versions, other courses) removed from the output folder.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.
