#!/usr/bin/env python3
"""Windows-friendly entry point: build all courseware then render PDFs
(via MS Office COM if LibreOffice is unavailable)."""
import os, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(HERE, "..", "_shared", "build_all.py"), run_name="__main__")
