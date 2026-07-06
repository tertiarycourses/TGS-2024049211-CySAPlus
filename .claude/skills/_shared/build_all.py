#!/usr/bin/env python3
"""Single-command aligned build of all CySA+ courseware from the shared sources.
Runs the slide/LG/LP generators (slides first — it writes the slide-number
manifest the Lesson Plan consumes), then renders PDFs.

PDF rendering: uses LibreOffice (`soffice`) if available, else falls back to
Microsoft Office COM automation (PowerPoint/Word) on Windows.
Requires: python-pptx, python-docx, Pillow. COM path also needs pywin32 + MS Office.
"""
import os, sys, glob, runpy, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths as P

def gen(name):
    print(f"==> {name}")
    runpy.run_path(os.path.join(HERE, name), run_name="__main__")

gen("build_slides.py")   # writes manifest.json (slide numbers)
gen("build_lg.py")
gen("build_lp.py")       # reads manifest.json

def pdfs():
    pptx = glob.glob(os.path.join(P.OUT, "*.pptx"))
    docx = glob.glob(os.path.join(P.OUT, "LG-*.docx")) + glob.glob(os.path.join(P.OUT, "LP-*.docx"))
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        for f in pptx + docx:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", P.OUT, f],
                           check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("==> PDFs rendered via LibreOffice")
        return
    # Fallback: MS Office COM
    import win32com.client as win32
    print("==> PDFs via MS Office COM")
    if pptx:
        pp = win32.DispatchEx("PowerPoint.Application")
        try:
            for f in pptx:
                pr = pp.Presentations.Open(os.path.normpath(f), WithWindow=False)
                pr.SaveAs(os.path.normpath(os.path.splitext(f)[0] + ".pdf"), 32)
                pr.Close()
        finally:
            pp.Quit()
    if docx:
        wd = win32.DispatchEx("Word.Application"); wd.Visible = False
        try:
            for f in docx:
                d = wd.Documents.Open(os.path.normpath(f))
                try:
                    d.Repaginate()
                    for st in d.StoryRanges: st.Fields.Update()
                except Exception: pass
                d.SaveAs(os.path.normpath(os.path.splitext(f)[0] + ".pdf"), FileFormat=17)
                d.Close(False)
        finally:
            wd.Quit()

pdfs()
print("==> Done. Artifacts in", P.OUT)
for f in sorted(glob.glob(os.path.join(P.OUT, "*"))):
    if os.path.isfile(f): print("   ", os.path.basename(f))
