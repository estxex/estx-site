#!/usr/bin/env python3
"""Split the ESTX Utility Token Whitepaper PDF into EN/DE paragraphs per section.

  python3 li-src/parse_wp.py ESTX_Whitepaper_v2.0_2026-09.pdf   -> li-src/wp-sections.json

The estx.li page takes its texts from this file, so they stay word-for-word identical to the
whitepaper (MiCA: marketing material must be consistent with the white paper).
Needs pdftotext (poppler).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
pdf = sys.argv[1]
raw = subprocess.check_output(["pdftotext", "-layout", pdf, "-"]).decode("utf-8")
lines = [l for l in raw.split("\n")
         if "ESTX Utility Token Whitepaper · Version" not in l and not re.fullmatch(r"\s*\d{1,2}\s*", l.replace("\f", ""))]
lines = [l.replace("\f", "") for l in lines]

head_re = re.compile(r"^ ?(\d{1,2}(?:\.\d{1,2})?)\.? (.+)$")
secs, cur, lang = [], None, None
for l in lines:
    s = l.strip()
    if s == "E N · E n g l i sh":
        lang = "en"; continue
    if s == "D E · D e u t s ch":
        lang = "de"; continue
    m = head_re.match(l)
    if m and not l.startswith("   ") and len(s) < 140 and ("/" in m.group(2) or m.group(2).strip() in ("Roadmap", "Management & Governance")):
        if "...." in s:          # table of contents line
            continue
        cur = {"id": m.group(1), "title": m.group(2).strip(), "en": [], "de": []}
        secs.append(cur); lang = None; continue
    if cur is not None and lang:
        cur[lang].append(s)

KEEP_SPACE = {"und", "oder", "and", "or", "sowie"}


def paras(ls):
    out, p = [], ""
    for s in ls + [""]:
        if not s:
            if p:
                out.append(p)
            p = ""; continue
        if s.startswith("•") and p and not p.startswith("•"):   # a list right after a lead-in line
            out.append(p); p = ""
        if p.endswith("-") and re.search(r"\w-$", p[-3:] if len(p) > 2 else p) or p.endswith(" -"):
            first = s.split(" ", 1)[0]
            p = p + (" " if first in KEEP_SPACE else "") + s      # re-join a word split at the line end
        else:
            p = (p + " " + s) if p else s
    return out


res = [{"id": c["id"], "title": c["title"], "en": paras(c["en"]), "de": paras(c["de"])} for c in secs]
json.dump(res, open(os.path.join(HERE, "wp-sections.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(res), "sections ->", os.path.join(HERE, "wp-sections.json"))
