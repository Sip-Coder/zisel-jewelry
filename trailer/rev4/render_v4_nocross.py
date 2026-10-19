import sys
import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageChops
A='../assets/'; P='../../collection/photos/'; A2='./'
W,H,FPS,T=1080,1920,30,31.0
ld=lambda n:Image.open(A+n+'.png').convert('RGBA')
bg,card,logo,logosm,hook,end=[ld(n) for n in 'bg card logo logosm hook end'.split()]
tag=Image.open('tagline.png').convert('RGBA')
WX,WY,WW,WH=78,288,924,1155
shots=[(n,'') for n in 'z083 z024 z051 z019sq z063 z074sq z037 z010 z068 z013sq z001 z004sq z052 z002 z011 z075 z076'.split()]  # no-cross: z080 removed
focus={'z083':(.5,.62)}
precrop={'z044':(40,0,824,980)}  # keeps the large price tag (y~1000-1130) out
S0,STEP,XF=4.5,21.25/16,0.5; DUR=STEP+XF
rng=np.random.default_rng(3)
base=[];moves=[];glints=[]
for i,(n,_) in enumerate(shots):
    im=Image.open(P+n+'.jpg').convert('RGB')
    if n in precrop: im=im.crop(precrop[n])
    bw,bh=int(WW*1.18),int(WH*1.18)
    s=max(bw/im.width,bh/im.height); im=im.resize((math.ceil(im.width*s),math.ceil(im.height*s)),Image.LANCZOS)
    fx,fy=focus.get(n,(.5,.5)); l=int((im.width-bw)*fx); tp=int((im.height-bh)*fy)
    im=im.crop((l,tp,l+bw,tp+bh)); base.append(im)
    zin=i%2==0; dx,dy=[(1,0),(-1,0),(0,1),(0,-1)][i%4]
    moves.append((zin,dx,dy))
    g=np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(float)
    pts=[]
    for _ in range(3):
        y,x=np.unravel_index(g.argmax(),g.shape); pts.append((x,y)); g[max(0,y-150):y+150,max(0,x-150):x+150]=0
    glints.append(pts)
def star(r):
    # soft round glow (no cross-shaped rays)
    s=int(r*2+4); y,x=np.mgrid[:s,:s]-s/2; d=np.sqrt(x*x+y*y)/r
    a=np.clip(np.exp(-d*d*6)*255+np.exp(-d*d*40)*255,0,255); return Image.fromarray(a.astype('uint8'))
STAR=star(34)
def photo_frame(i,lt):
    im=base[i]; u=lt/DUR; e=u*u*(3-2*u)*.6+u*.4
    zin,dx,dy=moves[i]; z=1+(.12*e if zin else .12*(1-e))
    cw,ch=im.width/z,im.height/z; mx,my=(im.width-cw)/2,(im.height-ch)/2
    cx=mx+dx*mx*(e-.5)*1.6; cy=my+dy*my*(e-.5)*1.6
    cx=min(max(cx,0),im.width-cw);cy=min(max(cy,0),im.height-ch)
    fr=im.resize((WW,WH),Image.BILINEAR,box=(cx,cy,cx+cw,cy+ch)).convert('RGBA')
    # light sweep
    p=(lt-.3)/1.2
    if 0<p<1:
        sw=Image.new('L',(WW,WH)); d=ImageDraw.Draw(sw); x0=-500+p*(WW+1000)
        d.polygon([(x0,0),(x0+160,0),(x0+160-600,WH),(x0-600,WH)],fill=int(70*math.sin(p*math.pi)))
        sw=sw.filter(ImageFilter.GaussianBlur(40)); fr=Image.composite(Image.new('RGBA',(WW,WH),(255,248,225,255)),fr,sw) if False else Image.alpha_composite(fr,Image.merge('RGBA',(*[Image.new('L',(WW,WH),255)]*3,sw)))
    for k,(gx,gy) in enumerate(glints[i]):
        tc=.5+k*.45; a=max(0,1-abs(lt-tc)/.35)
        if a>0:
            x=(gx-cx)*WW/cw; y=(gy-cy)*WH/ch
            if 20<x<WW-20 and 20<y<WH-20:
                m=STAR.point(lambda v:int(v*a*.85)); fr.alpha_composite(Image.merge('RGBA',(*[Image.new('L',m.size,255)]*3,m)),(int(x-m.width/2),int(y-m.height/2)))
    return fr
def fade(im,a):
    if a>=1: return im
    r=im.copy(); r.putalpha(im.getchannel('A').point(lambda v:int(v*a))); return r
cl=lambda x:max(0.,min(1.,x)); ease=lambda x:(lambda y:y*y*(3-2*y))(cl(x))
lmask=logo.getchannel('A'); gold=Image.new('RGBA',(W,H),(255,236,170,255))
photostatic=bg.copy(); photostatic.alpha_composite(logosm)
def intro(t):
    fr=bg.copy(); a=ease((t-.2)/1.2)
    if a>0:
        s=.94+.06*a; lg=logo.resize((int(W*s),int(H*s)),Image.BICUBIC); ox=(W-lg.width)//2; oy=int(820-820*s)
        L=Image.new('RGBA',(W,H)); L.alpha_composite(lg,(ox,oy)); L=fade(L,a)
        fr.alpha_composite(L)
        p=(t-1.0)/1.4
        if 0<p<1:
            band=Image.new('L',(W,H)); d=ImageDraw.Draw(band); x0=-300+p*(W+600)
            d.polygon([(x0,500),(x0+140,500),(x0-80,1150),(x0-220,1150)],fill=230); band=band.filter(ImageFilter.GaussianBlur(25))
            m=ImageChops.multiply(band,L.getchannel('A')); g2=gold.copy(); g2.putalpha(m); fr.alpha_composite(g2)
        ga=max(0,1-abs(t-2.5)/.4)
        if ga>0:
            m=star(60).point(lambda v:int(v*ga)); fr.alpha_composite(Image.merge('RGBA',(*[Image.new('L',m.size,255)]*3,m)),(int(W/2+0)-m.width//2+22,690-m.height//2))
    ha=ease((t-3.0)/.8)
    if ha>0:
        h=Image.new('RGBA',(W,H)); h.alpha_composite(hook,(0,int(30*(1-ha)))); fr.alpha_composite(fade(h,ha))
    return fr
def photos(t):
    fr=photostatic.copy(); win=Image.new('RGBA',(WW,WH),(13,31,69,255))
    for i in range(len(shots)):
        lt=t-(S0+i*STEP)
        if -0.0<=lt<DUR:
            a=1 if i==0 else ease(lt/XF)
            if i==len(shots)-1 or lt<STEP: win=Image.alpha_composite(win,fade(photo_frame(i,lt),a))
            else: win=Image.alpha_composite(win,photo_frame(i,lt))
    fr.alpha_composite(win,(WX,WY)); fr.alpha_composite(card)
    a=ease((t-S0-.1)/.5)*ease((26.9-t)/.35)
    if a>0: fr.alpha_composite(fade(tag,a))
    return fr
N=int(T*FPS)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
 '-c:v','libx264','-preset','slow','-crf','23','-maxrate','3.6M','-bufsize','7M','-pix_fmt','yuv420p','-profile:v','high','-level','4.1',
 '-an','-movflags','+faststart',sys.argv[1]],stdin=subprocess.PIPE)
for k in range(N):
    t=k/FPS
    K=0.75
    if t<4.2: f=intro(t/K)
    elif t<4.65: f=Image.blend(intro(t/K),photos(max(t,S0)),ease((t-4.2)/.45))
    elif t<27.0: f=photos(t)
    elif t<27.7: f=Image.blend(photos(t),end,ease((t-27.0)/.7))
    else: f=end
    ff.stdin.write(f.convert('RGB').tobytes())
ff.stdin.close(); ff.wait(); print('done',ff.returncode)
