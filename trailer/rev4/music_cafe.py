# Original bright coffee-shop jazz, 96 bpm, beat grid offset 0.125s so photo cuts (4.5+1.25k) land on beats
import numpy as np, wave
sr=44100; T=31.0; n=int(sr*T); bpm=96; b=60/bpm; OFF=0.125
f=lambda m:440*2**((m-69)/12)
L=np.zeros(n);R=np.zeros(n); rng=np.random.default_rng(11)
def add(sig,s0,g,pan=.5):
    i=int(s0*sr)
    if i>=n or i<0: return
    sig=sig[:n-i]; L[i:i+len(sig)]+=sig*g*(1-pan)*2; R[i:i+len(sig)]+=sig*g*pan*2
def rhodes(m,d):
    tt=np.arange(int((d+.6)*sr))/sr; fr=f(m)
    mod=np.sin(2*np.pi*fr*tt)*1.2*np.exp(-tt*6)
    return np.sin(2*np.pi*fr*tt+mod)*np.exp(-tt*1.3)*np.clip((d+.6-tt)/.4,0,1)
def bass(m,d):
    tt=np.arange(int(d*sr))/sr; fr=f(m)
    return (np.sin(2*np.pi*fr*tt)+.3*np.sin(4*np.pi*fr*tt))*np.exp(-tt*3)*np.clip(tt/.01,0,1)
def gtr(m):
    tt=np.arange(int(.35*sr))/sr; fr=f(m)
    return sum(np.sin(2*np.pi*fr*k*tt)/k**1.5 for k in (1,2,3))*np.exp(-tt*9)
def lp(x,a): 
    y=np.zeros_like(x); s=0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
nz=lp(rng.standard_normal(int(.25*sr)),.08)
def brush(d,acc): tt=np.arange(len(nz))/sr; return nz[:len(tt)]*np.exp(-tt*d)*acc
# I-vi-ii-V in F, then IV-iii-ii-V  (voicings)
prog=[([53,57,60,64],41),([50,53,57,60],38),([55,58,62,65],43),([48,52,55,58],36),
      ([58,62,65,69],46),([57,60,64,67],45),([55,58,62,65],43),([48,52,55,58,62],36)]
bars=int(T/(4*b))+1; scale=[65,67,69,72,74,77,79]
for bi in range(bars):
    ch,root=prog[bi%8]; s=OFF+bi*4*b
    for st in (0,2.5): 
        for m in ch: add(rhodes(m,1.4*b),s+st*b,.045,rng.uniform(.35,.65))
    walk=[root,root+4,root+7,root+(5 if bi%2 else 6)]
    for k,m in enumerate(walk): add(bass(m-12 if m>40 else m,b*.95),s+k*b,.16,.5)
    for k in range(4):
        add(brush(14,.10 if k%2 else .06),s+k*b,1,.6)
        add(brush(22,.035),s+(k+.66)*b,1,.4)
    for k in (1,3): add(gtr(ch[1]+12),s+k*b,.05,.75); add(gtr(ch[2]+12),s+k*b+.01,.05,.75)
    if 1<=bi<bars-1:  # light piano melody, generated from scale
        for k in range(rng.integers(3,6)):
            pos=rng.choice([0,1,1.5,2,2.5,3]); m=rng.choice(scale)+(0 if rng.random()<.7 else -12)
            add(rhodes(m,.5*b),s+pos*b,.05,.45)
x=np.stack([L,R]);
x=np.stack([lp(c,.35) for c in x])  # soften highs
def verb(c,ds,g):
    y=c.copy()
    for d in ds: D=int(d*sr); y[D:]+=c[:-D]*g
    return y
x=np.stack([verb(x[0],[.029,.061,.097,.151],.25),verb(x[1],[.033,.067,.109,.163],.25)])
t=np.arange(n)/sr; x*=np.clip(t/.4,0,1)*np.clip((T-t)/2.5,0,1)
x=x/np.abs(x).max()*.85
wave_=wave.open('music_cafe.wav','w'); wave_.setnchannels(2); wave_.setsampwidth(2); wave_.setframerate(sr)
wave_.writeframes((x.T*32767).astype('<i2').tobytes()); wave_.close(); print('ok')
