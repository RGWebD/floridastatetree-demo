#!/usr/bin/env python3
"""Static generator: python3 generator/build.py  -> writes the site into the repo root."""
import os, json, html, sys, math, random, shutil
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *
G = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(G, '..'))
BASE = os.environ.get('BASE', BASE)
VER = '7'
e = html.escape

I = {
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'msg':'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'left':'<path d="M19 12H5M11 6l-6 6 6 6"/>',
 'x':'<path d="M6 6l12 12M18 6L6 18"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'shield':'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'tag':'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
 'home':'<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
 'broom':'<path d="M14 4l6 6M17 7l-7 7M4 20c2-4 4-6 6-6l2 2c0 2-2 4-6 6z"/>',
 'list':'<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
 'star':'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 'leaf':'<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
 'saw':'<path d="M3 15l10-10 6 6-10 10z"/><path d="M6 12l2 2M9 9l2 2M12 6l2 2"/>',
 'storm':'<path d="M7 16a5 5 0 1 1 1-9.9A6 6 0 0 1 19 9a4 4 0 0 1-1 7.9"/><path d="M12 13l-2 4h3l-2 4"/>',
 'fb':'<path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V9H7v3.5h2V21h3.5v-8.5H15l.5-3.5h-3V7a1 1 0 0 1 1-1H15z"/>',
 'g':'<path d="M20 12.2c0-.6 0-1.2-.2-1.7H12v3.3h4.5a3.9 3.9 0 0 1-1.7 2.5v2h2.7c1.6-1.5 2.5-3.6 2.5-6.1z"/><path d="M12 20.5c2.3 0 4.2-.8 5.5-2.1l-2.7-2a5 5 0 0 1-7.5-2.7H4.6v2.1A8.5 8.5 0 0 0 12 20.5z"/><path d="M7.3 13.7a5 5 0 0 1 0-3.4V8.2H4.6a8.5 8.5 0 0 0 0 7.6z"/><path d="M12 6.9c1.3 0 2.5.4 3.4 1.3l2.5-2.5A8.5 8.5 0 0 0 4.6 8.2l2.7 2.1A5 5 0 0 1 12 6.9z"/>',
}
def ic(n, cls=''):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

_dims = {}
def dims(name):
    if name not in _dims: _dims[name] = Image.open(os.path.join(R, 'img', name)).size
    return _dims[name]
def img(k, alt, small=False, eager=False, cls='', sizes=None, style=''):
    f = f'{k}-s.webp' if small else f'{k}.webp'
    w, h = dims(f)
    ld = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    srcset = '' if small else f' srcset="img/{k}-s.webp {dims(k+"-s.webp")[0]}w, img/{k}.webp {w}w" sizes="{sizes or "(max-width:860px) 100vw, 50vw"}"'
    st = f' style="{style}"' if style else ''
    c = f' class="{cls}"' if cls else ''
    return f'<img src="img/{f}"{srcset} width="{w}" height="{h}" alt="{e(alt)}" {ld}{c}{st}>'

# ---------- tree rings (wobbly concentric paths) ----------
def ring_path(r, seed, wob=0.035, n=36, cx=0, cy=0):
    rnd = random.Random(seed); pts = []
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    for i in range(n):
        a = 2*math.pi*i/n
        rr = r*(1 + wob*math.sin(3*a+ph[0])*.6 + wob*math.sin(5*a+ph[1])*.3 + wob*math.sin(2*a+ph[2])*.5)
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[(i+1)%n], pts[(i+2)%n]
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6); c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + 'Z'
def rings_svg(count, maxr, cls, seed=1, wob=0.035, vb=None, extra=''):
    vb = vb or maxr*1.12
    ps = ''.join(f'<path d="{ring_path(maxr*(i+1)/count, seed*100+i, wob)}" style="--i:{i}"/>' for i in range(count))
    return f'<svg class="{cls}" viewBox="{-vb} {-vb} {2*vb} {2*vb}" aria-hidden="true" {extra}>{ps}</svg>'

PAGES = [('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('about.html','About'),('reviews.html','Reviews'),('contact.html','Contact')]
STAR5 = '<span class="stars" aria-label="5 out of 5 stars">' + ''.join('<i></i>' for _ in range(5)) + '</span>'
ADDR = f'{STREET}, {CITY}, {REGION} {ZIP}'

def head(page, title, desc, crumbs_ld, extra_ld=None, ogimg='og.jpg'):
    url = BASE + ('' if page == 'index.html' else page)
    lds = [business_ld()] + ([crumbs_ld] if crumbs_ld else []) + (extra_ld or [])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#1B2612">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(NAME)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/{ogimg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}img/{ogimg}">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="any"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,0..100;1,9..144,300..900,0..100&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={VER}">{ld}</head>'''

def business_ld():
    return {"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","additionalType":"https://en.wikipedia.org/wiki/Arborist",
      "@id":BASE+"#business","name":LEGAL,"alternateName":NAME,"slogan":TAGLINE,
      "description":"Licensed and insured tree service based in Belleview, Florida: tree removal, trimming, stump grinding, storm cleanup and emergency tree work, tree assessments and landscaping. Free estimates. Serving Marion County, Sumter County, Lady Lake and The Villages.",
      "url":BASE,"telephone":TEL,"image":BASE+"img/og.jpg","logo":BASE+"brand/logo-stacked.svg",
      "address":{"@type":"PostalAddress","streetAddress":STREET,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":GEO[0],"longitude":GEO[1]},
      "areaServed":[{"@type":"AdministrativeArea","name":"Marion County, FL"},{"@type":"AdministrativeArea","name":"Sumter County, FL"},{"@type":"City","name":"Lady Lake, FL"},{"@type":"Place","name":"The Villages, FL"}],
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}],
      "hasMap":MAPS,"sameAs":[FB,MAPS],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":str(REVIEWS),"bestRating":"5"},
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Tree & landscaping services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1],"description":s[3]}} for s in SVC]},
      "review":[{"@type":"Review","author":{"@type":"Person","name":r['name']},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":r['text']} for r in REVIEWS_LIST if not r.get('excerpt')]}

def crumbs(page, label):
    items = [{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
    if page != 'index.html': items.append({"@type":"ListItem","position":2,"name":label,"item":BASE+page})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def nav(page):
    links = ''.join(f'<li><a href="{p}"{" aria-current=page" if p==page else ""}>{l}</a></li>' for p,l in PAGES)
    mlinks = ''.join(f'<a class="mm-l" href="{p}"{" aria-current=page" if p==page else ""} style="--d:{i}"><span>0{i+1}</span>{l}</a>' for i,(p,l) in enumerate(PAGES))
    return f'''<a class="skip" href="#main">Skip to content</a><div class="vine" aria-hidden="true"><i></i></div><div class="grain" aria-hidden="true"></div>
<header class="nav"><div class="nav-in"><a class="brand" href="index.html" aria-label="{e(NAME)} home"><img src="brand/logo-horizontal-dark.svg" alt="{e(LEGAL)}" width="300" height="76"></a>
<nav aria-label="Main"><ul>{links}</ul></nav>
<div class="acts"><a class="btn ghost sm" href="sms:{TEL}">{ic('msg')}<span>Text</span></a><a class="btn wood sm mag" href="tel:{TEL}">{ic('phone')}<span>{PHONE}</span></a></div>
<button class="menu-btn" aria-expanded="false" aria-controls="mmenu" aria-label="Open menu"><i></i><i></i></button></div></header>
<div class="mmenu" id="mmenu" aria-hidden="true">{rings_svg(9,300,'mm-rings',seed=4)}<nav aria-label="Mobile">{mlinks}</nav>
<div class="mm-foot"><a class="btn wood" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn ghost" href="sms:{TEL}">{ic('msg')}Text for a free estimate</a></div></div>'''

def badge(cls=''):
    return f'<span class="live {cls}" data-live><i></i><span>Open 24 hours</span></span>'

def footer():
    links = ''.join(f'<li><a href="{p}">{l}</a></li>' for p,l in PAGES)
    return f'''<footer class="foot"><div class="wrap">
<div class="foot-top"><img src="brand/logo-stacked-dark.svg" alt="{e(LEGAL)}" width="300" height="230" loading="lazy" class="foot-logo">
<p class="foot-big">Call or text for a <em>free estimate.</em><a href="tel:{TEL}">{PHONE}</a></p></div>
<div class="foot-grid">
<div><h3>Pages</h3><ul>{links}</ul></div>
<div><h3>Visit / mail</h3><address>{LEGAL}<br>{STREET}<br>{CITY}, {REGION} {ZIP}</address><p><a href="{MAPS}" rel="noopener" target="_blank">Open in Google Maps</a></p></div>
<div><h3>Call or text</h3><p><a href="tel:{TEL}">{PHONE}</a><br><span class="muted">Also listed: <a href="tel:{TEL2}">{PHONE2}</a></span></p><p>{badge('sm')}</p><p class="muted">Hours: open 24 hours, 7 days (per Google)</p></div>
<div><h3>Service area</h3><p>{' · '.join(AREAS)} &amp; surrounding areas</p><p class="soc"><a href="{FB}" rel="noopener" target="_blank" aria-label="Facebook">{ic('fb')}</a><a href="{MAPS}" rel="noopener" target="_blank" aria-label="Google reviews">{ic('g')}</a></p></div>
</div>
<div class="foot-bot"><span>&copy; 2026 {e(LEGAL)} · Licensed &amp; insured</span><span>{e(TAGLINE)}</span></div></div></footer>
<div class="mbar"><a href="tel:{TEL}" class="mb-call">{ic('phone')}Call now</a><a href="sms:{TEL}" class="mb-text">{ic('msg')}Text us</a></div>
<div class="demo" role="note"><span>Design preview by <b>RGWebD</b></span><button aria-label="Dismiss design preview note">{ic('x')}</button></div>
<script src="script.js?v={VER}" defer></script></body></html>'''

def page_hero(eyebrow, h1_lines, lede, photo, alt, label, pos='50% 50%'):
    h = ''.join(f'<span class="ln"><span>{l}</span></span>' for l in h1_lines)
    return f'''<section class="phero" aria-labelledby="ph-h"><div class="wrap phero-in">
<div class="ph-copy"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>
<span class="eyebrow">{eyebrow}</span><h1 class="h1 split" id="ph-h">{h}</h1><p class="lede rv">{lede}</p>
<div class="cta-row rv d1"><a class="btn wood mag" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn line" href="sms:{TEL}">{ic('msg')}Text for a free estimate</a></div></div>
<figure class="ph-photo rv">{rings_svg(7,260,'ph-rings',seed=len(label))}<div class="ph-frame">{img(photo, alt, eager=True, sizes="(max-width:860px) 100vw, 46vw", style=f"object-position:{pos}")}</div></figure>
</div></section>'''

def cta_band(title='Got a tree that needs to go?', sub='Call or text for a free estimate. Licensed &amp; insured, references available on request.'):
    return f'''<section class="cta" aria-labelledby="cta-h">{rings_svg(16,520,'cta-rings draw',seed=9,wob=.05)}<div class="wrap cta-in">
<span class="eyebrow light rv">Free estimates</span><h2 class="h2 split" id="cta-h"><span class="ln"><span>{title}</span></span></h2>
<p class="lede rv">{sub}</p><div class="cta-row rv d1"><a class="btn wood xl mag" href="tel:{TEL}">{ic('phone')}{PHONE}</a><a class="btn ghost xl" href="sms:{TEL}">{ic('msg')}Text a photo of the tree</a></div></div></section>'''

def leaves():
    shapes = ''.join(f'<span class="leaf" style="--x:{x}%;--d:{d}s;--t:{t}s;--s:{s}"></span>' for x,d,t,s in [(8,0,14,1),(22,5,17,.7),(41,2,15,.9),(63,8,19,.6),(78,3,16,1.1),(90,10,18,.8),(52,12,21,.7)])
    return f'<div class="leaves" aria-hidden="true">{shapes}</div>'

def rv_cards(full=False):
    out = []
    for r in REVIEWS_LIST:
        tag = '<span class="rv-ex">Excerpt · <a href="'+MAPS+'" rel="noopener" target="_blank">read in full on Google</a></span>' if r.get('excerpt') else ''
        out.append(f'<figure class="slide"><blockquote><p>\u201c{e(r["text"] if full else r["pull"])}\u201d</p></blockquote><figcaption>{STAR5}<b>{e(r["name"])}</b><span>{e(r["meta"])} · Google</span>{tag if full else ""}</figcaption></figure>')
    return out

# ---------------- pages ----------------
def home():
    p = 'index.html'
    title = f'{NAME} | Tree Removal, Trimming & Stump Grinding · Belleview, FL'
    desc = f'Licensed & insured tree service in Belleview & Summerfield, FL. Tree removal, trimming, stump grinding, storm cleanup and landscaping for Marion County, Sumter County, Lady Lake and The Villages. 5.0★ on Google. Free estimates: {PHONE}.'
    loader = f'''<div class="loader" aria-hidden="true"><div class="ld-half l"></div><div class="ld-half r"></div><div class="ld-mid">{rings_svg(11,150,'ld-rings',seed=3,wob=.05)}<img src="brand/emblem-dark.svg" alt="" width="120" height="120" class="ld-em"></div></div>'''
    pins = [('22%','62%','Aerial lift','Towable lift reaching up into the canopy.'),('52%','22%','Live oak','A big Florida live oak hung with Spanish moss.'),('70%','80%','Ground crew','Crew on the ground, ready to drag brush and clean up.')]
    pinh = ''.join(f'<button class="pin" style="left:{x};top:{y}" aria-expanded="false" aria-label="{t}: {d}">{ic("plus")}<span class="pin-tip" role="tooltip"><b>{t}</b>{d}</span></button>' for x,y,t,d in pins)
    svc_cards = ''.join(f'''<a class="scard tilt rv d{i%3}" href="services.html#{k}"><div class="sc-img">{img(ph, alt, small=True)}</div><div class="sc-body"><span class="sc-n">0{i+1}</span><h3>{t}</h3><p>{short}</p><span class="sc-go">Learn more {ic('arrow')}</span></div></a>'''
        for i,(k,t,short,long,ph,alt) in enumerate([s if s[0]!='storm' else ('storm',s[1],s[2],s[3],'f10','Trunk cut down to a tall stub beside a house, with branches and wood chips on the lawn') for s in SVC]))
    # replace storm card photo (g02 used in storm band on home) and removal card photo distinct
    marq_items = ['Tree Removal','Trimming &amp; Pruning','Stump Grinding','Storm Cleanup','Emergency Tree Work','Tree Assessments','Landscaping','Palms','Free Estimates']
    m1 = ''.join(f'<span>{t}</span><i>{ic("leaf")}</i>' for t in marq_items)
    gauges = [('5.0','5','Star rating on Google','.1',1),('22','22','Google reviews','1',0),('24','24','Hours a day, per Google','1',0),('4','4','Areas served by name','1',0)]
    gh = ''.join(f'''<div class="gauge rv d{i}"><div class="g-ring">{rings_svg(int(float(to)) if float(to)>1 else 5, 100, 'g-svg', seed=20+i, wob=.06)}<span class="g-val" data-to="{to}" data-dec="{1 if dec=='.1' else 0}">0</span></div><p>{lab}</p></div>''' for i,(v,to,lab,dec,_) in enumerate(gauges))
    rail = ''.join(f'<figure class="rail-i">{img(k, CAP[k][0], small=True)}<figcaption>{CAP[k][0]}</figcaption></figure>' for k in ['f08','f15','f12','g01','f11'])
    slides = ''.join(rv_cards())
    why = [('shield','Licensed &amp; insured','Licensed &amp; insured, with references available on request.'),
           ('tag','Free estimates','Call or text and we\u2019ll come take a look. Customers say our quote beat the others.'),
           ('home','Careful over the house','Limbs over roofs, garages and lanais come down without damage.'),
           ('broom','We clean up','We stay to get the debris up, and blow off roofs and gutters.')]
    whyh = ''.join(f'<div class="why-i rv d{i}"><span class="why-ic">{ic(a)}</span><h3>{b}</h3><p>{c}</p></div>' for i,(a,b,c) in enumerate(why))
    body = f'''{head(p,title,desc,crumbs(p,'Home'))}<body class="home">{loader}{nav(p)}<main id="main">
<section class="hero" aria-labelledby="h-h"><div class="dapple" aria-hidden="true"><i></i><i></i><i></i><i></i></div>{leaves()}
<div class="bigtype" aria-hidden="true">TIMBER</div>
<div class="wrap hero-in"><div class="h-copy">
<span class="eyebrow light">Tree service · Belleview &amp; Summerfield, FL</span>
<h1 class="h1 split" id="h-h"><span class="ln"><span>From the crown</span></span><span class="ln"><span>down to the <em>stump.</em></span></span></h1>
<p class="lede">Tree removal, trimming, stump grinding, storm cleanup and landscaping across Marion County, Sumter County, Lady Lake and The Villages. {TAGLINE.replace('. ','.&nbsp;')}</p>
<div class="cta-row"><a class="btn wood xl mag" href="tel:{TEL}">{ic('phone')}Free estimate: {PHONE}</a><a class="btn ghost xl" href="sms:{TEL}">{ic('msg')}Text us</a></div>
<a class="trust" href="reviews.html"><span class="t-score">{RATING}</span>{STAR5}<span class="t-txt"><b>{REVIEWS} Google reviews</b>5.0 average on Google</span>{badge()}</a>
</div>
<div class="h-art">{rings_svg(10,330,'h-rings',seed=2,wob=.04)}<figure class="arch">{img('f04','Aerial lift raised into a large live oak with Spanish moss beside a home, crew member on the lawn', eager=True, sizes="(max-width:860px) 100vw, 44vw")}{pinh}</figure>
<figure class="polaroid">{img('f03','Crew member with a chainsaw behind two big fresh-cut tree rounds', small=True)}<figcaption>Fresh cut, clean rounds</figcaption></figure></div>
</div></section>

<section class="marq" aria-label="Services"><div class="mq r1"><div class="mq-t">{m1}{m1}</div></div><div class="mq r2" aria-hidden="true"><div class="mq-t">{m1}{m1}</div></div></section>

<section class="sec why" aria-labelledby="why-h"><div class="wrap why-in">
<div class="why-head"><span class="eyebrow rv">Why folks call Harley\u2019s crew</span><h2 class="h2 split" id="why-h"><span class="ln"><span>Honest service,</span></span><span class="ln"><span><em>start to stump.</em></span></span></h2>
<p class="lede rv d1">A local, licensed &amp; insured tree crew from the Belleview and Summerfield area. We show up, do the job right, and leave your yard cleaner than we found it.</p>
<a class="tlink rv d2" href="about.html">Meet the crew {ic('arrow')}</a></div>
<div class="why-grid">{whyh}</div></div></section>

<section class="sec rings-sec" aria-labelledby="num-h"><div class="wrap"><div class="rs-head"><span class="eyebrow light rv">By the numbers</span><h2 class="h2 split" id="num-h"><span class="ln"><span>Count the <em>rings.</em></span></span></h2><p class="lede rv d1">Every ring below is one unit of the real number, straight from Google and Facebook.</p></div><div class="gauges">{gh}</div></div></section>

<section class="sec svc" aria-labelledby="svc-h"><div class="wrap"><div class="sec-head"><div><span class="eyebrow rv">What we do</span><h2 class="h2 split" id="svc-h"><span class="ln"><span>Six ways we take</span></span><span class="ln"><span>care of your <em>trees.</em></span></span></h2></div><a class="btn line rv" href="services.html">All services {ic('arrow')}</a></div>
<div class="svc-grid">{svc_cards}</div></div></section>

<section class="storm" aria-labelledby="st-h"><div class="rain" aria-hidden="true"></div><div class="flash" aria-hidden="true"></div><div class="wrap storm-in">
<figure class="st-photo rv">{img('g02','Aerial lift up among tall oaks during a large removal, with brush piles and a tracked loader below', sizes="(max-width:860px) 100vw, 42vw")}<figcaption>Photo shared by a customer on Google</figcaption></figure>
<div class="st-copy"><span class="eyebrow light rv">Storm cleanup &amp; emergency tree work</span><h2 class="h2 split" id="st-h"><span class="ln"><span>When the storm</span></span><span class="ln"><span>passes, <em>we roll.</em></span></span></h2>
<p class="lede rv">After the hurricane, our crew drove up to Navarre, Florida to help homeowners: cutting hazardous trees, removing fallen ones and hauling off damaged fencing, while keeping our prices fair.</p>
<blockquote class="st-q rv d1">\u201cThis is why we do what we do!\u201d<cite>From our Facebook page</cite></blockquote>
<div class="cta-row rv d2"><a class="btn wood mag" href="tel:{TEL}">{ic('phone')}Storm damage? Call {PHONE}</a></div></div></div></section>

<section class="sec revs" aria-labelledby="rv-h"><div class="wrap"><div class="sec-head"><div><span class="eyebrow rv">{RATING} stars · {REVIEWS} Google reviews</span><h2 class="h2 split" id="rv-h"><span class="ln"><span>Neighbors say it <em>best.</em></span></span></h2></div><a class="btn line rv" href="reviews.html">Read the reviews {ic('arrow')}</a></div>
<div class="car rv" data-car><div class="car-track">{slides}</div><div class="car-ctl"><button class="car-b prev" aria-label="Previous review">{ic('left')}</button><div class="car-dots"></div><button class="car-b next" aria-label="Next review">{ic('arrow')}</button></div></div></div></section>

<section class="sec railsec" aria-labelledby="rl-h"><div class="wrap sec-head"><div><span class="eyebrow rv">Out on the job</span><h2 class="h2 split" id="rl-h"><span class="ln"><span>Drag through a few <em>jobs.</em></span></span></h2></div><a class="btn line rv" href="work.html">See all our work {ic('arrow')}</a></div>
<div class="rail" tabindex="0" aria-label="Job photos, scroll or drag sideways"><div class="rail-t">{rail}</div></div>
<div class="wrap teasers">{''.join(f'<a class="teaser rv d{i}" href="{h}"><span>{a}</span><b>{b}</b>{ic("arrow")}</a>' for i,(h,a,b) in enumerate([('about.html','About','Harley &amp; the crew'),('work.html','Our Work','Photos from real jobs'),('contact.html','Contact','Free estimate &amp; FAQ')]))}</div></section>
{cta_band()}
</main>{footer()}'''
    return body

def services():
    p='services.html'
    title=f'Tree Services: Removal, Trimming, Stump Grinding & Storm Cleanup | {NAME}'
    desc=f'Tree removal, trimming & pruning, stump grinding, storm cleanup & emergency tree work, tree assessments and landscaping in Marion County, Sumter County, Lady Lake & The Villages. Free estimates: {PHONE}.'
    secs=''
    for i,(k,t,short,long,ph,alt) in enumerate(SVC):
        secs+=f'''<section class="svc-row{' flip' if i%2 else ''}" id="{k}" aria-labelledby="s-{k}"><figure class="sr-photo rv">{img(ph,alt,sizes="(max-width:860px) 100vw, 46vw")}<span class="sr-n" aria-hidden="true">0{i+1}</span></figure>
<div class="sr-copy"><span class="eyebrow rv">Service 0{i+1}</span><h2 class="h2 split" id="s-{k}"><span class="ln"><span>{t}</span></span></h2><p class="lede rv">{long}</p>
<a class="btn line rv d1" href="contact.html#estimate">Get a free estimate {ic('arrow')}</a></div></section>'''
    steps=[('Call or text','Reach us at '+PHONE+' (or text a photo of the tree). Estimates are free.'),
           ('We take a look','We walk the property with you and talk through what the tree needs: trim, remove or leave it be.'),
           ('Notice, then crew','Customers mention we show up with plenty of notice and get right to work, with the lift, saws and grinder the job needs.'),
           ('Cut, grind, haul','Limbs come down carefully, stumps get ground, and the wood and brush get hauled off.'),
           ('Clean finish','We stay to get the debris up, and blow off roofs and gutters before we go.')]
    sh=''.join(f'<li class="step rv"><span class="st-dot">{i+1}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i,(a,b) in enumerate(steps))
    body=f'''{head(p,title,desc,crumbs(p,'Services'),[{"@context":"https://schema.org","@type":"ItemList","name":"Tree services","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Service","name":s[1],"description":s[3],"provider":{"@id":BASE+"#business"},"areaServed":AREAS}} for i,s in enumerate(SVC)]}])}<body>{nav(p)}<main id="main">
{page_hero('Services','Tree work, <em>top to bottom.</em>'.split('|') if False else ['Tree work,','<em>top to bottom.</em>'],'Removal, trimming, stump grinding, storm cleanup, tree assessments and landscaping. Licensed &amp; insured, with free estimates across Marion County, Sumter County, Lady Lake and The Villages.','f08','Looking up through tall pines with an aerial lift working among the trunks','Services','50% 40%')}
<nav class="jump wrap" aria-label="Jump to a service">{''.join(f'<a href="#{s[0]}">{s[1]}</a>' for s in SVC)}</nav>
<div class="wrap svc-rows">{secs}</div>
<section class="sec how" aria-labelledby="how-h"><div class="wrap how-in"><div class="how-head"><span class="eyebrow light rv">How it works</span><h2 class="h2 split" id="how-h"><span class="ln"><span>From first call</span></span><span class="ln"><span>to <em>clean yard.</em></span></span></h2><p class="lede rv">Five simple steps. No pressure, no surprises.</p></div>
<ol class="steps"><svg class="trunk" viewBox="0 0 40 1000" preserveAspectRatio="none" aria-hidden="true"><path d="M20 0 C 8 120, 32 240, 20 360 S 8 600, 20 720 S 32 900, 20 1000"/></svg>{sh}</ol></div></section>
{cta_band('Not sure what the tree needs?','Ask for a tree assessment. We\u2019ll tell you honestly whether to trim, remove or leave it.')}
</main>{footer()}'''
    return body

def work():
    p='work.html'
    title=f'Our Work: Tree Removal, Trimming & Landscaping Photos | {NAME}'
    desc='Photos from real Florida State Tree & Landscaping jobs: big removals with the aerial lift, trimming over homes, stump grinding, sod and landscaping.'
    order=['g02','f16','f05','f01','f11','f10','f08','f12','f03','f15','f13','f09','g01','f04']
    filt=[('all','All'),('removal','Removal'),('trimming','Trimming'),('stumps','Stumps'),('landscape','Landscaping')]
    fb=''.join(f'<button class="fbtn" data-f="{a}" aria-pressed="{"true" if a=="all" else "false"}">{b}</button>' for a,b in filt)
    items=''.join(f'<figure class="gi rv" data-tag="{CAP[k][1]}"><button class="gi-b" data-full="img/{k}.webp" data-cap="{e(CAP[k][0])}" aria-label="Open photo: {e(CAP[k][0])}">{img(k,CAP[k][0],small=True)}</button><figcaption>{CAP[k][0]}</figcaption></figure>' for k in order)
    lb=f'''<div class="lbx" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden><button class="lbx-x" aria-label="Close">{ic('x')}</button><button class="lbx-p" aria-label="Previous photo">{ic('left')}</button><figure><img alt=""><figcaption></figcaption></figure><button class="lbx-n" aria-label="Next photo">{ic('arrow')}</button></div>'''
    body=f'''{head(p,title,desc,crumbs(p,'Our Work'))}<body>{nav(p)}<main id="main">
{page_hero('Our work',['Real jobs,','<em>real yards.</em>'],'Every photo here comes from our own Facebook page or from customers on Google. Tap any photo to see it big.','f15','Towable aerial lift trailer set up beside a tall tree snag on a clear day','Our Work','50% 45%')}
<section class="sec gal" aria-label="Photo gallery"><div class="wrap"><div class="filters" role="group" aria-label="Filter photos">{fb}</div><div class="grid-g">{items}</div></div></section>
{cta_band('Want results like these?')}
</main>{lb}{footer()}'''
    return body

def about():
    p='about.html'
    title=f'About Harley Roth & the Crew | {NAME}, Belleview FL'
    desc=f'{LEGAL} is a licensed & insured tree service from the Belleview and Summerfield area, run by Harley Roth. Serving Marion County, Sumter County, Lady Lake and The Villages.'
    areas=''.join(f'<li class="rv d{i}"><span>{ic("pin")}</span>{a}</li>' for i,a in enumerate(AREAS+['&amp; surrounding areas']))
    vals=[('Quality work.','Big removals or a single limb over the garage, done carefully and done right.'),('Honest service.','Free estimates, fair prices and straight answers about what your tree needs.'),('Beautiful results.','We clean up, haul off and can finish the yard with sod and landscaping.')]
    vh=''.join(f'<div class="val rv d{i}"><span class="val-n">0{i+1}</span><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(vals))
    body=f'''{head(p,title,desc,crumbs(p,'About'))}<body>{nav(p)}<main id="main">
{page_hero('About us',['Local roots,','<em>honest work.</em>'],f'A licensed &amp; insured tree crew from the Belleview and Summerfield area, led by {OWNER}. Call Harley at {PHONE} for all your tree and landscaping needs.','f03','Crew member with a chainsaw behind two big fresh-cut tree rounds','About','50% 60%')}
<section class="sec story" aria-labelledby="sy-h"><div class="wrap story-in"><div class="story-copy"><span class="eyebrow rv">Our story</span><h2 class="h2 split" id="sy-h"><span class="ln"><span>Quality work.</span></span><span class="ln"><span>Honest service.</span></span><span class="ln"><span><em>Beautiful results.</em></span></span></h2>
<p class="lede rv">That\u2019s the line on our logo, and it\u2019s how we run every job. {OWNER} and the crew handle tree removal, trimming, stump grinding, storm cleanup, tree assessments and full landscaping for homeowners around Marion and Sumter counties.</p>
<p class="rv">Customers tell us the same things again and again: we show up when we say we will, we\u2019re careful around the house, our pricing beats the other estimates, and we don\u2019t leave until the debris is cleaned up. References are available on request.</p></div>
<div class="story-art"><figure class="st-a1 rv">{img('f04','Aerial lift raised into a large live oak with Spanish moss beside a home',small=True)}</figure><figure class="st-a2 rv d1">{img('f11','Front yard with planting beds, palms and large shade trees',small=True)}</figure></div></div></section>
<section class="sec vals-sec" aria-label="Our values"><div class="wrap vals">{vh}</div></section>
<section class="storm" aria-labelledby="nv-h"><div class="rain" aria-hidden="true"></div><div class="flash" aria-hidden="true"></div><div class="wrap storm-in">
<figure class="st-photo rv">{img('f16','Aerial lift and tractor working on a tall trunk being taken down in sections',sizes="(max-width:860px) 100vw, 42vw")}</figure>
<div class="st-copy"><span class="eyebrow light rv">Navarre, FL</span><h2 class="h2 split" id="nv-h"><span class="ln"><span>We went where</span></span><span class="ln"><span>help was <em>needed.</em></span></span></h2>
<p class="lede rv">After the hurricane, we traveled to Navarre, Florida to help homeowners recover: cutting hazardous trees, removing fallen trees and hauling away damaged fencing, all while keeping our prices fair. As we put it on Facebook: \u201cThis is why we do what we do!\u201d</p></div></div></section>
<section class="sec area" aria-labelledby="ar-h"><div class="wrap area-in"><div><span class="eyebrow rv">Service area</span><h2 class="h2 split" id="ar-h"><span class="ln"><span>Where we <em>work.</em></span></span></h2><p class="lede rv">Based at {ADDR}, near Summerfield. We serve:</p><ul class="areas">{areas}</ul></div>
<div class="map rv"><iframe title="Map of {e(NAME)} in Belleview, FL" src="https://www.google.com/maps?q={STREET.replace(' ','+')},+{CITY},+{REGION}+{ZIP}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>
{cta_band()}
</main>{footer()}'''
    return body

def reviews():
    p='reviews.html'
    title=f'Reviews: {RATING}★ from {REVIEWS} Google Reviews | {NAME}'
    desc=f'{NAME} is rated {RATING} out of 5 from {REVIEWS} Google reviews. Read what homeowners say about our tree trimming, removal and cleanup.'
    cards=''
    for i,r in enumerate(REVIEWS_LIST):
        ex = f'<p class="rc-ex">Excerpt; Google shortens this review. <a href="{MAPS}" rel="noopener" target="_blank">Read it in full on Google</a>.</p>' if r.get('excerpt') else ''
        cards+=f'<article class="rcard rv d{i%3}"><span class="rc-q" aria-hidden="true">\u201c</span>{STAR5}<blockquote><p>{e(r["text"])}</p></blockquote>{ex}<footer><b>{e(r["name"])}</b><span>{e(r["meta"])} · via Google</span></footer></article>'
    snip=''.join(f'<li class="rv d{i}">\u201c{e(s)}\u201d</li>' for i,s in enumerate(SNIPPETS))
    body=f'''{head(p,title,desc,crumbs(p,'Reviews'))}<body>{nav(p)}<main id="main">
{page_hero(f'{RATING} stars · {REVIEWS} Google reviews',['Don\u2019t take','<em>our word</em> for it.'],'Here are reviews quoted word for word from our Google listing. Every review shown is five stars.','f09','A full, leafy shade tree in a front yard in summer','Reviews','50% 35%')}
<section class="sec rscore" aria-label="Rating summary"><div class="wrap rs-in"><div class="big-score rv"><span class="bs-n" data-to="5.0" data-dec="1">0</span>{STAR5}<p>{REVIEWS} reviews on Google</p></div>
<div class="rs-side rv d1"><h2 class="h3">What reviewers bring up most</h2><ul class="chips">{''.join(f'<li>{a}<b>{b}</b></li>' for a,b in [('Trimming',8),('Pricing',6),('Stump',5),('Palm trees',4),('Sod',2),('Cleanliness',2)])}</ul><p class="muted">Topic counts as shown on Google.</p><a class="btn line" href="{MAPS}" rel="noopener" target="_blank">{ic('g')}See all reviews on Google</a></div></div></section>
<section class="sec" style="padding-top:0" aria-label="Customer reviews"><div class="wrap rgrid">{cards}</div></section>
<section class="sec snips" aria-labelledby="sn-h"><div class="wrap"><span class="eyebrow light rv">Highlights from more Google reviews</span><h2 class="sr-only" id="sn-h">Review highlights</h2><ul class="snip">{snip}</ul></div></section>
{cta_band('Ready to be our next 5-star yard?')}
</main>{footer()}'''
    return body

FAQ = [
 ('Are estimates free?', f'Yes. Call or text {PHONE} for a free estimate. Texting a photo of the tree is a great way to start.'),
 ('Are you licensed and insured?', 'Yes, Florida State Tree & Landscaping LLC is licensed and insured. References are available on request.'),
 ('What areas do you serve?', 'We\u2019re based in Belleview, near Summerfield, and serve Marion County, Sumter County, Lady Lake, The Villages and the surrounding areas.'),
 ('Do you handle storm damage and emergency tree work?', 'Yes. Storm cleanup and emergency tree work is one of our core services, including hazardous and fallen trees. Our Google listing shows us as open 24 hours.'),
 ('Do you clean up after the job?', 'Yes. Reviewers mention the crew stays to get all the debris up, hauls it away, and even blows debris off roofs and gutters.'),
 ('Do you work on palm trees?', 'Yes. Palms come up often in our reviews, from trimming to removal. One homeowner had us remove five palms and three pines over the years.'),
 ('What services do you offer?', 'Tree removal, tree trimming and pruning, stump grinding, storm cleanup and emergency tree work, tree assessments, and landscaping, including sod.'),
 ('What phone number should I use?', f'Our main line is {PHONE}. Our Facebook page also lists {PHONE2}. You can call or text either one.'),
]
def contact():
    p='contact.html'
    title=f'Contact & Free Estimates | {NAME} · {PHONE}'
    desc=f'Call or text {PHONE} for a free tree service estimate in Belleview, Summerfield, Marion County, Sumter County, Lady Lake and The Villages. Open 24 hours per Google.'
    faqh=''.join(f'<details class="faq rv"><summary><span>{q}</span><i aria-hidden="true"></i></summary><p>{a}</p></details>' for q,a in FAQ)
    opts=''.join(f'<option>{s[1]}</option>' for s in SVC)
    faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    body=f'''{head(p,title,desc,crumbs(p,'Contact'),[faq_ld])}<body>{nav(p)}<main id="main">
{page_hero('Contact &amp; free estimates',['Let\u2019s talk','<em>trees.</em>'],f'Call or text {PHONE} any time. Google lists us as open 24 hours. Fill in the form below and it opens a text message to us, ready to send.','f12','A palm set in a fresh rock-ringed planting bed in a front yard','Contact','50% 55%')}
<section class="sec contact" id="estimate" aria-labelledby="ct-h"><div class="wrap ct-in">
<div class="ct-info"><h2 class="h2 split" id="ct-h"><span class="ln"><span>Reach the <em>crew.</em></span></span></h2>
<a class="ct-line rv" href="tel:{TEL}"><span>{ic('phone')}</span><div><small>Call or text (main)</small><b>{PHONE}</b></div></a>
<a class="ct-line rv" href="tel:{TEL2}"><span>{ic('msg')}</span><div><small>Also listed on Facebook</small><b>{PHONE2}</b></div></a>
<a class="ct-line rv" href="{MAPS}" rel="noopener" target="_blank"><span>{ic('pin')}</span><div><small>Address</small><b>{ADDR}</b></div></a>
<div class="ct-line rv"><span>{ic('clock')}</span><div><small>Hours</small><b>Open 24 hours, 7 days</b>{badge('sm')}</div></div>
<p class="muted rv">No email listed. The fastest way to reach us is a call or text.</p></div>
<form class="ct-form rv" data-sms="{TEL}" novalidate><h3>Request a free estimate</h3>
<div class="fr"><label>Your name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel" required></label></div>
<label>Town or address<input name="where" autocomplete="street-address" placeholder="e.g. Summerfield, The Villages"></label>
<label>What do you need?<select name="svc">{opts}<option>Something else</option></select></label>
<label>Tell us about the tree(s)<textarea name="msg" rows="4" placeholder="How many trees, how big, anything near the house or lines?"></textarea></label>
<button class="btn wood xl mag" type="submit">{ic('msg')}Open text message</button><p class="muted small">This opens your phone\u2019s messaging app with the details filled in. Nothing is sent until you hit send.</p></form>
</div></section>
<section class="sec faqs" aria-labelledby="fq-h"><div class="wrap faq-in"><div><span class="eyebrow rv">FAQ</span><h2 class="h2 split" id="fq-h"><span class="ln"><span>Good <em>questions.</em></span></span></h2></div><div class="faq-list">{faqh}</div></div></section>
<section class="sec mapsec" aria-label="Map"><div class="wrap"><div class="map wide rv"><iframe title="Map of {e(NAME)} in Belleview, FL" src="https://www.google.com/maps?q={STREET.replace(' ','+')},+{CITY},+{REGION}+{ZIP}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>
</main>{footer()}'''
    return body

def notfound():
    b = '/floridastatetree-demo/'
    s = f'''{head('404.html','Page not found | '+NAME,'This page could not be found.',None)}<body class="nf">{nav('404.html')}<main id="main"><section class="nf-in"><div class="wrap">{rings_svg(12,260,'nf-rings draw',seed=12,wob=.05)}<span class="eyebrow">404</span><h1 class="h1">This branch <em>broke off.</em></h1><p class="lede">The page you\u2019re looking for isn\u2019t here. Head back home or give us a call.</p><div class="cta-row"><a class="btn wood" href="index.html">Back to home</a><a class="btn line" href="tel:{TEL}">{ic('phone')}{PHONE}</a></div></div></section></main>{footer()}'''
    s = s.replace('<head><meta charset="utf-8">', f'<head><meta charset="utf-8"><base href="{b}">',1).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"',1)
    return s

def main():
    out = {'index.html':home(),'services.html':services(),'work.html':work(),'about.html':about(),'reviews.html':reviews(),'contact.html':contact(),'404.html':notfound()}
    for k,v in out.items(): open(os.path.join(R,k),'w').write(v)
    shutil.copy(os.path.join(G,'styles.css'), os.path.join(R,'styles.css')); shutil.copy(os.path.join(G,'script.js'), os.path.join(R,'script.js'))
    open(os.path.join(R,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    urls=''.join(f'<url><loc>{BASE}{"" if p=="index.html" else p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="index.html" else "0.8"}</priority></url>' for p,_ in PAGES)
    open(os.path.join(R,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    llm=f"""# {LEGAL}
> Licensed and insured tree service based in Belleview, Florida (Summerfield area), led by {OWNER}. Tree removal, trimming, stump grinding, storm cleanup and emergency tree work, tree assessments and landscaping. Free estimates. Rated {RATING}/5 from {REVIEWS} Google reviews. Listed on Google as open 24 hours.

- Phone (call or text): {PHONE} (main). Facebook also lists {PHONE2}.
- Address: {ADDR}
- Hours: Open 24 hours, 7 days (per Google Business Profile)
- Service area: {', '.join(AREAS)} and surrounding areas
- Licensed & insured. Free estimates. References available upon request.
- Tagline: "{TAGLINE}"
- Storm work: after a hurricane the crew traveled to Navarre, FL to cut hazardous trees, remove fallen trees and haul damaged fencing.
- Email / website: none published.

## Services
""" + ''.join(f"- {html.unescape(s[1])}: {html.unescape(s[3])}\n" for s in SVC) + f"""
## Pages
- [Home]({BASE}): overview, why choose us, services, storm work, reviews
- [Services]({BASE}services.html): each service and how a job works
- [Our Work]({BASE}work.html): photo gallery of real jobs
- [About]({BASE}about.html): Harley Roth and the crew, Navarre storm trip, service area
- [Reviews]({BASE}reviews.html): Google reviews quoted word for word
- [Contact]({BASE}contact.html): phone, text form, hours, address, FAQ
- [Google listing]({MAPS})
- [Facebook]({FB})
"""
    open(os.path.join(R,'llms.txt'),'w').write(llm)
    print('built', len(out), 'pages')
if __name__ == '__main__': main()
