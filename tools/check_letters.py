"""Independent letters-and-digits check of the Lei Orgânica against its PDF, read with a second PDF reader (poppler's
pdftotext, not the builder's PyMuPDF) and none of the builder's code.

    python -X utf8 check_letters.py corpus.d/10-lei-organica.json

The pdftotext text in content-stream order (-raw), page by page: lines seen among the first six or last four lines of most pages (at least three) (digits
counted as the same), lines that are only a page number and rule lines are removed; the text runs from the first line
matching the start pattern after the "after" pattern to the last line matching the end pattern. A provision carrying
a note that it was declared unconstitutional is removed from its label line to the note; the edition's notes in
parentheses are removed. Reduced to letters and digits, it must equal the unit files reduced the same way, each unit
found at its place in document order. The patterns are read from parse.py's CONFIG line (data, not code).
"""
import ast, hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABEL = re.compile(r'^\s*(?:Art(?:igo)?\.?\s*[0-9]|§|Par[áa]grafo|[IVXLC]+\s*[-–.)]|[a-z]\))')


def config():
    for line in (HERE / 'parse.py').read_text(encoding='utf-8').splitlines():
        if line.startswith('CONFIG = '):
            return ast.literal_eval(line[len('CONFIG = '):])
    raise SystemExit('no CONFIG line in parse.py')


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def clean(s):
    return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()


def source_text(path, cfg):
    out = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', str(path), '-'], capture_output=True, check=True).stdout
    pages = [[clean(l) for l in pg.split('\n') if clean(l)] for pg in out.decode('utf-8').split('\f')]
    count = {}
    for p in pages:
        for l in set(p[:6] + p[-4:]):
            k = re.sub(r'[0-9]', '#', l)
            count[k] = count.get(k, 0) + 1
    rep = {k for k, c in count.items() if c >= max(3, len(pages) // 2)}
    lines = [l for p in pages for l in p if re.sub(r'[0-9]', '#', l) not in rep
             and not re.fullmatch(r'(?i)(?:p[áa]g(?:ina)?\.?\s*)?[0-9]{1,3}(?:\s*(?:/|de)\s*[0-9]{1,3})?|_{5,}', l)]
    after = next(i for i, l in enumerate(lines) if re.search(cfg['after'], l))
    a = next(i for i, l in enumerate(lines) if i >= after and re.search(cfg['start'], l))
    b = max(i for i, l in enumerate(lines) if i > a and re.search(cfg['end'], l))
    lines = lines[a:b + 1]
    if cfg.get('void'):
        while True:
            text = '\n'.join(lines)
            m = re.search(cfg['void'], text, re.I)
            if not m:
                break
            first = text.count('\n', 0, m.start())
            last = text.count('\n', 0, m.end())
            k = first
            while k > 0 and not LABEL.match(lines[k]):
                k -= 1
            rest = text[m.end():].split('\n', 1)[0]
            lines = lines[:k] + ([rest] if rest.strip() else []) + lines[last + 1:]
    text = '\n'.join(lines)
    if cfg.get('note'):
        text = re.sub(cfg['note'], ' ', text, flags=re.I)
    return text


def main(paths):
    cfg = config()
    bad = total = 0
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            for v in a['versions']:
                path = HERE / '.cache' / 'sapl' / 'raw' / hashlib.sha256(v['source_url'].encode()).hexdigest()
                assert hashlib.sha256(path.read_bytes()).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                src = ld(source_text(path, cfg))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                total += 1
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('10-*.json'))) else 0)
