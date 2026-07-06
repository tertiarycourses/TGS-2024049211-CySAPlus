import os
HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.join(HERE, "labs")
IMAGES = os.path.join(HERE, "images")
ASSETS = os.path.join(HERE, "assets")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))   # .claude/skills/_shared -> repo root
OUT = os.path.join(REPO, "courseware")
MANIFEST = os.path.join(HERE, "manifest.json")
os.makedirs(OUT, exist_ok=True)
