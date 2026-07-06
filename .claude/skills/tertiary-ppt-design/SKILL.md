---
name: tertiary-ppt-design
description: Best-practice design system and rules for building highly professional, visual training/course slide decks with python-pptx (Tertiary Infotech house style). Use whenever creating or polishing a .pptx deck so the result is clean, white-theme, visual, and consistent — large readable fonts, brand colours, icon/card layouts, screenshots and diagrams instead of walls of text. Pair with the tertiary-course-slides skill.
---

# PPT Design & Presentation — Best Practices

Apply these when generating or refining a course/training deck (python-pptx).

## Theme & format
- **16:9** (13.333 × 7.5 in). **All-white slides — never dark/black backgrounds.**
- **Font: Arial** for every run. Brand colours: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`, violet `#7C3AED`, light `#F5F8FC`.
- Cover with the **course title + course & Tertiary Infotech Academy logos + UEN**; footer on every content slide = course/code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## Typography (make it presentable — large fonts)
- Slide **title ≈ 28–30 pt**, kicker label ≈ 14 pt (brand colour, uppercase).
- **Body bullets ≈ 18–20 pt** (never below 16 pt). Two-column body ≈ 17 pt. Card body ≈ 14 pt.
- Section dividers: title ≈ 40 pt, big faint topic number ≈ 72 pt.
- Step slides: one step, big numbered circle + step text ≈ 24 pt.

## Be visual, not wordy
- **≤ 5 bullets per slide**, one idea per bullet. Split dense slides.
- Prefer **layouts over paragraphs**:
  - **3 colour cards** for "features / why / pillars" (heading + 3 short lines each).
  - **Two-column** for comparisons (GET vs POST, model vs memory, in-memory vs Pinecone).
  - **Big-statement** slides (one large sentence) to punctuate sections.
  - **Screenshot slides**: real product screenshots (websites, the n8n canvas) beside short steps.
  - **Diagrams**: redraw concepts in the brand theme (e.g. a RAG flow) — never paste watermarked images.
- Add a **workflow screenshot** for every hands-on activity; a **gallery** for sample student work.

## Structure of a course deck
1. Cover → admin (digital attendance/TRAQOM, trainer, ground rules, lesson plan, learning outcomes, assessment).
2. Per topic: a **section divider**, concept slides (what / why / how, with cards & comparisons), then per activity: **overview → workflow screenshot → one-step-per-slide → green "Test it"**.
3. **Lunch/tea-break** divider slides; recap slides at the end of each day; a Thank-You close.

## Consistency & alignment
- Activity titles and topic numbering must **match the Learner Guide and Lesson Plan exactly**.
- Reuse helper functions (`content`, `two_col`, `cards3`, `website_slide`, `gallery_slide`, `img_slide`, `big_statement`, `section`, `step_slide`) so spacing/fonts stay uniform.

Implementation lives in the **tertiary-course-slides** skill (`make_slides.py`).
