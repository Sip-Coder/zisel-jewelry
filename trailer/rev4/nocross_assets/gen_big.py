# Big "Wholesale Diamond & Fine Jewelry" variants of hook / tagline / end (no-cross trailers).
# Each .fit element is auto-sized so its widest line spans TARGET px (~87% of 1080).
import os,subprocess,sys
sys.path.insert(0,'../../src'); os.chdir(os.path.dirname(os.path.abspath(__file__)))
src=open('../../src/gen.py').read().split("for k,(css,body) in A.items()")[0]
src=src.replace('../../invite/','../../../invite/')
ns={};exec(src,ns);A=ns['A'];H=ns['H'];center=ns['center']
TARGET=945
JS=f'<script>document.fonts.ready.then(()=>{{for(const e of document.querySelectorAll(".fit")){{const r=document.createRange();let w=0;for(const l of e.querySelectorAll(".ln")){{r.selectNodeContents(l);w=Math.max(w,r.getBoundingClientRect().width)}}const fs=parseFloat(getComputedStyle(e).fontSize);e.style.fontSize=(fs*{TARGET}/w)+"px"}}document.body.dataset.ok=1}})</script>'
OLD='WHOLESALE DIAMOND<br>&amp; FINE JEWELRY</div>'
NEW='<span class="ln">WHOLESALE DIAMOND</span><br><span class="ln">&amp; FINE JEWELRY</span></div>'
out={}
for k in ['hook','end']:
    css,body=A[k]; body=body.replace('style="font-weight:600',' class="fit" style="line-height:1.25;margin-right:-.2em;font-weight:600',1).replace(OLD,NEW)
    assert 'class="fit"' in body; out[k]=(css,body)
out['tagline']=('',f'<div style="{center};top:1500px"><div style="width:120px;height:2px;background:var(--gold)"></div><div class="fit" style="font-family:ZPlay;font-style:italic;font-size:30px;color:#dfe6f5;margin-top:14px"><span class="ln">Wholesale Diamond &amp; Fine Jewelry</span></div></div>')
for k,(css,body) in out.items():
    open(k+'_big.html','w').write(H%(css,body+JS))
    subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1','--default-background-color=00000000','--virtual-time-budget=3000','--window-size=1080,1920',f'--screenshot={k}_big.png',f'{k}_big.html'],capture_output=True)
print('ok')
