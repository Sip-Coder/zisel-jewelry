"""Zisel store-counter mockup: navy gift bag + matching jewelry box on a boutique counter.
Base photo is AI-generated with no text (base_counter_blank.jpg). The bag/box blue is regraded to brand navy, then the real vector
artwork (card A front treatment + exact outlined logo, built from business-cards/src) is composited in perspective.
Run: cd /tmp && python3 <this file>"""
import sys, os, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE)
sys.path.insert(0,os.path.join(OUT,'..','business-cards','src')); sys.path.insert(0,HERE)
import build as card
from build import shapely_to_path, gradient, logo, EO, GOLD
from reportlab.pdfgen import canvas
from shapely.geometry import Polygon
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from comp import coeffs
card.MODE='rgb'
def ring(c,x0,y0,x1,y1,w,W,H):
    g=Polygon([(x0,y0),(x1,y0),(x1,y1),(x0,y1)]); r=g.difference(g.buffer(-w,join_style="mitre"))
    c.saveState(); c.clipPath(shapely_to_path(c,r),stroke=0,fill=0,fillMode=EO); gradient(c,0,H,W,0,GOLD); c.restoreState()
def face(path,W,H,band,gap,S=None,cy=None,inner=True,hair=.9):
    c=canvas.Canvas(path,pagesize=(W,H),initialFontName="ZOutline")
    ring(c,0,0,W,H,band,W,H); e=band+gap; ring(c,e,e,W-e,H-e,hair,W,H)
    if inner: e2=e+4.5; ring(c,e2,e2,W-e2,H-e2,.6,W,H)
    if S: logo(c,W/2,cy,S)
    c.showPage(); c.save()
face(os.path.join(HERE,'art_counter-bag-face.pdf'),300,395,11,7,62,395*.40)
face(os.path.join(HERE,'art_box-lid-front.pdf'),300,98,4,3,44,49,inner=False,hair=.6)
face(os.path.join(HERE,'art_box-lid-top.pdf'),300,300,9,7)
for n,src in (('cb_bag','art_counter-bag-face'),('cb_lidfront','art_box-lid-front'),('cb_lidtop','art_box-lid-top')):
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=pngalpha','-r700','-dGraphicsAlphaBits=4',f'-sOutputFile=/tmp/{n}.png',os.path.join(HERE,src+'.pdf')],check=True)

# ---- composite ----
P=Image.open(os.path.join(HERE,'base_counter_blank.jpg')).convert('RGB'); W,H=P.size
p=np.asarray(P).astype(float)/255
L0=p.mean(2,keepdims=True)
# 1) regrade royal blue -> Zisel navy (only the bag + box)
r,g,b=p[...,0],p[...,1],p[...,2]
wgt=np.clip((b-np.maximum(r,g)-0.06)/0.12,0,1)
obj=Image.new('L',(W,H),0); d=ImageDraw.Draw(obj)
d.polygon([(186,150),(240,154),(664,160),(686,676),(560,700),(254,734),(186,690)],fill=255)       # bag
BOX=[(567,567),(770,545),(935,585),(930,742),(702,782),(567,722)]
d.polygon(BOX,fill=255)
objm=np.asarray(obj.filter(ImageFilter.GaussianBlur(2))).astype(float)/255
wgt=(wgt*objm)[...,None]
navy=np.array([13,31,69])/255; blue_ref=np.array([0.20,0.27,0.55])  # typical lit bag colour -> brand navy
lum=p.mean(2,keepdims=True)/blue_ref.mean()
graded=np.clip(navy*lum*1.15,0,1)
p=p*(1-wgt)+graded*wgt
def layer(p, art, quad, occl=None, handle=None, texture=.3):
    A=Image.open(art).convert('RGBA'); aw,ah=A.size; ss=3
    Wb=A.transform((W*ss,H*ss),Image.PERSPECTIVE,coeffs([(x*ss,y*ss) for x,y in quad],[(0,0),(aw,0),(aw,ah),(0,ah)]),Image.BICUBIC).resize((W,H),Image.LANCZOS)
    a=np.asarray(Wb).astype(float)/255; rgb=a[...,:3]; al=a[...,3:4]
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(quad,fill=255); face=np.asarray(m)>0
    keep=np.ones((H,W),bool)
    if occl:
        o=Image.new('L',(W,H),0); ImageDraw.Draw(o).polygon(occl,fill=255); o=np.asarray(o.filter(ImageFilter.GaussianBlur(.8))).astype(float)[...,None]/255
        al=al*(1-o); keep&=o[...,0]<.5
    if handle is not None:
        hm=Image.fromarray((handle*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
        hA=np.asarray(hm).astype(float)[...,None]/255; al=al*(1-hA); keep&=handle<.5
    ref=np.median(L0[face&keep]); sh=np.clip(L0/ref,.6,1.45)
    shb=np.asarray(Image.fromarray((np.clip(sh/2,0,1)[...,0]*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(float)[...,None]/255*2
    sh=shb*(1-texture)+sh*texture
    lit=np.clip(rgb*sh,0,1)
    return p*(1-al)+lit*al
q=np.asarray(P).astype(float)/255
hm=((q[...,0]-q[...,2])>.12)&(q.mean(2)>.25); hm[:150]=False; hm[420:]=False; hm[:, :330]=False; hm[:, 580:]=False
p=layer(p,'/tmp/cb_bag.png',[(240,154),(664,160),(686,676),(254,732)],occl=BOX,handle=hm.astype(float))
# box lid top (frame only) and lid front (frame + logo); slight inset for the rounded lid edges
p=layer(p,'/tmp/cb_lidtop.png',[(571,568),(769,548),(927,586),(704,608)])
p=layer(p,'/tmp/cb_lidfront.png',[(704,615),(929,590),(926,655),(703,684)],texture=.4)
out=os.path.join(OUT,'zisel-counter-bag-and-box-mockup.png'); Image.fromarray((p*255).round().astype(np.uint8)).save(out)
Image.open(out).convert('RGB').save(out[:-4]+'.pdf',resolution=150); print('done')
