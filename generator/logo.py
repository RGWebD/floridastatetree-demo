"""Hand-built vector logo for Florida State Tree & Landscaping (inspired by their oak mark; text converted to paths)."""
import os, math, random
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','brand'); os.makedirs(OUT,exist_ok=True)
INK='#1B2612'; MOSS='#3D5A22'; SAP='#BACD7F'; CREAM='#F4EFE2'; WOOD='#D8662C'
_f={}
def font(w):
    if w not in _f:
        _f[w]=instancer.instantiateVariableFont(TTFont(os.path.join(HERE,'fonts','Cinzel.ttf')),{'wght':w})
    return _f[w]
def text_path(s,w,size,x,y,track=0):
    f=font(w); gs=f.getGlyphSet(); cmap=f.getBestCmap(); sc=size/f['head'].unitsPerEm
    pen=SVGPathPen(gs); cx=x
    for ch in s:
        g=cmap.get(ord(ch))
        if g is None: continue
        gs[g].draw(TransformPen(pen,(sc,0,0,-sc,cx,y))); cx+=gs[g].width*sc+track
    return pen.getCommands(), cx-track-x
def text_w(s,w,size,track=0): return text_path(s,w,size,0,0,track)[1]

def tree(canopy, veins, trunk, simple=False):
    """Oak emblem in a 100x100 box. canopy/veins/trunk colours."""
    rnd=random.Random(7); out=[]
    # canopy: broad dome body + scalloped edge of overlapping lobes
    cx,cy,rx,ry=50,39,43,30
    lobes=[]
    n=16 if simple else 34
    for i in range(n):
        a=math.pi*(1.08+ (i/(n-1))*-1.16)  # from lower-left over the top to lower-right
        a=math.radians(200 - i*(220/(n-1)))
        r=(9.5 if simple else 5.6)+rnd.random()*(1.5 if simple else 4.2)
        x=cx+(rx-r*0.55)*math.cos(a); y=cy-(ry-r*0.55)*math.sin(a)
        lobes.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}"/>')
    body=f'<ellipse cx="{cx}" cy="{cy+1}" rx="{rx-4}" ry="{ry-3}"/>'
    # flat-ish underside lobes
    under=''.join(f'<circle cx="{x}" cy="{58+rnd.random()*1.5:.2f}" r="{(8 if simple else 6)+rnd.random()*1.5:.2f}"/>' for x in (20,33,50,67,80))
    shape=f'{body}{"".join(lobes)}{under}'
    out.append(f'<defs><clipPath id="cnp">{shape}<rect x="40" y="55" width="20" height="40"/></clipPath></defs>')
    out.append(f'<g fill="{canopy}">{shape}</g>')
    # trunk with root flare
    out.append(f'<path fill="{trunk}" d="M44.6 60 C45.2 70 44.6 78 41 84.5 C37.5 87 32 88.4 26 89.2 L74 89.2 C68 88.4 62.5 87 59 84.5 C55.4 78 54.8 70 55.4 60 Z"/>')
    out.append(f'<path fill="none" stroke="{trunk}" stroke-width="1.2" stroke-linecap="round" d="M22 90.2 H78"/>')
    # veins: recursive branches in the canopy
    segs=[]
    def br(x,y,ang,l,w,d):
        if d==0 or l<2.2: return
        x2=x+l*math.cos(ang); y2=y-l*math.sin(ang)
        mx=(x+x2)/2+rnd.uniform(-1.2,1.2); my=(y+y2)/2+rnd.uniform(-1.2,1.2)
        segs.append(f'<path d="M{x:.2f} {y:.2f} Q{mx:.2f} {my:.2f} {x2:.2f} {y2:.2f}" stroke-width="{w:.2f}"/>')
        k=2
        for j in range(k):
            na=ang+(0.5 if j==0 else -0.5)+rnd.uniform(-0.2,0.2)
            br(x2,y2,na,l*rnd.uniform(0.7,0.82),w*0.64,d-1)
    depth=3 if simple else 5
    br(50,66,math.pi/2,13,4.4 if simple else 3.8,depth)
    br(49,62,math.pi/2+1.05,15,2.8 if simple else 2.6,depth)
    br(51,62,math.pi/2-1.05,15,2.8 if simple else 2.6,depth)
    out.append(f'<g fill="none" stroke="{veins}" stroke-linecap="round" clip-path="url(#cnp)">{"".join(segs)}</g>')
    # trunk highlight (heartwood line)
    out.append(f'<path fill="{veins}" opacity=".9" d="M48.6 60 C49 70 48.4 78 46 85 L50.5 85 C51 77 51.4 70 51.4 60 Z"/>')
    return ''.join(out)

def emblem_svg(canopy,veins,trunk,bg=None,simple=False,pad=0):
    b=f'<rect width="100" height="100" rx="22" fill="{bg}"/>' if bg else ''
    s=1-pad*2/100
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{b}<g transform="translate({pad} {pad}) scale({s})">{tree(canopy,veins,trunk,simple)}</g></svg>'

def horizontal(fg,band,bandtxt,canopy,veins,trunk,tag=None):
    # emblem 0..100 then wordmark
    t1,w1=text_path('FLORIDA STATE',700,40,120,48,1.2)
    bw=text_w('TREE & LANDSCAPING LLC',600,15.5,2.2)
    band_w=w1
    tr=(band_w-bw)/2
    t2,_=text_path('TREE & LANDSCAPING LLC',600,15.5,120+tr,77.5,2.2)
    W=120+w1+6
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 100">'
            f'<g>{tree(canopy,veins,trunk)}</g><path fill="{fg}" d="{t1}"/>'
            f'<rect x="118" y="59" width="{band_w+4:.1f}" height="25" fill="{band}"/>'
            f'<path fill="{bandtxt}" d="{t2}"/></svg>')

def stacked(fg,band,bandtxt,canopy,veins,trunk,tagc):
    t1,w1=text_path('FLORIDA STATE',700,44,0,0,1.4)
    W=max(w1,300)+40; x1=(W-w1)/2
    t1,_=text_path('FLORIDA STATE',700,44,x1,186,1.4)
    bw=text_w('TREE & LANDSCAPING LLC',600,17,2.4); t2,_=text_path('TREE & LANDSCAPING LLC',600,17,(W-bw)/2,218,2.4)
    tg='QUALITY WORK · HONEST SERVICE · BEAUTIFUL RESULTS'
    tw=text_w(tg,500,9.6,1.4); t3,_=text_path(tg,500,9.6,(W-tw)/2,252,1.4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 264">'
            f'<g transform="translate({W/2-70} 0) scale(1.4)">{tree(canopy,veins,trunk)}</g>'
            f'<path fill="{fg}" d="{t1}"/><rect x="{x1-2:.1f}" y="198" width="{w1+4:.1f}" height="28" fill="{band}"/>'
            f'<path fill="{bandtxt}" d="{t2}"/><path fill="{tagc}" d="{t3}"/></svg>')

files={
 'emblem.svg':emblem_svg(MOSS,SAP,INK),
 'emblem-dark.svg':emblem_svg(SAP,INK,CREAM),
 'emblem-1c.svg':emblem_svg(INK,CREAM,INK),
 'favicon.svg':emblem_svg(SAP,INK,CREAM,bg=INK,simple=True,pad=8),
 'logo-horizontal.svg':horizontal(INK,MOSS,CREAM,MOSS,SAP,INK),
 'logo-horizontal-dark.svg':horizontal(CREAM,SAP,INK,SAP,INK,CREAM),
 'logo-horizontal-1c.svg':horizontal(INK,INK,CREAM,INK,CREAM,INK),
 'logo-stacked.svg':stacked(INK,MOSS,CREAM,MOSS,SAP,INK,MOSS),
 'logo-stacked-dark.svg':stacked(CREAM,SAP,INK,SAP,INK,CREAM,SAP),
}
for k,v in files.items(): open(os.path.join(OUT,k),'w').write(v)
sheet=f'''<html><body style="margin:0;font-family:sans-serif;background:#fff"><div style="display:grid;grid-template-columns:1fr 1fr;gap:0">
<div style="background:{CREAM};padding:40px"><img src="logo-horizontal.svg" style="height:90px"><br><br><img src="logo-stacked.svg" style="height:220px"></div>
<div style="background:{INK};padding:40px"><img src="logo-horizontal-dark.svg" style="height:90px"><br><br><img src="logo-stacked-dark.svg" style="height:220px"></div>
<div style="padding:40px"><img src="emblem.svg" style="height:140px"> <img src="emblem-1c.svg" style="height:140px"> <img src="favicon.svg" style="height:140px"> <img src="favicon.svg" style="height:32px"> <img src="favicon.svg" style="height:16px"> <img src="emblem.svg" style="height:32px"></div>
<div style="padding:40px;display:flex;gap:10px">{''.join(f'<div style="width:90px;height:90px;background:{c};color:{"#fff" if c in (INK,MOSS,WOOD) else "#000"};font:12px monospace;display:flex;align-items:end;padding:6px;box-sizing:border-box">{c}</div>' for c in (INK,MOSS,SAP,CREAM,WOOD))}</div>
</div></body></html>'''
open(os.path.join(OUT,'logo-sheet.html'),'w').write(sheet)
print('ok')
