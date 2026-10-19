# Self-synthesized lounge/swing jazz bed for the Zisel trailer (no samples, no licensing).
# 160 BPM, half-time feel: 1 bar = 4 beats = 1.5 s = one photo cut, so every cut lands on a downbeat.
import numpy as np, wave
from scipy.signal import fftconvolve, butter, sosfilt
sr=44100; T=31.0; n=int(sr*T); BPM=160; B=60/BPM; BAR=4*B
rng=np.random.default_rng(11)
L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(sig,t0,g=1.0,pan=0.5):
    i=int(t0*sr)
    if i>=n: return
    s=sig[:n-i]; L[i:i+len(s)]+=s*g*np.sqrt(1-pan); R[i:i+len(s)]+=s*g*np.sqrt(pan)
def sw(beat,eighth=0):  # swung time for beat index (+ eighth=1 for the "and")
    return beat*B+(eighth*B*2/3)
hp=lambda x,fc:sosfilt(butter(2,fc,'hp',fs=sr,output='sos'),x)
lp=lambda x,fc:sosfilt(butter(2,fc,'lp',fs=sr,output='sos'),x)
bp=lambda x,a,b:sosfilt(butter(2,[a,b],'bp',fs=sr,output='sos'),x)
# --- instruments ---
def bass(m,dur=B*0.95,vel=1.0):
    t=np.arange(int(sr*(dur+0.15)))/sr; fr=f(m)
    env=(1-np.exp(-t*400))*np.exp(-t*3.2)*np.clip((dur+0.1-t)/0.1,0,1)
    x=np.sin(2*np.pi*fr*t)+0.45*np.sin(2*np.pi*2*fr*t)*np.exp(-t*6)+0.18*np.sin(2*np.pi*3*fr*t)*np.exp(-t*10)
    thump=np.sin(2*np.pi*fr*0.5*t)*np.exp(-t*30)*0.3
    return lp((x+thump)*env,1400)*vel
def rhodes(m,dur,vel=1.0):
    t=np.arange(int(sr*(dur+0.6)))/sr; fr=f(m)
    idx=1.8*np.exp(-t*5)+0.25
    x=np.sin(2*np.pi*fr*t+idx*np.sin(2*np.pi*fr*t))
    tine=0.12*np.sin(2*np.pi*fr*7.0*t)*np.exp(-t*25)
    env=(1-np.exp(-t*300))*np.exp(-t*1.6)*np.clip((dur+0.5-t)/0.5,0,1)
    trem=1+0.08*np.sin(2*np.pi*4.5*t)
    return (x+tine)*env*trem*vel
def vibe(m,vel=1.0,dec=1.6):
    t=np.arange(int(sr*2.6))/sr; fr=f(m)
    x=np.sin(2*np.pi*fr*t)+0.25*np.sin(2*np.pi*4*fr*t)*np.exp(-t*6)+0.08*np.sin(2*np.pi*10*fr*t)*np.exp(-t*14)
    env=(1-np.exp(-t*800))*np.exp(-t*dec)*(1+0.25*np.sin(2*np.pi*5.5*t))
    return x*env*vel
def ride(vel=1.0,long=False):
    t=np.arange(int(sr*(1.6 if long else 0.7)))/sr
    parts=sum(np.sin(2*np.pi*fq*t+rng.uniform(0,6)) for fq in (3120,4310,5270,6650,7940,9020))/6
    noise=hp(rng.standard_normal(len(t)),6000)*0.5
    ping=np.exp(-t*(2.5 if long else 7)); wash=np.exp(-t*(1.2 if long else 3.5))*0.6
    return (parts*ping+noise*wash)*0.35*vel
def brush(vel=1.0,dur=0.22):
    t=np.arange(int(sr*dur))/sr
    x=bp(rng.standard_normal(len(t)),900,7000)
    env=(1-np.exp(-t*120))*np.exp(-t*14)
    return x*env*0.35*vel
def swish(dur):
    t=np.arange(int(sr*dur))/sr
    x=bp(rng.standard_normal(len(t)),2000,9000)
    env=np.sin(np.pi*t/dur)**2
    return x*env*0.05
def kick(vel=1.0):
    t=np.arange(int(sr*0.3))/sr
    return np.sin(2*np.pi*(55+60*np.exp(-t*40))*t)*np.exp(-t*12)*0.5*vel
# --- harmony: Fmaj9 | D9 | Gm9 | C13 (I-VI-ii-V in F) ---
prog=[dict(root=41,voic=[57,60,64,67],walk=[41,45,48,52]),   # Fmaj9: A C E G over F
      dict(root=38,voic=[54,57,60,64],walk=[38,42,45,47]),   # D9: F# A C E
      dict(root=43,voic=[58,62,65,69],walk=[43,46,50,52]),   # Gm9: Bb D F A
      dict(root=36,voic=[58,62,64,69],walk=[36,40,43,40])]   # C13: Bb D E A
END=28.5; nbars=int(END/BAR)
for b in range(nbars):
    t0=b*BAR; c=prog[b%4]; nxt=prog[(b+1)%4]
    intro=t0<3.0
    # walking bass (last note = chromatic approach to next root)
    w=list(c['walk']); w[3]=nxt['root']+rng.choice([-1,1])
    for k,m in enumerate(w): add(bass(m,vel=0.95 if k in (0,2) else 0.85),t0+k*B,0.55,0.48)
    # ride: ding, ding-da-ding (swung)
    for beat,e,v in [(0,0,1),(1,0,.9),(1,1,.55),(2,0,.95),(3,0,.9),(3,1,.55)]:
        add(ride(v*(0.7 if intro else 1)),t0+sw(beat,e),0.28,0.62)
    # brushes: swish under bar, tap on 2 and 4, feathered kick on 1
    add(swish(BAR),t0,1,0.45)
    if not intro:
        for beat in (1,3): add(brush(1.0),t0+beat*B,0.55,0.4)
        add(kick(.6),t0,0.5,0.5)
    # Rhodes comping: Charleston (beat 1, and-of-2), plus push into next bar on odd bars
    if t0>=1.5:
        hits=[(sw(0),B*1.2,0.9),(sw(1,1),B*0.9,0.7)]
        if b%2==1: hits.append((sw(3,1),B*0.8,0.6))
        for (dt,d,v) in hits:
            vo=c['voic'] if dt<sw(3) else nxt['voic']
            for j,m in enumerate(vo): add(rhodes(m,d,v),t0+dt+j*0.006,0.11,0.35+0.1*j)
# vibraphone fills: logo shimmer + every section change
def fill(t0,notes,step=B*2/3/1.0,g=0.16,pan=0.7):
    for k,m in enumerate(notes): add(vibe(m,1-0.08*k),t0+k*step,g,pan)
fill(0.15,[72,76,79,84,88],step=0.11,g=0.14)          # logo reveal glissando (F6-ish arpeggio)
fill(1.8,[93],g=0.10)                                   # diamond glint ping
for ts in (4.5,10.5,16.5,22.5):                         # Rings / Bracelets / Hoops / Pendants
    fill(ts-B*2/3*3,[79,81,84,88],step=B*2/3/2,g=0.12)
fill(27.0-B,[77,81,84,88,91],step=B/3,g=0.13)           # into end card
# button ending on the end card at 27.0: full Fmaj9 hit, bass root, ride bell, vibe chord
add(bass(29,dur=1.2,vel=1.1),END,0.6,0.48); add(bass(41,dur=1.2,vel=0.8),END,0.4,0.48)
for j,m in enumerate([57,60,64,67,72]): add(rhodes(m,1.0,1.0),END+j*0.008,0.12,0.3+0.1*j)
for m in (76,79,84): add(vibe(m,1.0,dec=1.1),END+0.01,0.11,0.65)
add(ride(1.0,long=True),END,0.35,0.62); add(kick(1.0),END,0.6,0.5); add(brush(1.2,0.4),END,0.6,0.4)
# small room reverb (stereo-decorrelated exponential noise IR)
tir=np.arange(int(sr*1.4))/sr
irL=rng.standard_normal(len(tir))*np.exp(-tir*4.2); irR=rng.standard_normal(len(tir))*np.exp(-tir*4.2)
irL=lp(irL,6000); irR=lp(irR,6000); irL/=np.sqrt((irL**2).sum()); irR/=np.sqrt((irR**2).sum())
L=L+0.22*fftconvolve(L,irL)[:n]; R=R+0.22*fftconvolve(R,irR)[:n]
t=np.arange(n)/sr
fade=np.clip(t/1.2,0,1)*np.clip((T-t)/0.6,0,1)   # 1.2 s fade-in; button rings out, gentle 0.6 s tail
x=np.stack([L,R],1)*fade[:,None]; x=hp(x.T,35).T
x/=np.abs(x).max()/0.5
w=wave.open('music_v3_raw.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('ok')
