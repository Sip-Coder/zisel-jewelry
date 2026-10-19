import numpy as np, wave
sr=44100; T=31.0; n=int(sr*T); t=np.arange(n)/sr
bpm=80; beat=60/bpm
def f(m): return 440*2**((m-69)/12)
chords=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59,62]]  # Fmaj7 Em7 Dm7 Cmaj9
L=np.zeros(n); R=np.zeros(n)
seg=beat*8  # 6s per chord
for ci in range(int(np.ceil(T/seg))):
    c=chords[ci%4]; s0=ci*seg
    env=np.clip((t-s0)/1.5,0,1)*np.clip((s0+seg+1.2-t)/1.5,0,1)
    for k,m in enumerate(c):
        for d,(a,b) in zip((-0.08,0.08),((1,.6),(.6,1))):
            w=np.sin(2*np.pi*f(m)*(1+d/100)*t+k)+.25*np.sin(2*np.pi*2*f(m)*t)+.08*np.sin(2*np.pi*3*f(m)*t)
            L+=a*.05*env*w; R+=b*.05*env*w
    bass=np.sin(2*np.pi*f(c[0]-12)*t)*.09*env; L+=bass; R+=bass
rng=np.random.default_rng(7)
for bi in range(int(T/beat)):
    s0=bi*beat
    if s0<1.0 or s0>T-2: continue
    c=chords[int(s0//seg)%4]; m=c[rng.integers(len(c))]+24
    i0=int(s0*sr); ln=int(2.5*sr); tt=np.arange(min(ln,n-i0))/sr
    v=(.05 if bi%2 else .075)*np.exp(-tt*2.2)*(np.sin(2*np.pi*f(m)*tt)+.3*np.sin(2*np.pi*f(m)*2.76*tt)*np.exp(-tt*5))
    p=rng.uniform(.3,.7); L[i0:i0+len(tt)]+=v*(1-p)*2; R[i0:i0+len(tt)]+=v*p*2
# simple reverb
def verb(x,ds,g):
    y=x.copy()
    for d in ds:
        D=int(d*sr); z=np.zeros_like(x); z[D:]=x[:-D]*g; y+=z
    return y
L=verb(L,[.031,.067,.113,.173,.241],.35); R=verb(R,[.037,.071,.127,.181,.263],.35)
fade=np.clip(t/1.2,0,1)*np.clip((T-t)/3.0,0,1)
x=np.stack([L,R],1)*fade[:,None]; x/=np.abs(x).max()/0.6
w=wave.open('music_calm.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
