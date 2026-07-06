import os, re, json
import brand
import config as C
import lab_parser as LP
import paths as P

SP = os.path.dirname(os.path.abspath(__file__))
IMG = P.IMAGES
LABS = {L['num']: L for L in LP.load_all(P.LABS)}
OUT_DIR = P.OUT
os.makedirs(OUT_DIR, exist_ok=True)

def sent(text, n=2, cap=260):
    text = LP.md_inline(text)
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    out = ' '.join(parts[:n]).strip()
    return (out[:cap].rsplit(' ',1)[0] + '…') if len(out) > cap else out

D = brand.Deck(C.COURSE_TITLE, C.COURSE_CODE)
manifest = {"domains": [], "labs": {}, "ppt_file": None}

# ---------------- Title ----------------
D.title_slide("Learner Guide · Course Slides", C.COURSE_TITLE,
    [f"WSQ Course Code: {C.COURSE_CODE}",
     f"WSQ TSC: {C.TSC_TITLE} ({C.TSC_CODE})",
     "Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W"],
    f"Version v{C.VERSION_PPT.split('.')[0]}  ·  Learner Guide Slides")

# ---------------- Course Administration ----------------
D.section_slide("Course Administration", "Welcome & Housekeeping")
D.content_slide("TRAQOM · SSG Digital Attendance", "Digital Attendance (Mandatory)", [
    ("It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.", 0),
    ("The trainer/administrator will display the digital attendance QR code generated from the SSG portal.", 0),
    ("Scan the QR code with your mobile phone camera and submit your attendance.", 0),
    ("A minimum of 75% attendance is required to be eligible for assessment and funding.", 0),
])
D.content_slide("Icebreaker", "Let's Know Each Other", [
    ("Your name and organisation / role", 0),
    ("Your experience with security operations and SOC tools", 0),
    ("What you want to get out of this CySA+ course", 0),
    ("One security incident or tool you are curious about", 0),
])
D.cards_slide("Housekeeping", "Ground Rules", [
    (1, "Set your mobile phone to silent mode."),
    (2, "Participate actively — no question is too small."),
    (3, "Mutual respect: agree to disagree."),
    (4, "One conversation at a time."),
    (5, "Be punctual; return from breaks on time."),
    (6, "75% attendance is required."),
])
# Lesson plan overview (per day)
day_topics = [
    ("Day 1", ["Digital Attendance (AM)", "Trainer & Learner Introduction", "Learning Outcomes & Course Outline",
               "Topic 1: Security Operations (Labs 1–10)", "Lunch Break", "Digital Attendance (PM)", "End of Day 1"]),
    ("Day 2", ["Digital Attendance (AM)", "Topic 2: Vulnerability Management (Labs 11–19)", "Lunch Break",
               "Digital Attendance (PM)", "Topic 2 continued", "End of Day 2"]),
    ("Day 3", ["Digital Attendance (AM)", "Topic 3: Incident Response & Management (Labs 20–25)", "Lunch Break",
               "Digital Attendance (PM)", "Topic 3 continued", "End of Day 3"]),
    ("Day 4", ["Digital Attendance (AM)", "Topic 4: Reporting & Communication (Labs 26–30)", "Lunch Break",
               "Digital Attendance (PM)", "Topic 4 continued", "End of Day 4"]),
    ("Day 5", ["Digital Attendance (AM)", "Revision", "Lunch Break", "Digital Attendance (PM)",
               "Course Feedback & TRAQOM Survey", "Digital Attendance (Assessment)", "Final Assessment", "End of Class"]),
]
for day, items in day_topics:
    D.content_slide("Lesson Plan", day, [(x, 0) for x in items])

# Skills framework
D.content_slide("Skills Framework", f"WSQ TSC: {C.TSC_TITLE}", [
    (f"TSC Title: {C.TSC_TITLE}", 0, True),
    (f"TSC Code: {C.TSC_CODE}", 0, True),
    ("This course is aligned to the SkillsFuture Singapore (SSG) Skills Framework Technical Skills & Competency (TSC) above.", 0),
])
D.content_slide("Skills Framework", "TSC Knowledge (K)", [(k, 0) for k in C.TSC_KNOWLEDGE])
D.content_slide("Skills Framework", "TSC Abilities (A)", [(a, 0) for a in C.TSC_ABILITIES])
D.content_slide("Outcomes", "Learning Outcomes",
    [("By the end of the course, learners will be able to:", 0, True)] + [(lo, 0) for lo in C.LEARNING_OUTCOMES])
# Course outline
for dom in C.DOMAINS:
    D.content_slide("Course Outline", f"{dom['topic']}: {dom['name']} ({dom['weight']}%)",
                    [(c, 0) for c in dom['concepts']])
D.content_slide("Assessment", "Final Assessment", [
    ("Written Assessment (SAQ) — 1 hour", 0),
    ("Case Study (CS) — 1 hour", 0),
    ("Assessment format: Open Book", 0, True),
    ("Open book assessment ONLY includes Slides, Learner Guide or any approved materials.", 1),
    ("An appeal process is available for learners assessed as Not Yet Competent.", 0),
])
D.content_slide("Assessment", "Briefing for Assessment", [
    ("Place phones and other materials under the table or on the floor.", 0),
    ("No photos or recording of assessment scripts.", 0),
    ("No discussion during assessment.", 0),
    ("Use black/blue pen for assessment (hard copies). No liquid paper or correction tape.", 0),
    ("Assessment scripts will be collected when the time is up.", 0),
])
D.content_slide("Funding", "Criteria for Funding", [
    ("Minimum attendance rate of 75% based on SSG Digital Attendance record.", 0),
    ("Complete the assessment and be assessed as 'Competent'.", 0),
])
D.content_slide("Systems", "LMS / TMS", [
    ("Access your Learning & Training Management System for materials, attendance and certificates:", 0),
    ("https://lms-tms.tertiaryinfotech.com", 0, True, brand.BLUE),
])

# ---------------- Topics + Labs ----------------
def cysa_map(intro_text):
    m = re.search(r'\(CySA\+\s*([^)]*)\)', intro_text)
    return m.group(1).strip() if m else ''

for di, dom in enumerate(C.DOMAINS, 1):
    eyebrow = f"{dom['topic']} · {dom['name']}"
    ssec = D.section_slide(f"{dom['topic']} · {dom['weight']}% of CS0-003", dom['name'])
    ov = [(f"CompTIA CySA+ CS0-003 exam weighting: {dom['weight']}%", 0, True, brand.BLUE)] + \
         [(c, 0) for c in dom['concepts']] + \
         [(f"Hands-on Labs {dom['labs'][0]}–{dom['labs'][-1]} ({len(dom['labs'])} labs)", 0, True, brand.BLUE)]
    D.content_slide(eyebrow, f"{dom['topic']} Overview", ov)
    manifest["domains"].append({"topic": dom['topic'], "name": dom['name'], "weight": dom['weight'],
                                "section_slide": ssec, "labs": dom['labs']})
    for ln in dom['labs']:
        L = LABS[ln]
        tail = L['title'].split('—',1)[-1].strip() if '—' in L['title'] else L['title']
        intro = next((b[1] for b in L['intro'] if b[0]=='text'), '')
        cm = cysa_map(intro)
        objb = [("Objective", 0, True, brand.BLUE),
                (sent(re.sub(r'\s*\(CySA\+[^)]*\)','',intro), 3, 320), 1),
                (f"Environment: {C.ENV[ln]}", 0, True)]
        if cm:
            objb.append((f"CySA+ mapping: {cm}", 0, False, brand.GREY))
        labslide = D.content_slide(eyebrow, f"Lab {ln} — {tail}", objb)
        manifest["labs"][ln] = {"title": L['title'], "slide": labslide}
        # diagram
        if ln in C.DIAGRAMS:
            D.diagram_slide(eyebrow, f"Lab {ln} — Reference Diagram",
                            [os.path.join(IMG, f) for f in C.DIAGRAMS[ln]])
        # steps
        steps = LP.get_steps(L)
        CH = 5
        for i in range(0, len(steps), CH):
            grp = steps[i:i+CH]
            sd = []
            for st in grp:
                htail = re.sub(r'^Step\s*\d+\s*[—-]\s*','', st['heading'])
                snum = re.match(r'^Step\s*(\d+)', st['heading'])
                label = f"Step {snum.group(1)}: {htail}" if snum else htail
                desc=''; code=''; clang=''
                for b in st['blocks']:
                    if b[0]=='text' and not desc: desc = sent(b[1],1,150)
                    if b[0]=='code' and not code:
                        code = b[1].strip().split('\n')[0][:78]; clang = b[2] if len(b)>2 else ''
                if code:
                    is_shell = clang in ('bash','sh','shell','console','') and not code.lstrip().startswith(('#','*','-','1.','**'))
                    code = ("$ " if is_shell else "") + LP.md_inline(code)
                sd.append({"label": LP.md_inline(label), "desc": desc, "code": code})
            part = " (cont'd)" if i>0 else ""
            D.steps_slide(eyebrow, f"Lab {ln} — Hands-On Steps{part}", sd)
        # outcomes
        wyl = LP.get_outcomes(L)
        ob = [("By completing this lab you can:", 0, True, brand.BLUE)]
        if wyl:
            for b in wyl['blocks']:
                if b[0] in ('bullets','numbered'):
                    for it in b[1]: ob.append((LP.md_inline(it), 0))
                elif b[0]=='text':
                    ob.append((sent(b[1],2,200), 0))
        D.content_slide(eyebrow, f"Lab {ln} — What You Learned", ob)

# ---------------- Back admin ----------------
D.content_slide("Practice", "Practice Exams", [
    ("Access the Practice Exams from the Google Classroom.", 0),
    ("Work through the practice questions to reinforce each domain before the final assessment.", 0),
])
D.section_slide("Wrap-Up", "Summary & Q&A")
D.content_slide("Feedback", "Cert & TRAQOM Survey (Mandatory)", [
    ("Complete the mandatory TRAQOM survey and claim your certificate via the LMS/TMS:", 0),
    ("https://lms-tms.tertiaryinfotech.com", 0, True, brand.BLUE),
])
D.content_slide("TRAQOM · SSG Digital Attendance", "Digital Attendance (Mandatory)", [
    ("It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.", 0),
    ("Scan the QR code shown by your trainer/administrator and submit your attendance.", 0),
])
D.section_slide("Assessment", "Final Assessment")
D.cards_slide("What's Next", "Recommended Courses", [
    (None, "WSQ – CompTIA Certified Server+ Training"),
    (None, "WSQ – CompTIA Certified A+ Training (Core 1 & Core 2)"),
    (None, "WSQ – CompTIA Certified Linux+ Training"),
    (None, "WSQ – CompTIA PenTest+ Training"),
    (None, "WSQ – CompTIA Certified Security+ Training"),
    (None, "WSQ – CompTIA CySA+ (Refresher)"),
])
D.content_slide("Support", "Support", [
    ("If you have any enquiries during and after the class, you can contact us below:", 0),
    (f"Email: {C.CONTACT['email']}", 0, True),
    (f"Tel: {C.CONTACT['tel']}", 0, True),
    (f"Website: {C.CONTACT['web']}", 0, True),
])
D.closing_slide("Thank You!", ["Tertiary Infotech Academy Pte Ltd",
                                f"{C.CONTACT['web']}  ·  {C.CONTACT['email']}  ·  {C.CONTACT['tel']}"])

out_name = f"{C.COURSE_TITLE}-v{C.VERSION_PPT.split('.')[0]}.pptx"
D.save(os.path.join(OUT_DIR, out_name))
manifest["ppt_file"] = out_name
manifest["total_slides"] = D.page
with open(P.MANIFEST, "w") as f:
    json.dump(manifest, f, indent=2)
print("Saved:", out_name, "| slides:", D.page)
print("Domains:", [(d['topic'], d['section_slide']) for d in manifest['domains']])
print("Lab1 slide:", manifest['labs'][1], "Lab30:", manifest['labs'][30])
