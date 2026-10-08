#!/usr/bin/env python3
"""Build token.html — the ESTX Utility Token page (EN + DE) in the estx.exchange site style.

Content lives in token-content.json (taken from ESTX Utility Token Whitepaper 2.0 via
build_landing.py). Layout, colours, nav and footer mirror index.html.

  python3 build-token.py                              # writes token.html
  python3 build-token.py --import ../build_landing.py # refresh token-content.json first

Language: same switch as index.html (localStorage key estx_lang); token.html?lang=de opens German.
"""
import html, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "token-content.json")

if len(sys.argv) == 3 and sys.argv[1] == "--import":
    spec = importlib.util.spec_from_file_location("bl", sys.argv[2])
    bl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bl)
    data = {"source": "ESTX Utility Token Whitepaper 2.0 (September 2026), via build_landing.py",
            "PDF": bl.PDF, "CONTRACT": bl.CONTRACT, "ADDR": bl.ADDR, "ALLOC": bl.ALLOC,
            "RELEASE": bl.RELEASE, "T": bl.T}
    json.dump(data, open(CONTENT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("content refreshed:", CONTENT)

C = json.load(open(CONTENT, encoding="utf-8"))
T, PDF, CONTRACT = C["T"], C["PDF"], C["CONTRACT"]
# allocation colours mapped onto the site palette (brand, gold, purple, green, light blue)
SITE_COLORS = ["#144CBC", "#B8963E", "#7C3AED", "#10b981", "#5b9aff"]

e = lambda s: html.escape(s, quote=True)


def bi(en, de, tag="span", cls=""):
    """Same element twice, one per language; CSS hides the inactive one."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-lang="en">{en}</{tag}><{tag}{c} data-lang="de">{de}</{tag}>'


# site strings (copied from the index.html i18n dictionary)
S = {
    "login": ("Login", "Anmelden"), "signup": ("Sign Up", "Registrieren"), "home": ("Home", "Startseite"),
    "footer_desc": ("Next-generation digital asset exchange with a purpose-built three-tier market structure.",
                    "Börse der nächsten Generation für digitale Assets mit einer speziell entwickelten Drei-Stufen-Marktstruktur."),
    "footer_signup": ("Sign Up Free", "Kostenlos registrieren"),
    "col_exchange": ("Exchange", "Börse"), "crypto_prices": ("Crypto Prices", "Krypto-Kurse"),
    "trade_now": ("Trade Now", "Jetzt handeln"), "buy_crypto": ("Buy Crypto", "Krypto kaufen"),
    "institutional": ("Institutional", "Institutionell"), "list_token": ("List Token", "Token listen"),
    "col_service": ("Service", "Service"), "help": ("Help Center", "Hilfecenter"),
    "guide": ("Beginner’s Guide", "Einsteiger-Leitfaden"), "ticket": ("Submit a Ticket", "Ticket einreichen"),
    "contact": ("Contact Us", "Kontakt"), "col_legal": ("Legal", "Rechtliches"),
    "terms": ("Terms of Use", "Nutzungsbedingungen"), "privacy": ("Privacy Policy", "Datenschutzerklärung"),
    "risk": ("Risk Disclosure", "Risikohinweis"), "security": ("Security", "Sicherheit"), "about": ("About Us", "Über uns"),
    "legal": ('<strong>ESTX Georgia LLC</strong> — Avtomshenebeli St. N 88 (Plot N01/298), Free Industrial Zone, Kutaisi, Georgia. Regulated as a Virtual Asset Service Provider by the National Bank of Georgia (VASP License L37-2026 · Registration number 412800036). ESTX Georgia LLC directly provides and operates the platform infrastructure, exchange services, and custody. Trading involves significant risk.',
              '<strong>ESTX Georgia LLC</strong> — Avtomshenebeli Str. N 88 (Grundstück N01/298), Freie Industriezone, Kutaissi, Georgien. Als Virtual Asset Service Provider von der Nationalbank von Georgien reguliert (VASP-Lizenz L37-2026 · Registrierungsnummer 412800036). Die ESTX Georgia LLC stellt die Plattforminfrastruktur, die Handelsdienstleistungen und die Verwahrung unmittelbar selbst bereit. Der Handel ist mit erheblichen Risiken verbunden.'),
    "copy": ("Copy", "Kopieren"), "copied": ("Copied", "Kopiert"),
    "verified": ("Source code verified on Etherscan", "Quellcode auf Etherscan verifiziert"),
    "contract": ("Contract address", "Contract-Adresse"),
    "facts": ("All facts on this page are taken from Whitepaper 2.0 and verified against the Ethereum mainnet.",
              "Alle Angaben auf dieser Seite stammen aus Whitepaper 2.0 und wurden gegen das Ethereum-Mainnet geprüft."),
}
s2 = lambda k: bi(e(S[k][0]), e(S[k][1]))

ICON = {  # 24x24 stroke icons
    "receipt": '<path d="M4 2v20l3-2 3 2 3-2 3 2 3-2 1 .7V2l-1 .7-3-2-3 2-3-2-3 2-3-2z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3 21 2M17 6l3 3M14 9l2 2"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "layers": '<path d="M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "play": '<circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4z"/>',
    "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.5 8 11 4.6-1.5 8-6 8-11V5z"/>',
    "flame": '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-9-1 2-2 3-4 3 0-3-1-5-3-7 0 4-5 7-5 13 0 4 3 7 9 7z"/>',
    "users": '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-7 7-7s7 3 7 7M16 4a4 4 0 0 1 0 8M22 21c0-3-2-5.5-4.5-6.5"/>',
    "pen": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "undo": '<path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-15-6.7L3 13"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
}
TINT = [("20,76,188", "#144CBC"), ("124,58,237", "#7C3AED"), ("184,150,62", "#B8963E"), ("16,185,129", "#10b981")]


def icon(name, i):
    rgb, stroke = TINT[i % 4]
    return (f'<div class="why-icon" style="background:linear-gradient(135deg,rgba({rgb},0.12),rgba({rgb},0.06));">'
            f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg></div>')


def sec_head(t, white=False):
    eyebrow, h2, p = t
    return (f'<div class="sec-head reveal"><div class="label">{e(eyebrow)}</div>'
            f'<h2>{e(h2)}</h2><p>{e(p)}</p></div>')


def main_block(lang):
    t = T[lang]
    L = 0 if lang == "en" else 1
    de = lang == "de"
    pct = (lambda p: f"{p} %") if de else (lambda p: f"{p}%")
    tok = (lambda v: v.replace(",", ".")) if de else (lambda v: v)
    a = lambda anchor: f'{anchor}-{lang}'

    # hero
    h1_words = t["h1"].split(". ", 1)  # "One Token." / "Every ESTX Platform."
    h1 = (f'{e(h1_words[0])}.<br/><span class="accent">{e(h1_words[1].split(" ", 1)[0])}</span> '
          f'{e(h1_words[1].split(" ", 1)[1])}') if len(h1_words) == 2 else e(t["h1"])
    stat_icons = ["layers", "lock", "zap", "shield"]
    stats = "".join(
        f'<div class="hfeat">{icon(stat_icons[i], i).replace("why-icon", "hfeat-icon")}'
        f'<div><div class="hfeat-label">{e(lbl)}</div><div class="hfeat-val">{e(val)}</div></div></div>'
        for i, (val, lbl) in enumerate(t["stats"]))
    hero = f'''
<section class="hero" id="{a("top")}">
  <div class="hero-bg" aria-hidden="true"><svg width="100%" height="100%"><defs><pattern id="grid-{lang}" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M 44 0 L 0 0 0 44" fill="none" stroke="#fff" stroke-width="0.5"/></pattern></defs><rect width="100%" height="100%" fill="url(#grid-{lang})"/></svg></div>
  <div class="hero-inner">
    <div class="hero-grid">
      <div class="hero-text">
        <div class="label label-white reveal">{e(t["eyebrow"])}</div>
        <h1 class="hero-h1 reveal">{h1}</h1>
        <p class="hero-sub reveal">{e(t["lead"])}</p>
        <div class="hero-btns reveal">
          <a href="{e(PDF)}" class="btn-hero-white">{e(t["cta1"])}<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
          <a href="https://etherscan.io/token/{CONTRACT}" class="btn-hero-outline" target="_blank" rel="noopener">{e(t["cta2"])}</a>
        </div>
      </div>
      <aside class="token-card reveal" aria-label="{e(S["contract"][L])}">
        <div class="tc-top"><img src="brand_assets/logo_bw.svg" alt="ESTX" class="tc-logo"/><span class="tc-chip">ERC-20 · Ethereum</span></div>
        <div class="tc-label">{e(S["contract"][L])}</div>
        <div class="tc-addr mono">{CONTRACT}</div>
        <div class="tc-actions">
          <button type="button" class="tc-copy" data-copy="{CONTRACT}" data-done="{e(S["copied"][L])}">{e(S["copy"][L])}</button>
          <a href="https://etherscan.io/address/{CONTRACT}#code" target="_blank" rel="noopener" class="tc-link">{e(S["verified"][L])} ↗</a>
        </div>
      </aside>
    </div>
    <div class="hero-bottom reveal">{stats}</div>
  </div>
</section>'''

    params = "".join(f'<div class="prow"><dt>{e(k)}</dt><dd{" class=\"mono\"" if v.startswith("0x") else ""}>{e(v)}</dd></div>'
                     for k, v in t["params"])
    util_icons = ["receipt", "key", "zap", "layers"]
    utility = "".join(f'<div class="why-card reveal">{icon(util_icons[i], i)}<h3>{e(h)}</h3><p>{e(p)}</p></div>'
                      for i, (h, p) in enumerate(t["utility"]))
    conveys = "".join(f"<li>{e(x)}</li>" for x in t["conveys"])

    alloc = C["ALLOC"]
    bar = "".join(f'<span style="flex:{x[2]};background:{SITE_COLORS[i]}" title="{e(x[L])} {pct(x[2])}">{pct(x[2])}</span>'
                  for i, x in enumerate(alloc))
    alloc_rows = "".join(
        f'<tr><td><span class="swatch" style="background:{SITE_COLORS[i]}"></span><b>{e(x[L])}</b>'
        f'<span class="sub">{e(d)}</span></td><td class="n">{pct(x[2])}</td><td class="n">{tok(x[3])}</td></tr>'
        for i, (x, d) in enumerate(zip(alloc, t["alloc_desc"])))
    th = lambda cols: "".join(f'<th{" class=\"n\"" if i else ""}>{e(c)}</th>' for i, c in enumerate(cols))
    total = "Summe" if de else "Total"

    kpi = [(pct(20), "zum TGE" if de else "at the TGE"),
           ("36", "Monate, linear, ohne Cliff" if de else "months, linear, no cliff"),
           ("06.08.2029" if de else "6 Aug 2029", "Ende des Vestings" if de else "end of vesting")]
    kpi_html = "".join(f'<div class="kpi"><b>{e(x)}</b><span>{e(y)}</span></div>' for x, y in kpi)
    rel_rows = "".join(
        f'<tr><td>{e(r[L])}</td><td class="n">{tok(r[2])}</td><td class="n">{tok(r[3])}</td><td class="n">{tok(r[4])}</td>'
        f'<td class="n">{(r[5].replace(".", ",") + " %") if de else (r[5] + "%")}</td></tr>'
        for r in C["RELEASE"])

    c_icons = ["lock", "play", "shield", "flame", "users", "pen", "undo", "search"]
    contract = "".join(f'<div class="why-card reveal">{icon(c_icons[i], i)}<h3>{e(h)}</h3><p>{e(p)}</p></div>'
                       for i, (h, p) in enumerate(t["contract"]))
    addr_rows = "".join(f'<tr><td>{e(x[L])}</td><td class="mono"><a href="https://etherscan.io/address/{x[2]}" target="_blank" rel="noopener">{x[2]}</a></td></tr>'
                        for x in C["ADDR"])
    eco = "".join(
        f'<div class="eco-card reveal{" planned" if i else ""}"><div class="eco-tag">{e(tag)}</div><h3>{e(h)}</h3><dl>'
        + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in rows) + "</dl></div>"
        for i, (h, tag, rows) in enumerate(t["eco"]))
    legal_not = "".join(f"<li>{e(x)}</li>" for x in t["legal_not"])
    risks = "".join(f"<li>{e(x)}</li>" for x in t["risks"])

    return f'''<div data-lang="{lang}">
{hero}

<section class="sec" id="{a("token")}"><div class="wrap">
{sec_head(t["s_token"])}
<dl class="params reveal">{params}</dl>
</div></section>

<section class="sec alt" id="{a("utility")}"><div class="wrap">
{sec_head(t["s_utility"])}
<div class="grid g4">{utility}</div>
<div class="callout reveal"><div class="callout-h">{e(t["conveys_h"])}</div><ul class="two-col">{conveys}</ul></div>
</div></section>

<section class="sec" id="{a("allocation")}"><div class="wrap">
{sec_head(t["s_alloc"])}
<div class="bar reveal" role="img" aria-label="{e(t["s_alloc"][1])}">{bar}</div>
<div class="tcard reveal"><table><thead><tr>{th(t["th_alloc"])}</tr></thead><tbody>{alloc_rows}
<tr class="total"><td><b>{total}</b></td><td class="n"><b>{pct(100)}</b></td><td class="n"><b>{tok("2,000,000,000")}</b></td></tr></tbody></table></div>
</div></section>

<section class="sec alt" id="{a("vesting")}"><div class="wrap">
{sec_head(t["s_vest"])}
<div class="kpis reveal">{kpi_html}</div>
<div class="tcard reveal"><table><thead><tr>{th(t["th_rel"])}</tr></thead><tbody>{rel_rows}</tbody></table></div>
<p class="note">{e(t["vest_note"])}</p>
</div></section>

<section class="sec" id="{a("contract")}"><div class="wrap">
{sec_head(t["s_contract"])}
<div class="grid g4">{contract}</div>
</div></section>

<section class="sec alt" id="{a("addresses")}"><div class="wrap">
{sec_head(t["s_addr"])}
<div class="tcard reveal"><table><thead><tr>{th(t["th_addr"])}</tr></thead><tbody>{addr_rows}</tbody></table></div>
</div></section>

<section class="sec" id="{a("ecosystem")}"><div class="wrap">
{sec_head(t["s_eco"])}
<div class="grid g2">{eco}</div>
<div class="callout reveal"><div class="callout-h">{e(t["neutral_h"])}</div><p>{e(t["neutral"])}</p></div>
</div></section>

<section class="sec alt" id="{a("legal")}"><div class="wrap">
{sec_head(t["s_legal"])}
<div class="grid g2">
<div class="why-card plain reveal"><h3>{e(t["legal_not_h"])}</h3><ul>{legal_not}</ul></div>
<div class="why-card plain reveal"><h3>{e(t["risk_h"])}</h3><ul>{risks}</ul></div>
</div>
<div class="disc"><b>{e(t["disclaimer_h"])}.</b> {e(t["disclaimer"])}</div>
<p class="note">{e(S["facts"][L])}</p>
</div></section>

<section class="cta-band"><div class="wrap cta-inner">
<div><h2>{e(t["final_h"])}</h2><p>{e(t["final_p"])}</p></div>
<a href="{e(PDF)}" class="btn-cta-white">{e(t["nav_cta"])}<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M12 3v12M6 11l6 6 6-6M5 21h14"/></svg></a>
</div></section>
</div>'''


CSS = r"""
:root{--brand:#144CBC;--navy:#032363;--gold:#C9A84C;--purple:#7C3AED;--ink:#0a1628;--muted:#64748b;--line:#eaeff8;--paper:#f8faff;--dark:#020d24;}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;scroll-padding-top:84px;overflow-x:hidden;}
body{font-family:'DM Sans',sans-serif;background:#fff;color:var(--ink);overflow-x:hidden;max-width:100vw;-webkit-font-smoothing:antialiased;}
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");pointer-events:none;z-index:9999;}
html[data-ui-lang="de"] [data-lang="en"],html:not([data-ui-lang="de"]) [data-lang="de"]{display:none !important;}
h1,h2,h3,h4{font-family:'Outfit',sans-serif;}
a:focus-visible,button:focus-visible{outline:2px solid var(--brand);outline-offset:3px;border-radius:4px;}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.86em;word-break:break-all;}
.wrap{max-width:1280px;margin:0 auto;}

/* NAV — same as index.html */
nav.top{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 24px;background:rgba(255,255,255,0.96);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(20,76,188,0.08);box-shadow:0 2px 24px rgba(3,35,99,0.07);}
.nav-inner{max-width:1280px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:24px;}
.nav-links{display:none;align-items:center;gap:26px;}
.nav-link{font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:rgba(10,22,40,0.7);text-decoration:none;transition:color 0.2s;position:relative;}
.nav-link::after{content:'';position:absolute;bottom:-3px;left:0;right:0;height:2px;background:var(--brand);transform:scaleX(0);transform-origin:left;transition:transform 0.2s ease;}
.nav-link:hover{color:var(--brand);}
.nav-link:hover::after{transform:scaleX(1);}
.nav-right{display:none;align-items:center;gap:12px;}
.nav-login{font-weight:600;font-size:0.85rem;color:var(--brand);text-decoration:none;}
.burger{background:none;border:none;cursor:pointer;padding:4px;}
@media(min-width:1100px){.nav-links,.nav-right{display:flex;}.burger{display:none;}}

.btn-primary{display:inline-flex;align-items:center;gap:8px;background:var(--brand);color:#fff;font-weight:700;font-size:0.8rem;letter-spacing:0.03em;padding:10px 20px;border-radius:8px;border:none;cursor:pointer;transition:transform 0.22s ease,box-shadow 0.22s ease,background 0.22s ease;text-decoration:none;box-shadow:0 4px 18px rgba(20,76,188,0.28);}
.btn-primary:hover{background:#1a58e0;transform:translateY(-2px);box-shadow:0 8px 28px rgba(20,76,188,0.38);}
.btn-primary:active{transform:translateY(0);}
.btn-outline-white{display:inline-flex;align-items:center;gap:8px;background:transparent;color:#fff;font-weight:700;font-size:0.875rem;padding:12px 28px;border-radius:8px;border:1.5px solid rgba(255,255,255,0.3);text-decoration:none;}

.lang-switch{position:relative;display:flex;align-items:center;}
.lang-switch-btn{display:flex;align-items:center;gap:5px;background:rgba(20,76,188,0.06);border:1px solid rgba(20,76,188,0.12);border-radius:8px;padding:6px 12px;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:0.78rem;font-weight:600;color:var(--brand);transition:background 0.2s,border-color 0.2s;user-select:none;}
.lang-switch-btn:hover{background:rgba(20,76,188,0.1);border-color:rgba(20,76,188,0.25);}
.lang-switch-btn:active{transform:scale(0.97);}
.lang-dropdown{position:absolute;top:calc(100% + 6px);right:0;background:#fff;border:1px solid #e2e8f8;border-radius:10px;box-shadow:0 8px 28px rgba(3,35,99,0.12);overflow:hidden;opacity:0;visibility:hidden;transform:translateY(-4px);transition:opacity 0.2s ease,transform 0.2s ease,visibility 0.2s;z-index:110;min-width:120px;}
.lang-dropdown.open{opacity:1;visibility:visible;transform:translateY(0);}
.lang-option{display:flex;align-items:center;gap:8px;width:100%;padding:10px 14px;border:none;background:none;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:0.8rem;font-weight:600;color:#475569;text-align:left;}
.lang-option:hover{background:rgba(20,76,188,0.06);color:var(--brand);}
.lang-option.active{color:var(--brand);background:rgba(20,76,188,0.04);}

.mob-menu{display:none;position:fixed;inset:0;background:rgba(3,35,99,0.97);backdrop-filter:blur(20px);z-index:200;flex-direction:column;align-items:center;justify-content:center;gap:26px;padding:24px;}
.mob-menu.open{display:flex;}
.mob-close{position:absolute;top:24px;right:24px;background:none;border:none;cursor:pointer;color:#fff;}
.mob-link{font-family:'Outfit',sans-serif;font-size:1.6rem;font-weight:700;color:#fff;text-decoration:none;}
.mob-lang{display:flex;gap:12px;margin-top:4px;}
.mob-lang button{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:10px 18px;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:0.9rem;font-weight:600;color:rgba(255,255,255,0.7);}
.mob-lang button.active{background:rgba(255,255,255,0.15);border-color:rgba(255,255,255,0.3);color:#fff;}

/* LABEL — same as index.html */
.label{display:inline-flex;align-items:center;gap:8px;font-size:0.7rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--brand);margin-bottom:14px;}
.label::before{content:'';width:20px;height:2px;background:var(--brand);flex-shrink:0;}
.label-white{color:rgba(255,255,255,0.55);}
.label-white::before{background:rgba(255,255,255,0.35);}

/* HERO — dark like the landing hero */
.hero{position:relative;overflow:hidden;background:var(--dark);}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 78% 40%,rgba(20,76,188,0.42) 0%,transparent 70%),radial-gradient(ellipse 45% 55% at 8% 100%,rgba(201,168,76,0.10) 0%,transparent 70%),linear-gradient(180deg,rgba(2,13,36,0) 60%,rgba(2,13,36,0.9) 100%);}
.hero-bg{position:absolute;inset:0;opacity:0.03;}
.hero-inner{position:relative;z-index:2;max-width:1280px;margin:0 auto;padding:136px 40px 36px;}
.hero-grid{display:grid;grid-template-columns:1fr;gap:40px;align-items:center;}
.hero-text{max-width:640px;}
.hero-h1{font-size:clamp(2.6rem,5.5vw,5.2rem);font-weight:900;color:#fff;line-height:0.96;letter-spacing:-0.04em;margin-bottom:22px;text-shadow:0 2px 30px rgba(0,0,0,0.3);}
.hero-h1 .accent{color:#5b9aff;}
.hero-sub{font-size:1.05rem;color:rgba(255,255,255,0.7);line-height:1.8;max-width:540px;}
.hero-btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px;}
.btn-hero-white{display:inline-flex;align-items:center;gap:8px;background:#fff;color:var(--navy);font-weight:700;font-size:0.9rem;padding:15px 32px;border-radius:10px;text-decoration:none;box-shadow:0 4px 24px rgba(0,0,0,0.2);transition:transform 0.22s,box-shadow 0.22s;}
.btn-hero-white:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,0.28);}
.btn-hero-outline{display:inline-flex;align-items:center;gap:8px;background:transparent;color:#fff;font-weight:700;font-size:0.85rem;padding:13px 28px;border-radius:8px;border:1.5px solid rgba(255,255,255,0.25);text-decoration:none;transition:border-color 0.22s,background 0.22s,transform 0.22s;}
.btn-hero-outline:hover{border-color:rgba(255,255,255,0.7);background:rgba(255,255,255,0.08);transform:translateY(-2px);}
.token-card{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:28px;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 30px 80px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.08);max-width:460px;}
.tc-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;}
.tc-logo{height:28px;width:auto;}
.tc-chip{font-size:0.68rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#5b9aff;background:rgba(91,154,255,0.12);border:1px solid rgba(91,154,255,0.25);border-radius:999px;padding:5px 11px;}
.tc-label{font-size:0.68rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:8px;}
.tc-addr{color:#fff;font-size:0.8rem;line-height:1.55;background:rgba(2,13,36,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 16px;}
.tc-actions{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:16px;}
.tc-copy{background:var(--brand);color:#fff;border:none;border-radius:8px;padding:9px 18px;font-family:'DM Sans',sans-serif;font-weight:700;font-size:0.8rem;cursor:pointer;transition:background 0.2s,transform 0.2s;}
.tc-copy:hover{background:#1a58e0;transform:translateY(-1px);}
.tc-copy:active{transform:translateY(0);}
.tc-link{font-size:0.8rem;font-weight:600;color:rgba(255,255,255,0.65);text-decoration:none;}
.tc-link:hover{color:#fff;}
.hero-bottom{display:flex;flex-wrap:wrap;gap:12px;margin-top:56px;padding-top:28px;border-top:1px solid rgba(255,255,255,0.08);}
.hfeat{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:12px 16px;backdrop-filter:blur(8px);}
.hfeat-icon{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.hfeat-icon svg{width:18px;height:18px;}
.hfeat-label{font-size:0.68rem;font-weight:600;color:rgba(255,255,255,0.45);}
.hfeat-val{font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:800;color:#fff;}
@media(min-width:1000px){.hero-grid{grid-template-columns:1.25fr 1fr;gap:64px;}.token-card{justify-self:end;width:100%;}}

/* SECTIONS — same rhythm as index.html */
.sec{padding:96px 24px;background:#fff;}
.sec.alt{background:var(--paper);}
.sec-head{max-width:680px;margin-bottom:48px;}
.sec-head h2{font-size:clamp(2rem,4vw,3rem);font-weight:800;color:var(--ink);letter-spacing:-0.03em;line-height:1.1;margin-bottom:18px;text-wrap:balance;}
.sec-head p{font-size:1rem;color:var(--muted);line-height:1.75;}
.grid{display:grid;gap:24px;}
.g4{grid-template-columns:1fr;}
.g2{grid-template-columns:1fr;}
@media(min-width:640px){.g4{grid-template-columns:repeat(2,1fr);}}
@media(min-width:900px){.g2{grid-template-columns:repeat(2,1fr);}}
@media(min-width:1100px){.g4{grid-template-columns:repeat(4,1fr);}}

.why-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:28px;position:relative;overflow:hidden;transition:transform 0.38s cubic-bezier(0.16,1,0.3,1),box-shadow 0.38s cubic-bezier(0.16,1,0.3,1),border-color 0.3s ease;box-shadow:0 1px 8px rgba(3,35,99,0.04);}
.why-card:hover{border-color:rgba(20,76,188,0.25);box-shadow:0 20px 48px rgba(3,35,99,0.1),0 4px 12px rgba(20,76,188,0.08);transform:translateY(-6px);}
.why-card h3{font-size:1rem;font-weight:700;color:var(--ink);margin-bottom:10px;transition:color 0.25s ease;}
.why-card:hover h3{color:var(--brand);}
.why-card p,.why-card li{font-size:0.875rem;color:var(--muted);line-height:1.7;}
.why-card ul{padding-left:18px;display:flex;flex-direction:column;gap:6px;}
.why-card.plain:hover{transform:none;}
.why-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:18px;transition:transform 0.38s cubic-bezier(0.16,1,0.3,1);}
.why-card:hover .why-icon{transform:scale(1.1) rotate(-4deg);}

.params{display:grid;grid-template-columns:1fr;background:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 28px;box-shadow:0 1px 8px rgba(3,35,99,0.04);}
.prow{display:grid;grid-template-columns:1fr;gap:4px;padding:16px 0;border-bottom:1px solid var(--line);}
.prow dt{font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#94a3b8;padding-top:3px;}
.prow dd{font-size:0.95rem;color:var(--ink);}
.prow dd.mono{font-size:0.8rem;padding-top:2px;}
@media(min-width:700px){.prow{grid-template-columns:190px 1fr;gap:16px;}}
@media(min-width:1100px){.params{grid-template-columns:1fr 1fr;column-gap:56px;}}
.params .prow:last-child{border-bottom:none;}
@media(min-width:1100px){.params .prow:nth-last-child(2){border-bottom:none;}}

.callout{margin-top:28px;background:linear-gradient(135deg,rgba(20,76,188,0.07),rgba(20,76,188,0.03));border:1px solid rgba(20,76,188,0.12);border-radius:16px;padding:22px 28px;}
.callout-h{font-size:0.7rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--brand);margin-bottom:10px;}
.callout p,.callout li{font-size:0.92rem;color:#475569;line-height:1.7;}
.two-col{padding-left:18px;columns:1;column-gap:40px;}
@media(min-width:700px){.two-col{columns:2;}}

.bar{display:flex;height:40px;border-radius:10px;overflow:hidden;gap:3px;margin-bottom:22px;}
.bar span{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:0.8rem;font-variant-numeric:tabular-nums;}
.tcard{background:#fff;border:1px solid var(--line);border-radius:16px;overflow-x:auto;box-shadow:0 1px 8px rgba(3,35,99,0.04);}
table{width:100%;border-collapse:collapse;font-size:0.92rem;}
th{text-align:left;font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:#94a3b8;font-weight:700;padding:16px 20px;border-bottom:1px solid var(--line);white-space:nowrap;}
td{padding:14px 20px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink);}
tbody tr:last-child td{border-bottom:none;}
tr.total td{background:var(--paper);}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;}
td .sub{display:block;color:var(--muted);font-size:0.84rem;margin-top:3px;}
td.mono a{color:var(--brand);text-decoration:none;}
td.mono a:hover{text-decoration:underline;}
.swatch{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:10px;vertical-align:0;}
.note{color:#94a3b8;font-size:0.84rem;line-height:1.7;margin-top:16px;max-width:900px;}
.kpis{display:grid;grid-template-columns:1fr;gap:16px;margin-bottom:24px;}
@media(min-width:700px){.kpis{grid-template-columns:repeat(3,1fr);}}
.kpi{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 24px;}
.kpi b{display:block;font-family:'Outfit',sans-serif;font-size:clamp(1.6rem,3vw,2.2rem);font-weight:800;color:var(--navy);letter-spacing:-0.03em;line-height:1.1;}
.kpi span{font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#94a3b8;}

.eco-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:28px;box-shadow:0 1px 8px rgba(3,35,99,0.04);}
/* planned platform: dashed outline = not built yet */
.eco-card.planned{background:transparent;border:1.5px dashed rgba(184,150,62,0.45);box-shadow:none;}
.eco-tag{display:inline-flex;align-items:center;gap:8px;font-size:0.65rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:var(--brand);background:rgba(20,76,188,0.06);border:1px solid rgba(20,76,188,0.14);border-radius:999px;padding:5px 12px;margin-bottom:14px;}
.eco-tag::before{content:'';width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 0 3px rgba(16,185,129,0.18);}
.eco-card.planned .eco-tag{color:#8a6d22;background:rgba(184,150,62,0.08);border-color:rgba(184,150,62,0.25);}
.eco-card.planned .eco-tag::before{background:transparent;border:1.5px solid #B8963E;box-shadow:none;}
.eco-card h3{font-size:1.3rem;font-weight:800;color:var(--ink);margin-bottom:16px;}
.eco-card dl{display:grid;grid-template-columns:120px 1fr;gap:8px 16px;font-size:0.9rem;}
.eco-card dt{color:var(--muted);font-weight:600;}
.eco-card dd{color:var(--ink);}
.disc{margin-top:32px;font-size:0.84rem;color:var(--muted);line-height:1.75;border-top:1px solid var(--line);padding-top:24px;max-width:1000px;}
.disc b{color:var(--ink);}

.cta-band{background:linear-gradient(135deg,var(--brand) 0%,var(--navy) 100%);padding:72px 24px;position:relative;overflow:hidden;}
.cta-inner{display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap;}
.cta-band h2{font-size:clamp(1.6rem,3vw,2.3rem);font-weight:800;color:#fff;letter-spacing:-0.03em;}
.cta-band p{color:rgba(255,255,255,0.72);margin-top:8px;}
.btn-cta-white{display:inline-flex;align-items:center;gap:8px;background:#fff;color:var(--brand);font-weight:700;font-size:0.9rem;padding:14px 32px;border-radius:8px;text-decoration:none;box-shadow:0 4px 20px rgba(0,0,0,0.2);transition:transform 0.22s,box-shadow 0.22s;}
.btn-cta-white:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,0.25);}

/* FOOTER — same as index.html */
footer{background:var(--dark);padding:60px 24px 32px;border-top:1px solid rgba(255,255,255,0.05);}
.footer-grid{display:grid;gap:32px;margin-bottom:48px;grid-template-columns:1fr 1fr;}
@media(min-width:768px){.footer-grid{grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;}}
.f-desc{font-size:0.82rem;color:rgba(255,255,255,0.35);line-height:1.7;max-width:240px;margin:16px 0 20px;}
.f-col-h{font-size:0.68rem;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:14px;}
.f-list{list-style:none;display:flex;flex-direction:column;gap:9px;}
.f-list a{font-size:0.84rem;color:rgba(255,255,255,0.5);text-decoration:none;transition:color 0.2s;}
.f-list a:hover,.f-list a[aria-current]{color:#fff;}
.f-social{display:flex;gap:12px;margin-top:18px;}
.f-social a{width:36px;height:36px;border-radius:10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;transition:background 0.2s,border-color 0.2s;}
.f-social a:hover{background:rgba(20,76,188,0.3);border-color:var(--brand);}
.f-legal{padding:20px 0;border-top:1px solid rgba(255,255,255,0.06);margin-bottom:16px;font-size:0.73rem;color:rgba(255,255,255,0.22);line-height:1.7;}
.f-legal strong{color:rgba(255,255,255,0.35);}
.f-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:0.72rem;color:rgba(255,255,255,0.18);}

.reveal{opacity:0;transform:translateY(24px);transition:opacity 0.65s ease,transform 0.65s cubic-bezier(0.16,1,0.3,1);}
.reveal.in{opacity:1;transform:none;}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto;}.reveal{opacity:1;transform:none;transition:none;}*{transition:none !important;}}

@media(max-width:600px){
  nav.top{padding:14px 16px;}
  .hero-inner{padding:112px 16px 28px;}
  .sec{padding:64px 16px;}
  .cta-band{padding:56px 16px;}
  footer{padding:48px 16px 28px;}
  .params{padding:4px 18px;}
  .why-card,.eco-card{padding:22px;}
  .bar span{font-size:0;}
  .eco-card dl{grid-template-columns:1fr;gap:2px 0;}
  .eco-card dd{margin-bottom:8px;}
  th,td{padding:12px 14px;}
}
"""

JS = r"""
(function(){
  var flags={en:'🇬🇧',de:'🇩🇪'};
  window.setLang=function(lang){
    lang=lang==='de'?'de':'en';
    document.documentElement.setAttribute('data-ui-lang',lang);
    document.documentElement.lang=lang;
    try{localStorage.setItem('estx_lang',lang);}catch(e){}
    document.getElementById('langFlag').innerHTML=flags[lang];
    document.getElementById('langCode').textContent=lang.toUpperCase();
    ['en','de'].forEach(function(l){
      var o=document.getElementById('langOpt'+l);if(o)o.classList.toggle('active',l===lang);
      var m=document.getElementById('mobLang'+l);if(m)m.classList.toggle('active',l===lang);
    });
    document.getElementById('langDropdown').classList.remove('open');
    document.title=lang==='de'?'ESTX Utility Token — ESTX.Exchange':'ESTX Utility Token — ESTX.Exchange';
    observe();
  };
  window.toggleLangDropdown=function(){document.getElementById('langDropdown').classList.toggle('open');};
  document.addEventListener('click',function(e){var ls=document.querySelector('.lang-switch');if(ls&&!ls.contains(e.target))document.getElementById('langDropdown').classList.remove('open');});
  window.openMob=function(){document.getElementById('mobMenu').classList.add('open');};
  window.closeMob=function(){document.getElementById('mobMenu').classList.remove('open');};
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeMob();document.getElementById('langDropdown').classList.remove('open');}});
  document.querySelectorAll('.tc-copy').forEach(function(b){
    var label=b.textContent;
    b.addEventListener('click',function(){
      var done=function(){b.textContent=b.getAttribute('data-done');setTimeout(function(){b.textContent=label;},1600);};
      if(navigator.clipboard){navigator.clipboard.writeText(b.getAttribute('data-copy')).then(done,function(){});}
    });
  });
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:0.08,rootMargin:'0px 0px -40px 0px'}):null;
  function observe(){document.querySelectorAll('.reveal:not(.in)').forEach(function(el){if(io&&el.offsetParent!==null)io.observe(el);else if(!io)el.classList.add('in');});}
  setLang(document.documentElement.getAttribute('data-ui-lang'));
})();
"""

HEAD_JS = ("(function(){var l=null;try{var q=new URLSearchParams(location.search).get('lang');"
           "if(q==='de'||q==='en'){l=q;localStorage.setItem('estx_lang',q);}else{l=localStorage.getItem('estx_lang');}}catch(e){}"
           "l=l==='de'?'de':'en';document.documentElement.setAttribute('data-ui-lang',l);document.documentElement.lang=l;})();")


def nav_links(cls, close=False):
    items = [("token", "Token", "Token"), ("allocation", "Allocation", "Allokation"), ("vesting", "Vesting", "Vesting"),
             ("contract", "Contract", "Vertrag"), ("ecosystem", "Ecosystem", "Ökosystem"), ("legal", "Legal", "Recht")]
    oc = ' onclick="closeMob()"' if close else ""
    out = "".join(f'<a href="#{k}-en" class="{cls}" data-lang="en"{oc}>{en}</a><a href="#{k}-de" class="{cls}" data-lang="de"{oc}>{de}</a>'
                  for k, en, de in items)
    return out + f'<a href="{e(PDF)}" class="{cls}"{oc}>Whitepaper</a>'


def footer():
    li = lambda href, k, ext=False: (f'<li><a href="{href}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{s2(k)}</a></li>')
    return f'''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img src="brand_assets/logo_bw.svg" alt="ESTX" style="height:30px;width:auto;"/>
        <p class="f-desc">{s2("footer_desc")}</p>
        <a href="https://trade.estx.exchange/signup" class="btn-primary" style="font-size:0.78rem;">{s2("footer_signup")}</a>
        <div class="f-social">
          <a href="https://t.me/estx_exchange" target="_blank" rel="noopener" aria-label="Telegram"><svg width="16" height="16" viewBox="0 0 24 24" fill="rgba(255,255,255,0.6)" aria-hidden="true"><path d="M21.9 4.3 18.6 19.8c-.2 1.1-.9 1.4-1.8.9l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.2-8.3c.4-.4-.1-.6-.6-.2L6.1 13.4 1.2 11.9c-1.1-.3-1.1-1.1.2-1.6L20.5 2.9c.9-.3 1.7.2 1.4 1.4z"/></svg></a>
          <a href="https://x.com/estx_exchange" target="_blank" rel="noopener" aria-label="X"><svg width="14" height="14" viewBox="0 0 24 24" fill="rgba(255,255,255,0.6)" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
        </div>
      </div>
      <div><div class="f-col-h">{s2("col_exchange")}</div><ul class="f-list">
        {li("index.html#markets", "crypto_prices")}{li("https://trade.estx.exchange/trade/btc-usdt", "trade_now", True)}
        {li("index.html#buy", "buy_crypto")}{li("index.html#institutional", "institutional")}{li("index.html#contact", "list_token")}</ul></div>
      <div><div class="f-col-h">{s2("col_service")}</div><ul class="f-list">
        {li("index.html#contact", "help")}{li("index.html#faq", "guide")}{li("index.html#contact", "ticket")}
        <li><a href="token.html" aria-current="page">ESTX Token</a></li>{li("index.html#contact", "contact")}</ul></div>
      <div><div class="f-col-h">{s2("col_legal")}</div><ul class="f-list">
        {li("terms.html", "terms")}{li("privacy.html", "privacy")}{li("risk-disclosure.html", "risk")}
        {li("index.html#security", "security")}{li("index.html#about", "about")}</ul></div>
    </div>
    <div class="f-legal">{bi(S["legal"][0], S["legal"][1], "p")}</div>
    <div class="f-bottom"><div>© 2026 ESTX Exchange. All rights reserved.</div><div>estx.exchange</div></div>
  </div>
</footer>'''


def build():
    en = T["en"]
    page = f'''<!DOCTYPE html>
<html lang="en" data-ui-lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<meta name="robots" content="index, follow"/>
<title>ESTX Utility Token — ESTX.Exchange</title>
<meta name="description" content="{e(en["meta_desc"])}"/>
<link rel="canonical" href="https://estx.exchange/token.html"/>
<link rel="icon" href="brand_assets/favicon.png" type="image/png"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<script>{HEAD_JS}</script>
<style>{CSS}</style>
</head>
<body>

<div class="mob-menu" id="mobMenu" role="dialog" aria-modal="true" aria-label="Menu">
  <button class="mob-close" onclick="closeMob()" aria-label="Close menu"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
  <a href="index.html" class="mob-link">{s2("home")}</a>
  {nav_links("mob-link", close=True)}
  <div class="mob-lang">
    <button id="mobLangen" onclick="setLang('en');closeMob();">&#127468;&#127463; EN</button>
    <button id="mobLangde" onclick="setLang('de');closeMob();">&#127465;&#127466; DE</button>
  </div>
  <div style="display:flex;gap:12px;margin-top:8px;">
    <a href="https://trade.estx.exchange/login" class="btn-outline-white">{s2("login")}</a>
    <a href="https://trade.estx.exchange/signup" class="btn-primary">{s2("signup")}</a>
  </div>
</div>

<nav class="top" aria-label="Main">
  <div class="nav-inner">
    <a href="index.html" aria-label="ESTX.Exchange home"><img src="brand_assets/logo.svg" alt="ESTX" style="height:34px;width:auto;display:block;"/></a>
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
      <a href="https://trade.estx.exchange/login" class="nav-login">{s2("login")}</a>
      <a href="https://trade.estx.exchange/signup" class="btn-primary">{s2("signup")}</a>
    </div>
    <button class="burger" onclick="openMob()" aria-label="Open menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0a1628" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
</nav>

<main>
{main_block("en")}
{main_block("de")}
</main>

{footer()}
<script>{JS}</script>
</body>
</html>
'''
    out = os.path.join(HERE, "token.html")
    open(out, "w", encoding="utf-8").write(page)
    print("written:", out, len(page.encode()), "bytes")


if __name__ == "__main__":
    build()
