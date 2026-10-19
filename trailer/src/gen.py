H='<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../../invite/zisel.css"><style>html,body{background:none!important;width:1080px;height:1920px;overflow:hidden}%s</style></head><body>%s</body></html>'
LOGO=lambda ls:f'<div class="logo" style="--ls:{ls}px"><div class="word">Z<span class="i">ı<img class="gem" src="../../invite/gem.svg"></span>sel</div><div class="jw goldtext">JEWELRY</div></div>'
BG='.bgx{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,#1d3770 0%,#0d1f45 60%,#060f26 100%)}'
FR='<div style="position:absolute;inset:0;padding:26px;border-radius:12px;background:var(--gold);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude"></div><div style="position:absolute;inset:50px;border:1px solid rgba(233,207,122,.6)"></div>'
center='position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center'
A={}
A['bg']=(BG+'.frame>.inner{background:none!important}', '<div class="bgx"></div>'+FR)
A['card']=('.ring{position:absolute;left:70px;top:280px;width:940px;height:1171px;padding:8px;border-radius:6px;background:var(--gold);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;box-shadow:0 0 0 1px rgba(255,240,190,.35) inset}.hair{position:absolute;left:104px;top:314px;width:872px;height:1103px;border:1px solid rgba(233,207,122,.6)}',
 '<div class="ring"></div><div class="hair"></div>')
A['logo']=('',f'<div style="{center};top:640px">{LOGO(230)}</div>')
A['logosm']=('',f'<div style="{center};top:120px">{LOGO(92)}</div>')
A['hook']=('',f'<div style="{center};top:1180px"><div class="goldtext" style="font-family:ZPlay;font-size:76px;line-height:1.15">Brilliance,<br>by appointment.</div><div style="font-weight:600;font-size:30px;letter-spacing:.2em;margin-top:34px;color:#fff">WHOLESALE DIAMOND<br>&amp; FINE JEWELRY</div></div>')
for k,t in [('rings','RINGS'),('bracelets','BRACELETS'),('hoops','HOOPS'),('pendants','PENDANTS &amp; NECKLACES')]:
    A['lab_'+k]=('',f'<div style="{center};top:1500px"><div style="width:120px;height:2px;background:var(--gold)"></div><div class="goldtext" style="font-weight:600;font-size:38px;letter-spacing:.32em;margin-right:-.32em;margin-top:22px">{t}</div><div style="font-family:ZPlay;font-style:italic;font-size:30px;color:#dfe6f5;margin-top:14px">Wholesale Diamond &amp; Fine Jewelry</div></div>')
A['end']=(BG+'.frame>.inner{background:none!important}','<div class="bgx"></div>'+FR+f'<div style="{center};top:400px">{LOGO(210)}<div class="goldtext" style="font-family:ZPlay;font-size:84px;line-height:1.12;margin-top:110px">Book a<br>Private Showing</div><div style="font-weight:600;font-size:32px;letter-spacing:.2em;margin-top:40px">WHOLESALE DIAMOND<br>&amp; FINE JEWELRY</div><div style="width:160px;height:2px;background:var(--gold);margin-top:70px"></div><div style="font-family:ZPlay;font-style:italic;font-size:46px;margin-top:50px">Viewing by appointment only</div><div style="font-size:36px;letter-spacing:.04em;color:#e9cf7a;margin-top:34px">Jonathan Shulkin · Call/Text 725.254.6937</div></div>')
for k,(css,body) in A.items(): open(k+'.html','w').write(H%(css,body))
print(' '.join(A))
