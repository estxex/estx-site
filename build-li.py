#!/usr/bin/env python3
"""Build li/ — the estx.li landing page of the ESTX Utility Token (EN + DE), in the estx.exchange style.

Texts: li-src/wp-sections.json (the whitepaper split into paragraphs, word for word — see
li-src/parse_wp.py) and token-content.json (the token page data). Design, hero, cards and the
shared sections come from build-token.py, so both pages look the same.

  python3 build-li.py      -> li/index.html, li/brand_assets/*, li/<whitepaper>.pdf

Preview: https://stage.estx.exchange/li/   Production target: estx.li (nginx root -> the li/ folder).
"""
import importlib.util, json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "li")
spec = importlib.util.spec_from_file_location("bt", os.path.join(HERE, "build-token.py"))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
e, bi, icon, T, PDF, CONTRACT = bt.e, bt.bi, bt.icon, bt.T, bt.PDF, bt.CONTRACT

WP = {s["id"]: s for s in json.load(open(os.path.join(HERE, "li-src", "wp-sections.json"), encoding="utf-8"))}
WPTEXT = {l: " ".join(p for s in WP.values() for p in s[l]) for l in ("en", "de")}


def para(sid, lang, i):
    return WP[sid][lang][i]


def text(sid, lang, *idx, cls=""):
    """Whitepaper paragraphs as <p>, bullet paragraphs as <ul>."""
    out = []
    for i in idx:
        p = para(sid, lang, i)
        if p.startswith("•"):
            items = [x.strip() for x in p.split("•") if x.strip()]
            out.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>")
        else:
            out.append(f'<p{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{e(p)}</p>')
    return "".join(out)


def check(lang, *values):
    """Hand-entered table figures must appear in the whitepaper text."""
    for v in values:
        assert v in WPTEXT[lang], f"not in whitepaper ({lang}): {v}"


def head(lang, label, h2, intro_html=""):
    return f'<div class="sec-head reveal"><div class="label">{e(label)}</div><h2>{e(h2)}</h2>{intro_html}</div>'


L = lambda lang, en, de: en if lang == "en" else de


# ---------- new sections ----------

def sec_why(lang):
    cards = [("4.1", "Tokenization & RWA Market Outlook", "Tokenisierung & RWA-Marktausblick", "layers"),
             ("4.2", "Europe as a Regulated Crypto Hub", "Europa als regulierter Krypto-Hub", "shield"),
             ("4.3", "Demand for Utility-Driven Tokens", "Nachfrage nach nutzungsorientierten Tokens", "key"),
             ("4.4", "Regulatory-Forward Architecture", "Regulatorisch ausgerichtete Architektur", "lock")]
    market = "".join(f'<div class="why-card reveal">{icon(ic, i)}<h3>{e(L(lang, en, de))}</h3>{text(sid, lang, 0)}</div>'
                     for i, (sid, en, de, ic) in enumerate(cards))
    ps = WP["3"][lang]
    return f'''<section class="sec" id="why-{lang}"><div class="wrap">
{head(lang, L(lang, "Why ESTX", "Warum ESTX"), L(lang, "Problem & Opportunity", "Problem & Chance"), text("2", lang, 0))}
<div class="grid g2">
<div class="why-card plain reveal"><div class="eco-tag eval">{e(L(lang, "The problem", "Das Problem"))}</div>{text("3", lang, *range(0, 3))}</div>
<div class="why-card plain reveal"><div class="eco-tag">{e(L(lang, "The opportunity", "Die Chance"))}</div>{text("3", lang, *range(3, len(ps)))}</div>
</div>
<h3 class="sub-h reveal">{e(L(lang, "Market Overview", "Marktüberblick"))}</h3>
<div class="grid g4">{market}</div>
</div></section>'''


def sec_expansion(lang):
    jur = [("live", "Licensed · VASP", "Lizenziert · VASP", "Georgia", "Georgien", "6.3", (0, 1)),
           ("planned", "Planned · from Dec 2026", "Geplant · ab Dez. 2026", "European Union / EEA", "Europäische Union / EWR", "6.2", (0, 1)),
           ("eval", "Evaluation", "Evaluierung", "United Arab Emirates", "Vereinigte Arabische Emirate", "6.4", (0, 1))]
    cards = "".join(
        f'<div class="eco-card reveal{" planned" if st != "live" else ""}"><div class="eco-tag {st}">{e(L(lang, pen, pde))}</div>'
        f'<h3>{e(L(lang, hen, hde))}</h3><div class="prose">{text(sid, lang, *idx)}</div></div>'
        for st, pen, pde, hen, hde, sid, idx in jur)
    return f'''<section class="sec" id="expansion-{lang}"><div class="wrap">
{head(lang, L(lang, "Expansion", "Expansion"), L(lang, "One Ecosystem, Several Jurisdictions", "Ein Ökosystem, mehrere Jurisdiktionen"), text("6.1", lang, 0, 2))}
<div class="grid g3">{cards}</div>
<div class="callout reveal"><div class="callout-h">{e(L(lang, "Unified token utility across jurisdictions", "Einheitlicher Token-Nutzen über Jurisdiktionen hinweg"))}</div>{text("5.5", lang, 0, 2)}</div>
</div></section>'''


TGE_ROWS = [  # whitepaper 9.4
    ("Community & Ecosystem", "Community & Ecosystem", "700,000,000", "35.0%", "Project-controlled hardware wallet", "Projektkontrollierte Hardware-Wallet"),
    ("Liquidity Provisioning", "Liquidity Provisioning", "400,000,000", "20.0%", "Liquidity Safe (multisig 2-of-3)", "Liquidity-Safe (Multisig 2 von 3)"),
    ("Treasury & Strategic Operations", "Treasury & Strategic Operations", "300,000,000", "15.0%", "Treasury Safe (multisig 2-of-3)", "Treasury-Safe (Multisig 2 von 3)"),
    ("Founders & Management – TGE tranches (20%)", "Founders & Management – TGE-Tranchen (20 %)", "80,000,000", "4.0%", "Released to beneficiaries", "An Begünstigte freigegeben"),
    ("Founders & Management – vesting (80%)", "Founders & Management – Vesting (80 %)", "320,000,000", "16.0%", "Locked in vesting contracts", "In Vesting-Verträgen gesperrt"),
    ("Strategic partner (5%) *", "Strategischer Partner (5 %) *", "100,000,000", "5.0%", "Not yet transferred – held by the project", "Noch nicht übertragen – vom Projekt verwahrt"),
    ("Technical team – TGE tranche (20%)", "Tech-Team – TGE-Tranche (20 %)", "4,000,000", "0.2%", "Released to beneficiary", "An Begünstigten freigegeben"),
    ("Technical team – vesting (80%)", "Tech-Team – Vesting (80 %)", "16,000,000", "0.8%", "Locked in vesting contract", "Im Vesting-Vertrag gesperrt"),
    ("Governance reserve", "Governance-Reserve", "80,000,000", "4.0%", "Project-controlled hardware wallet", "Projektkontrollierte Hardware-Wallet"),
]
CIRC = [  # whitepaper 9.7
    ("16.8%", "336,000,000", "Locked in vesting contracts, linear release until 6 August 2029", "In Vesting-Verträgen gesperrt, lineare Freigabe bis 06.08.2029"),
    ("39.0%", "780,000,000", "Held in multisig safes, 2-of-3", "In Multisig-Safes, 2 von 3"),
    ("40.0%", "800,000,000", "Held in project-controlled hardware wallets", "In projektkontrollierten Hardware-Wallets"),
    ("4.2%", "84,000,000", "Transferred to beneficiaries as TGE tranches", "Als TGE-Tranchen an Begünstigte übertragen"),
]
de_num = lambda v: v.replace(",", ".")
de_pct = lambda v: v.replace(".", ",").replace("%", " %")


def sec_circulation(lang):
    de = lang == "de"
    rows = ""
    for en_l, de_l, n, pct, st_en, st_de in TGE_ROWS:
        num, p = (de_num(n), de_pct(pct)) if de else (n, pct)
        check(lang, num, p, L(lang, st_en, st_de))
        rows += f'<tr><td><b>{e(L(lang, en_l, de_l))}</b></td><td class="n">{num}</td><td class="n">{p}</td><td>{e(L(lang, st_en, st_de))}</td></tr>'
    total = (de_num("2,000,000,000"), de_pct("100.0%")) if de else ("2,000,000,000", "100.0%")
    cols = L(lang, ("Allocation", "ESTX", "%", "Holding / status"), ("Allokation", "ESTX", "%", "Verwahrung / Status"))
    th = "".join(f'<th{" class=n" if i in (1, 2) else ""}>{e(c)}</th>' for i, c in enumerate(cols))
    foot = para("9.4", lang, len(WP["9.4"][lang]) - 1)
    foot = re.sub(r"^\* (See footnote in Section 9\.5\.|Siehe Fußnote in Abschnitt 9\.5\.) ", "* ", foot)
    tiles = ""
    for pct, n, en_t, de_t in CIRC:
        p, num = (de_pct(pct), de_num(n)) if de else (pct, n)
        check(lang, p, num)
        tiles += f'<div class="kpi"><b>{p}</b><span class="kpi-n">{num} ESTX</span><span>{e(L(lang, en_t, de_t))}</span></div>'
    return f'''<section class="sec" id="circulation-{lang}"><div class="wrap">
{head(lang, "Tokenomics", L(lang, "Distribution at the TGE", "Verteilung zum TGE"), text("9.4", lang, 0))}
<div class="tcard reveal"><table><thead><tr>{th}</tr></thead><tbody>{rows}
<tr class="total"><td><b>{L(lang, "Total", "Summe")}</b></td><td class="n"><b>{total[0]}</b></td><td class="n"><b>{total[1]}</b></td><td></td></tr></tbody></table></div>
<p class="note">{e(foot)}</p>
<h3 class="sub-h reveal">{e(L(lang, "Circulating Supply & Circulation Management", "Umlaufmenge & Zirkulationsmanagement"))}</h3>
<p class="lead-p">{e(para("9.7", lang, 0))}</p>
<div class="kpis kpis4 reveal">{tiles}</div>
<div class="prose reveal">{text("9.7", lang, 3, 4, 7)}</div>
<div class="callout reveal"><div class="callout-h">{e(L(lang, "Supply reduction from own holdings", "Angebotsreduktion aus eigenen Beständen"))}</div>{text("9.8", lang, 0, 5, 6)}</div>
</div></section>'''


def sec_security(lang):
    cards = [("10.2", "Security Review & Audit Status", "Sicherheitsprüfung & Audit-Status", "search"),
             ("10.3", "Treasury & Access Controls", "Treasury- & Zugriffskontrollen", "users")]
    body = "".join(f'<div class="why-card plain reveal">{icon(ic, i)}<h3>{e(L(lang, en, de))}</h3>{text(sid, lang, 0, 1)}</div>'
                   for i, (sid, en, de, ic) in enumerate(cards))
    return f'''<section class="sec" id="security-{lang}"><div class="wrap">
{head(lang, L(lang, "Security", "Sicherheit"), L(lang, "Review, Audit Status and Controls", "Prüfung, Audit-Status und Kontrollen"))}
<div class="grid g2">{body}</div>
</div></section>'''


def roadmap_items(raw):
    items = []
    for x in [x.strip() for x in raw.split("•") if x.strip()]:
        m = re.match(r"^([^:]{3,32}\d{4}(?: \((?:planned|geplant)\))?):\s*(.+)$", x)
        items.append((m.group(1), m.group(2)) if m else ("", x))
    return items


def sec_roadmap(lang):
    ps = WP["11"][lang]          # [Completed, • items, Next steps, • items]
    cols = ""
    for (h_i, l_i), state in (((0, 1), "done"), ((2, 3), "next")):
        lis = "".join(f'<li class="tl-{state}">{f"<span class=tl-date>{e(d)}</span>" if d else ""}<span class="tl-text">{e(t)}</span></li>'
                      for d, t in roadmap_items(ps[l_i]))
        cols += f'<div class="tl-col reveal"><h3 class="tl-h">{e(ps[h_i])}</h3><ol class="tl">{lis}</ol></div>'
    return f'''<section class="sec" id="roadmap-{lang}"><div class="wrap">
{head(lang, "Roadmap", L(lang, "Where the Ecosystem Stands", "Wo das Ökosystem steht"))}
<div class="grid g2 tl-grid">{cols}</div>
</div></section>'''


def sec_governance(lang):
    role, rest = para("12.1", lang, 1).split(": ", 1)
    name, desc = rest.split(" – ", 1)
    return f'''<section class="sec" id="governance-{lang}"><div class="wrap">
{head(lang, "Management & Governance", L(lang, "Who Runs ESTX Venture GmbH", "Wer die ESTX Venture GmbH führt"), text("12.1", lang, 0))}
<div class="grid g2">
<div class="why-card plain reveal">
  <div class="ceo"><div class="ceo-mono" aria-hidden="true">CB</div><div><div class="ceo-role">{e(role)}</div><div class="ceo-name">{e(name)}</div><div class="ceo-desc">{e(desc)}</div></div></div>
  <div class="prose">{text("12.1", lang, 2, 3, 4)}</div>
</div>
<div class="why-card plain reveal"><h3>{e(L(lang, "Governance principles", "Governance-Grundsätze"))}</h3><div class="prose">{text("12.3", lang, 0, 1, 2)}{text("12.2", lang, len(WP["12.2"][lang]) - 1)}</div></div>
</div>
</div></section>'''


# ---------- page assembly ----------

def shared_sections(lang):
    """The token page sections (hero, parameters, utility, ...) keyed by name."""
    html_ = bt.main_block(lang)
    out = {}
    for m in re.finditer(r'(<section class="(hero|sec(?: alt)?|cta-band)"(?: id="([a-z]+)-(?:en|de)")?>.*?</section>)', html_, re.S):
        out[m.group(3) or "cta"] = m.group(1)
    return out


def page_block(lang):
    s = shared_sections(lang)
    order = [s["top"], sec_why(lang), s["token"], s["ecosystem"], sec_expansion(lang), s["utility"], s["allocation"],
             sec_circulation(lang), s["vesting"], s["contract"], sec_security(lang), s["addresses"], sec_roadmap(lang),
             sec_governance(lang), s["legal"], s["cta"]]
    out, k = [], 0
    for sec in order:                                  # re-alternate white / paper backgrounds
        if sec.startswith('<section class="sec'):
            sec = re.sub(r'^<section class="sec(?: alt)?"', f'<section class="sec{" alt" if k % 2 else ""}"', sec)
            k += 1
        out.append(sec)
    return f'<div data-lang="{lang}">\n' + "\n\n".join(out) + "\n</div>"


NAV = [("why", "Why ESTX", "Warum ESTX"), ("ecosystem", "Ecosystem", "Ökosystem"), ("utility", "Utility", "Nutzen"),
       ("allocation", "Tokenomics", "Tokenomics"), ("contract", "Technology", "Technologie"), ("roadmap", "Roadmap", "Roadmap"),
       ("governance", "Governance", "Governance")]


def nav_links(cls, close=False):
    oc = ' onclick="closeMob()"' if close else ""
    return "".join(f'<a href="#{k}-en" class="{cls}" data-lang="en"{oc}>{en}</a><a href="#{k}-de" class="{cls}" data-lang="de"{oc}>{de}</a>'
                   for k, en, de in NAV)


todo = lambda x: f'<span class="todo">[{e(x)}]</span>'


def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img src="brand_assets/logo_bw.svg" alt="ESTX" style="height:30px;width:auto;"/>
        <p class="f-desc">{bi("ESTX Utility Token · issued by ESTX Venture GmbH, Liechtenstein", "ESTX Utility Token · ausgegeben von der ESTX Venture GmbH, Liechtenstein")}</p>
        {bt.wp_button("btn-primary", "Whitepaper (PDF)", "en", "") .replace('class="btn-primary"', 'class="btn-primary" style="font-size:0.78rem;"')}
      </div>
      <div id="imprint"><div class="f-col-h">{bi("Issuer · Imprint", "Emittentin · Impressum")}</div>
        <p class="f-text">ESTX Venture GmbH<br/>Industriestrasse 4<br/>9491 Ruggell, Liechtenstein<br/>CEO: Christoph Bosch<br/>{bi("Commercial register", "Handelsregister")}: {todo("FL-…")}<br/>E-mail: {todo("hello@estx.li?")}</p></div>
      <div><div class="f-col-h">{bi("Exchange operator", "Börsenbetreiberin")}</div>
        <p class="f-text">ESTX.exchange International<br/>ESTX Georgia LLC, Kutaisi, Georgia<br/>{bi("Registration number", "Registrierungsnummer")} 412800036<br/>VASP License L37-2026<br/>National Bank of Georgia</p></div>
      <div><div class="f-col-h">{bi("Links", "Links")}</div><ul class="f-list">
        <li><a href="{e(PDF)}">Whitepaper (PDF)</a></li>
        <li><a href="https://etherscan.io/token/{CONTRACT}" target="_blank" rel="noopener">{bi("Contract on Etherscan", "Vertrag auf Etherscan")}</a></li>
        <li><a href="https://estx.exchange" target="_blank" rel="noopener">ESTX.exchange ↗</a></li>
        <li><a href="#legal-en" data-lang="en">Legal</a><a href="#legal-de" data-lang="de">Recht</a></li></ul></div>
    </div>
    <div class="f-bottom"><div>© 2026 ESTX Venture GmbH</div><div>{bt.s2("facts")}</div></div>
  </div>
</footer>'''


LI_CSS = r"""
/* estx.li additions on top of the token page styles */
@media(min-width:1100px) and (max-width:1359px){.nav-links,.nav-right{display:none;}.burger{display:inline-block;}}
.nav-link,.nav-login,.nav-right .btn-primary{white-space:nowrap;}
.g3{grid-template-columns:1fr;}
@media(min-width:900px){.g3{grid-template-columns:repeat(3,1fr);}}
.eco-tag{display:inline-flex;align-items:center;gap:8px;font-size:0.65rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:var(--brand);background:rgba(20,76,188,0.06);border:1px solid rgba(20,76,188,0.14);border-radius:999px;padding:5px 12px;margin-bottom:14px;}
.eco-tag::before{content:'';width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 0 3px rgba(16,185,129,0.18);}
.eco-tag.planned{color:#8a6d22;background:rgba(184,150,62,0.08);border-color:rgba(184,150,62,0.25);}
.eco-tag.planned::before{background:transparent;border:1.5px solid #B8963E;box-shadow:none;}
.eco-tag.eval{color:#475569;background:rgba(100,116,139,0.08);border-color:rgba(100,116,139,0.22);}
.eco-tag.eval::before{background:transparent;border:1.5px solid #94a3b8;box-shadow:none;}
.eco-card.planned{background:transparent;border:1.5px dashed rgba(100,116,139,0.35);box-shadow:none;}
.prose p,.why-card p{margin-bottom:10px;}
.prose ul,.why-card ul,.callout ul{padding-left:18px;margin:6px 0 12px;display:flex;flex-direction:column;gap:5px;}
.prose p,.prose li{font-size:0.9rem;color:var(--muted);line-height:1.7;}
.callout p{margin-bottom:8px;}
.sub-h{font-size:clamp(1.3rem,2.4vw,1.7rem);font-weight:800;color:var(--ink);letter-spacing:-0.02em;margin:64px 0 12px;}
.lead-p{color:var(--muted);margin-bottom:20px;}
.kpis4{grid-template-columns:1fr;}
@media(min-width:640px){.kpis4{grid-template-columns:repeat(2,1fr);}}
@media(min-width:1100px){.kpis4{grid-template-columns:repeat(4,1fr);}}
.kpi .kpi-n{display:block;font-size:0.85rem;font-weight:700;letter-spacing:0;text-transform:none;color:var(--ink);margin:2px 0 6px;font-variant-numeric:tabular-nums;}
.kpi span:last-child{letter-spacing:0.02em;text-transform:none;font-weight:600;font-size:0.8rem;line-height:1.5;}
.tl-h{font-size:1.1rem;font-weight:800;color:var(--ink);margin-bottom:18px;}
.tl{list-style:none;position:relative;padding-left:26px;}
.tl::before{content:'';position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:var(--line);}
.tl li{position:relative;margin-bottom:20px;}
.tl li::before{content:'';position:absolute;left:-26px;top:4px;width:14px;height:14px;border-radius:50%;box-sizing:border-box;}
.tl-done::before{background:var(--brand);box-shadow:0 0 0 4px rgba(20,76,188,0.14);}
.tl-next::before{background:#fff;border:2px solid #B8963E;}
.tl-date{display:block;font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--brand);margin-bottom:3px;}
.tl-next .tl-date{color:#8a6d22;}
.tl-text{font-size:0.92rem;color:var(--ink);line-height:1.6;}
.ceo{display:flex;align-items:center;gap:16px;margin-bottom:18px;}
.ceo-mono{width:56px;height:56px;border-radius:14px;background:linear-gradient(135deg,var(--brand),var(--navy));color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Outfit',sans-serif;font-weight:800;font-size:1.1rem;flex-shrink:0;}
.ceo-role{font-size:0.68rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#94a3b8;}
.ceo-name{font-family:'Outfit',sans-serif;font-size:1.25rem;font-weight:800;color:var(--ink);}
.ceo-desc{font-size:0.85rem;color:var(--muted);}
.f-text{font-size:0.84rem;color:rgba(255,255,255,0.5);line-height:1.75;}
.todo{background:#FEF3C7;color:#92400E;padding:0 5px;border-radius:4px;font-weight:600;}
"""


def build():
    js = bt.JS
    old_title = "document.title=lang==='de'?'ESTX Utility Token — ESTX.Exchange':'ESTX Utility Token — ESTX.Exchange';"
    assert js.count(old_title) == 1
    js = js.replace(old_title, "")
    mob_btns = (f'<a href="https://estx.exchange" class="btn-outline-white" target="_blank" rel="noopener">ESTX.exchange ↗</a>'
                + bt.wp_button("btn-primary", "Whitepaper (PDF)", "en", ""))
    page = f'''<!DOCTYPE html>
<html lang="en" data-ui-lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<meta name="robots" content="index, follow"/>
<title>ESTX Utility Token — ESTX Venture GmbH</title>
<meta name="description" content="{e(T["en"]["meta_desc"])}"/>
<link rel="canonical" href="https://estx.li/"/>
<link rel="icon" href="brand_assets/favicon.png" type="image/png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<script>{bt.HEAD_JS}</script>
<style>{bt.CSS}{LI_CSS}</style>
</head>
<body>

<div class="mob-menu" id="mobMenu" role="dialog" aria-modal="true" aria-label="Menu">
  <button class="mob-close" onclick="closeMob()" aria-label="Close menu"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
  {nav_links("mob-link", close=True)}
  <div class="mob-lang">
    <button id="mobLangen" onclick="setLang('en');closeMob();">&#127468;&#127463; EN</button>
    <button id="mobLangde" onclick="setLang('de');closeMob();">&#127465;&#127466; DE</button>
  </div>
  <div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap;justify-content:center;">{mob_btns}</div>
</div>

<nav class="top" aria-label="Main">
  <div class="nav-inner">
    <a href="#top" aria-label="ESTX Utility Token"><img src="brand_assets/logo.svg" alt="ESTX" style="height:34px;width:auto;display:block;"/></a>
    <div class="nav-links">{nav_links("nav-link")}</div>
    <div class="nav-right">
      <div class="lang-switch">
        <button class="lang-switch-btn" id="langBtn" onclick="toggleLangDropdown()" aria-label="Select language" aria-haspopup="true">
          <span id="langFlag">&#127468;&#127463;</span><span id="langCode">EN</span>
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="lang-dropdown" id="langDropdown">
          <button class="lang-option" id="langOpten" onclick="setLang('en')">&#127468;&#127463; English</button>
          <button class="lang-option" id="langOptde" onclick="setLang('de')">&#127465;&#127466; Deutsch</button>
        </div>
      </div>
      <a href="https://estx.exchange" class="nav-login" target="_blank" rel="noopener">ESTX.exchange ↗</a>
      {bt.wp_button("btn-primary", "Whitepaper (PDF)", "en", "")}
    </div>
    <button class="burger" onclick="openMob()" aria-label="Open menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0a1628" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
</nav>

<main id="top">
{page_block("en")}
{page_block("de")}
</main>

{footer()}
<script>{js}</script>
</body>
</html>
'''
    os.makedirs(os.path.join(OUT, "brand_assets"), exist_ok=True)
    for f in ("logo.svg", "logo_bw.svg", "favicon.png"):
        shutil.copy(os.path.join(HERE, "brand_assets", f), os.path.join(OUT, "brand_assets", f))
    if bt.PDF_OK:
        shutil.copy(os.path.join(HERE, PDF), os.path.join(OUT, PDF))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    print("written:", os.path.join(OUT, "index.html"), len(page.encode()), "bytes")


if __name__ == "__main__":
    build()
