"""Curate + export Florida State Tree photos to WebP. Private info blurred, phone UI / intrusions cropped."""
from PIL import Image, ImageFilter, ImageOps
import imagehash, os, itertools
SRC='/workspace/ftree-research/photos/'
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','img'); os.makedirs(OUT,exist_ok=True)
KEEP=['f01','f03','f04','f05','f08','f09','f10','f11','f12','f13','f15','f16','g01','g02']
# blur boxes in ORIGINAL coords
BLUR={'f01':[(858,702,928,750)],          # house number
      'f13':[(38,832,158,918)]}            # customer name + house number on post sign
CROP={'f01':(0,395,946,1652),               # phone screenshot black bars
      'f03':(0,0,1536,1590),                # photographer shadow
      'f09':(0,0,1536,1540),                # finger / knee in frame
      'g02':(0,120,1500,2000)}              # roof eave bar
hs={}
for k in KEEP:
    im=ImageOps.exif_transpose(Image.open(SRC+k+'.jpg')).convert('RGB')
    for b in BLUR.get(k,[]):
        reg=im.crop(b)
        for _ in range(3): reg=reg.filter(ImageFilter.GaussianBlur(14))
        im.paste(reg,b[:2])
    if k in CROP: im=im.crop(CROP[k])
    hs[k]=imagehash.phash(im)
    big=im.copy(); big.thumbnail((1600,1600)); big.save(f'{OUT}/{k}.webp','WEBP',quality=80,method=6)
    sm=im.copy(); sm.thumbnail((720,720)); sm.save(f'{OUT}/{k}-s.webp','WEBP',quality=76,method=6)
    print(k, im.size)
for a,b in itertools.combinations(hs,2):
    if hs[a]-hs[b]<14: print('close',a,b,hs[a]-hs[b])
# OG base: g02 crop wide
og=Image.open(SRC+'f04.jpg').convert('RGB'); w,h=og.size
og=og.crop((0,int(h*.18),w,int(h*.18)+int(w*630/1200))).resize((1200,630)); og.save(f'{OUT}/og-base.jpg',quality=85)
print('done')
