"""Parse CySA+ lab markdown files into structured data."""
import os, re, glob

DOMAINS = [
    ("Security Operations", 33, list(range(1, 11))),
    ("Vulnerability Management", 30, list(range(11, 20))),
    ("Incident Response and Management", 20, list(range(20, 26))),
    ("Reporting and Communication", 17, list(range(26, 31))),
]

def _lab_num(path):
    m = re.search(r'lab-(\d+)', os.path.basename(path))
    return int(m.group(1)) if m else 999

def parse_lab(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    # normalise dashes
    lines = raw.split('\n')
    title = ''
    # find first H1
    for ln in lines:
        if ln.startswith('# '):
            title = ln[2:].strip()
            break
    # split into sections by H2
    sections = []  # list of dict(heading, blocks)
    intro_blocks = []
    cur_heading = None
    cur_blocks = []
    i = 0
    def flush():
        nonlocal cur_heading, cur_blocks
        if cur_heading is None:
            for b in cur_blocks:
                intro_blocks.append(b)
        else:
            sections.append({'heading': cur_heading, 'blocks': cur_blocks})
        cur_blocks = []
    # tokenise
    buf_para = []
    def flush_para():
        nonlocal buf_para
        txt = ' '.join(x.strip() for x in buf_para).strip()
        if txt:
            cur_blocks.append(('text', txt))
        buf_para = []
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('# '):
            i += 1; continue
        if ln.strip() == '---':
            flush_para(); i += 1; continue
        if ln.startswith('## '):
            flush_para(); flush()
            cur_heading = ln[3:].strip()
            i += 1; continue
        if ln.startswith('### '):
            flush_para()
            cur_blocks.append(('subhead', ln[4:].strip()))
            i += 1; continue
        # code fence
        if ln.lstrip().startswith('```'):
            flush_para()
            lang = ln.lstrip()[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].lstrip().startswith('```'):
                code.append(lines[i]); i += 1
            i += 1  # skip closing fence
            cur_blocks.append(('code', '\n'.join(code), lang))
            continue
        # bullet list
        if re.match(r'^\s*[-*] ', ln):
            flush_para()
            items = []
            while i < len(lines) and re.match(r'^\s*[-*] ', lines[i]):
                items.append(re.sub(r'^\s*[-*] ', '', lines[i]).strip())
                i += 1
            cur_blocks.append(('bullets', items))
            continue
        if re.match(r'^\s*\d+\. ', ln):
            flush_para()
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\. ', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s*', '', lines[i]).strip())
                i += 1
            cur_blocks.append(('numbered', items))
            continue
        # table row -> keep as text-ish (rare)
        if ln.strip():
            buf_para.append(ln)
            i += 1; continue
        else:
            flush_para(); i += 1; continue
    flush_para(); flush()
    return {'num': _lab_num(path), 'title': title, 'intro': intro_blocks, 'sections': sections, 'path': path}

def load_all(labs_dir):
    files = sorted(glob.glob(os.path.join(labs_dir, 'lab-*.md')), key=_lab_num)
    return [parse_lab(f) for f in files]

def md_inline(s):
    """Strip inline markdown emphasis/code/links for plain rendering."""
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', s)
    s = s.replace('**', '').replace('__', '')
    s = s.replace('`', '')
    s = s.replace('‑', '-')
    return s

def get_steps(L):
    return [s for s in L['sections'] if s['heading'].lower().startswith('step')]

def get_outcomes(L):
    for s in L['sections']:
        if s['heading'].lower().strip().startswith('what you learned'):
            return s
    return None

if __name__ == '__main__':
    import sys
    labs = load_all(sys.argv[1])
    for L in labs:
        steps = [s['heading'] for s in L['sections'] if s['heading'].lower().startswith('step')]
        wyl = [s for s in L['sections'] if 'learn' in s['heading'].lower()]
        ncode = sum(1 for s in L['sections'] for b in s['blocks'] if b[0]=='code')
        print(f"Lab {L['num']:2d}: {L['title'][:55]:55s} | sections={len(L['sections']):2d} steps={len(steps):2d} code={ncode:2d} | headings={[s['heading'][:18] for s in L['sections']]}")
