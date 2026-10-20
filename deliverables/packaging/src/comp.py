import numpy as np
from PIL import Image, ImageFilter
def coeffs(dst, src):
    # PIL perspective: maps output (dst) pixel -> input (src) pixel
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+= [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
def composite(photo, art, quad, out, handle_mask_fn=None, texture=0.0, foil_soft=0.6, shade_clip=(0.75,1.3), ss=3):
    P=Image.open(photo).convert('RGB'); W,H=P.size
    A=Image.open(art).convert('RGBA'); aw,ah=A.size
    # warp at ss x supersampling then downsample
    dst=[(x*ss,y*ss) for x,y in quad]; src=[(0,0),(aw,0),(aw,ah),(0,ah)]
    Wb=A.transform((W*ss,H*ss),Image.PERSPECTIVE,coeffs(dst,src),Image.BICUBIC)
    Wb=Wb.resize((W,H),Image.LANCZOS)
    a=np.asarray(Wb).astype(float)/255; art_rgb=a[...,:3]; al=a[...,3:4]
    p=np.asarray(P).astype(float)/255
    L=p.mean(2,keepdims=True)
    # face mask from quad (for reference luminance)
    from PIL import ImageDraw
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(quad,fill=255); face=np.asarray(m)>0
    keep=np.ones((H,W),bool)
    if handle_mask_fn is not None:
        hm=handle_mask_fn(p); hmI=Image.fromarray((hm*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
        hmA=np.asarray(hmI).astype(float)[...,None]/255; al=al*(1-hmA); keep=hm<0.5
    ref=np.median(L[face&keep]); shade=np.clip(L/ref, *shade_clip)
    # blur shading a bit so paper/suede grain doesn't print onto the gold too hard, then re-add some grain
    sh=np.asarray(Image.fromarray((np.clip(shade/2,0,1)[...,0]*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(float)[...,None]/255*2
    shade=sh*(1-texture)+shade*texture
    lit=np.clip(art_rgb*shade*foil_soft+art_rgb*(1-foil_soft)*shade**0.5,0,1)
    o=p*(1-al)+lit*al
    Image.fromarray((o*255).round().astype(np.uint8)).save(out)
