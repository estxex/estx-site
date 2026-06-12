#!/usr/bin/env python3
"""Generate styled legal pages (terms.html, risk-disclosure.html) from the
plain-text extractions of the source ODT documents. Re-run after the legal
texts change:  python3 build-legal.py /tmp/terms.txt /tmp/risk.txt
"""
import html
import re
import sys

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="robots" content="index, follow"/>
<title>{title} — ESTX.Exchange</title>
<meta name="description" content="{title} for ESTX.Exchange — the regulated venue where crypto starts to trade."/>
<link rel="icon" href="brand_assets/favicon.png" type="image/png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
  :root {{
    --ink: #0a1628;
    --body: #475569;
    --muted: #64748b;
    --gold: #F78F27;
    --paper: #f8faff;
    --line: #e8edf8;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; scroll-padding-top: 90px; }}
  body {{ font-family: 'DM Sans', sans-serif; background: var(--paper); color: var(--body); }}

  .topbar {{
    position: sticky; top: 0; z-index: 50;
    background: rgba(248,250,255,0.92); backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--line);
  }}
  .topbar-inner {{
    max-width: 1080px; margin: 0 auto; padding: 16px 24px;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .back-link {{
    font-size: 0.84rem; font-weight: 600; color: var(--muted); text-decoration: none;
    display: inline-flex; align-items: center; gap: 7px; transition: color .15s;
  }}
  .back-link:hover {{ color: var(--ink); }}

  .doc-head {{
    max-width: 760px; margin: 0 auto; padding: 72px 24px 0;
  }}
  .eyebrow {{
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 18px;
  }}
  .eyebrow::before {{
    content: ''; display: inline-block; width: 26px; height: 2px; background: var(--gold);
    vertical-align: middle; margin-right: 10px;
  }}
  h1 {{
    font-family: 'Outfit', sans-serif; font-weight: 800; color: var(--ink);
    font-size: clamp(2rem, 5vw, 2.9rem); line-height: 1.12; letter-spacing: -0.02em;
    margin-bottom: 14px;
  }}
  .updated {{ font-size: 0.86rem; color: var(--muted); margin-bottom: 36px; }}
  .updated strong {{ color: var(--ink); font-weight: 600; }}

  .intro {{
    border-left: 3px solid var(--gold);
    background: #fff; border-radius: 0 12px 12px 0;
    padding: 24px 28px; margin-bottom: 44px;
    box-shadow: 0 1px 3px rgba(10,22,40,0.05);
  }}
  .intro p {{ font-size: 0.96rem; line-height: 1.7; }}
  .intro p + p {{ margin-top: 12px; }}

  .toc {{
    max-width: 760px; margin: 0 auto 56px; padding: 0 24px;
  }}
  .toc-box {{
    background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 26px 30px;
  }}
  .toc-title {{
    font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.78rem;
    letter-spacing: 0.16em; text-transform: uppercase; color: var(--ink); margin-bottom: 16px;
  }}
  .toc ol {{
    columns: 2; column-gap: 40px; list-style: none; counter-reset: toc;
  }}
  .toc li {{ counter-increment: toc; margin-bottom: 8px; break-inside: avoid; }}
  .toc a {{
    font-size: 0.86rem; color: var(--body); text-decoration: none; line-height: 1.45;
    display: inline-block; transition: color .15s;
  }}
  .toc a::before {{
    content: counter(toc, decimal-leading-zero); font-family: 'Outfit', sans-serif;
    font-weight: 700; font-size: 0.72rem; color: var(--gold); margin-right: 9px;
  }}
  .toc a:hover {{ color: var(--ink); }}
  @media (max-width: 640px) {{ .toc ol {{ columns: 1; }} }}

  main {{ max-width: 760px; margin: 0 auto; padding: 0 24px 90px; }}
  section {{ margin-bottom: 48px; }}
  h2 {{
    font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--ink);
    font-size: 1.32rem; letter-spacing: -0.01em; line-height: 1.3;
    margin-bottom: 16px; padding-top: 10px;
  }}
  h2 .num {{ color: var(--gold); margin-right: 10px; font-weight: 800; }}
  h3 {{
    font-family: 'Outfit', sans-serif; font-weight: 600; color: var(--ink);
    font-size: 1.02rem; margin: 22px 0 10px;
  }}
  h3 .num {{ color: var(--gold); margin-right: 8px; font-weight: 700; }}
  p {{ font-size: 0.95rem; line-height: 1.75; margin-bottom: 13px; }}
  ul {{ margin: 0 0 16px 4px; list-style: none; }}
  li {{
    font-size: 0.95rem; line-height: 1.7; margin-bottom: 7px; padding-left: 22px; position: relative;
  }}
  li::before {{
    content: ''; position: absolute; left: 0; top: 0.62em;
    width: 7px; height: 7px; border-radius: 2px;
    background: linear-gradient(135deg, var(--gold), #FFA94D);
  }}
  .address {{ font-style: normal; }}
  .address p {{ margin-bottom: 2px; font-weight: 500; color: var(--ink); }}

  .crossref {{
    margin: 64px auto 0; max-width: 760px; padding: 0 24px;
  }}
  .crossref-box {{
    border: 1px solid var(--line); background: #fff; border-radius: 14px;
    padding: 22px 28px; display: flex; align-items: center; justify-content: space-between; gap: 16px;
    flex-wrap: wrap;
  }}
  .crossref-box span {{ font-size: 0.9rem; color: var(--muted); }}
  .crossref-box a {{
    font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 0.9rem;
    color: var(--gold); text-decoration: none;
  }}
  .crossref-box a:hover {{ text-decoration: underline; }}

  footer {{
    background: var(--ink); margin-top: 80px; padding: 30px 24px;
  }}
  .footer-inner {{
    max-width: 1080px; margin: 0 auto;
    display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap;
  }}
  footer .copy {{ font-size: 0.8rem; color: rgba(255,255,255,0.4); }}
  footer nav {{ display: flex; gap: 22px; }}
  footer nav a {{
    font-size: 0.8rem; color: rgba(255,255,255,0.55); text-decoration: none; transition: color .15s;
  }}
  footer nav a:hover {{ color: #fff; }}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-inner">
    <a href="index.html"><img src="brand_assets/logo.svg" alt="ESTX" style="height:30px;width:auto;display:block;"/></a>
    <a class="back-link" href="index.html">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
      Back to ESTX.Exchange
    </a>
  </div>
</div>

<header class="doc-head">
  <div class="eyebrow">Legal</div>
  <h1>{title}</h1>
  <p class="updated">Last updated: <strong>{updated}</strong></p>
  <div class="intro">
{intro}
  </div>
</header>

<nav class="toc" aria-label="Table of contents">
  <div class="toc-box">
    <div class="toc-title">Contents</div>
    <ol>
{toc}
    </ol>
  </div>
</nav>

<main>
{body}
</main>

<div class="crossref">
  <div class="crossref-box">
    <span>{cross_label}</span>
    <a href="{cross_href}">{cross_title} &rarr;</a>
  </div>
</div>

<footer>
  <div class="footer-inner">
    <div class="copy">&copy; 2026 ESTX.Exchange &middot; ESTX Venture GmbH, Vaduz, Liechtenstein</div>
    <nav>
      <a href="index.html">Home</a>
      <a href="terms.html">Terms of Use</a>
      <a href="privacy.html">Privacy Policy</a>
      <a href="risk-disclosure.html">Risk Disclosure</a>
      <a href="https://trade.estx.exchange" target="_blank" rel="noopener">Trade</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""

H2_RE = re.compile(r"^(\d+)\.\s+(.*)")
H3_RE = re.compile(r"^(\d+\.\d+)\s+(.*)")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build(lines, *, title, updated, intro_count, skip_head, cross_label, cross_href, cross_title, drop_lines=()):
    lines = [l for l in lines if l.strip() and l.strip() not in drop_lines]
    lines = lines[skip_head:]
    intro, rest = lines[:intro_count], lines[intro_count:]

    toc_items, sections = [], []
    cur = None  # {'num','title','id','blocks'}
    list_buf = []
    in_contact = False

    def flush_list(blocks):
        nonlocal list_buf
        if list_buf:
            blocks.append("<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in list_buf) + "</ul>")
            list_buf = []

    for line in rest:
        m2, m3 = H2_RE.match(line), H3_RE.match(line)
        if m3:
            flush_list(cur["blocks"])
            cur["blocks"].append(
                f'<h3><span class="num">{m3.group(1)}</span>{html.escape(m3.group(2))}</h3>'
            )
            continue
        if m2:
            if cur:
                flush_list(cur["blocks"])
                sections.append(cur)
            num, heading = m2.group(1), m2.group(2)
            cur = {"num": num, "title": heading, "id": slug(heading), "blocks": []}
            toc_items.append((cur["id"], heading))
            in_contact = heading.strip().lower() in ("contact", "data controller")
            continue
        # Body line classification: trailing ';' or no terminal punctuation → bullet,
        # except inside the Contact section (address lines render as paragraphs).
        is_bullet = (line.endswith(";") or not re.search(r"[.:;?]$", line)) and not in_contact
        if is_bullet:
            list_buf.append(line.rstrip(";"))
        else:
            flush_list(cur["blocks"])
            cls = ' class="address"' if in_contact and not re.search(r"[.:;?]$", line) else ""
            cur["blocks"].append(f"<p{cls}>{html.escape(line)}</p>")
    if cur:
        flush_list(cur["blocks"])
        sections.append(cur)

    toc_html = "\n".join(f'      <li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc_items)
    body_html = "\n".join(
        f'<section id="{s["id"]}">\n<h2><span class="num">{s["num"]}.</span>{html.escape(s["title"])}</h2>\n'
        + "\n".join(s["blocks"])
        + "\n</section>"
        for s in sections
    )
    intro_html = "\n".join(f"    <p>{html.escape(p)}</p>" for p in intro)
    return HEAD.format(
        title=title, updated=updated, intro=intro_html, toc=toc_html, body=body_html,
        cross_label=cross_label, cross_href=cross_href, cross_title=cross_title,
    )


def main(terms_txt, risk_txt, privacy_txt=None):
    terms_lines = open(terms_txt).read().splitlines()
    risk_lines = open(risk_txt).read().splitlines()

    terms = build(
        terms_lines,
        title="Terms of Use",
        updated="April 1, 2026",
        skip_head=3,   # "Terms of Use" / "ESTX.Exchange – Terms of Use" / "Last Updated..."
        intro_count=3,
        cross_label="Please also review the risks of trading digital assets:",
        cross_href="risk-disclosure.html",
        cross_title="Risk Disclosure Statement",
        drop_lines=(
            # Internal counsel annotation in §25 — NOT part of the public terms.
            "Important:",
            "Because ESTX involves a Liechtenstein entity, Georgian VASP infrastructure, "
            "and potentially cross-border users, this section should be finalized by counsel "
            "before publication.",
        ),
    )
    risk = build(
        risk_lines,
        title="Risk Disclosure Statement",
        updated="April 1, 2026",
        skip_head=2,   # title / "Last Updated..."
        intro_count=5,
        cross_label="These risk disclosures form part of our user agreement:",
        cross_href="terms.html",
        cross_title="Terms of Use",
    )
    open("terms.html", "w").write(terms)
    open("risk-disclosure.html", "w").write(risk)
    written = "terms.html, risk-disclosure.html"

    if privacy_txt:
        privacy_lines = open(privacy_txt).read().splitlines()
        privacy = build(
            privacy_lines,
            title="Privacy Policy",
            updated="June 12, 2026",
            skip_head=2,   # title / "Last Updated..."
            intro_count=3,
            cross_label="Our full user agreement is set out in the:",
            cross_href="terms.html",
            cross_title="Terms of Use",
        )
        open("privacy.html", "w").write(privacy)
        written += ", privacy.html"
    print("written:", written)


if __name__ == "__main__":
    main(*sys.argv[1:4])
