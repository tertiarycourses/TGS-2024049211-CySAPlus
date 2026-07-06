#!/usr/bin/env python3
"""PostToolUse hook: after any courseware generator runs, require a quality review
of the produced PPT/LP/LG via the courseware-qa agent."""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""
GENERATORS = ("make_slides.py", "build_slides.py", "make_lesson_plan.py",
              "build_lesson_plan.py", "make_learner_guide.py", "build_learner_guide.py",
              "build_assessment.py", "build_wsq_assessment.py", "build_courseware.sh")
if any(g in cmd for g in GENERATORS):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "COURSEWARE POST-CHECK (mandatory): courseware was just (re)generated. "
                "Before reporting completion, launch the courseware-qa agent to audit the "
                "regenerated PPT/LP/LG: render the cover, admin slides (front and end) and "
                "changed pages to images and verify the WSQ hard rules (no overlapping/"
                "clipped text; version bumped with version-control record; Trainer x2 "
                "profile cards; Briefing before Assessment; Assessment Flow diagram; TRAQOM "
                "at front and end). Fix any failure and re-run the check."
            ),
        }
    }))
sys.exit(0)
