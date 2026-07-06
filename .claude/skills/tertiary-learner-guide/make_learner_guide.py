#!/usr/bin/env python3
"""Course-specific launcher — builds this course's artifact via the shared
CySA+ generators in .claude/skills/_shared. Edit course content in
_shared/config.py and the lab sources in _shared/labs/."""
import os, sys, runpy
SHARED = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "_shared"))
sys.path.insert(0, SHARED)
runpy.run_path(os.path.join(SHARED, "build_lg.py"), run_name="__main__")
