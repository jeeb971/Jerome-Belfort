"""Generates an original royalty-free soundtrack (tropical-house style) + transition whooshes."""
import numpy as np, wave, sys

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 47.5
TRANS = [4.6, 10.2, 14.4, 29.6, 35.6, 40.4]
STEP_HITS = [14.4 + i * 3.04 for i in range(1, 5)]
BPM = 112
beat = 60 / BPM
N = int(SR * DUR)
t = np.arange(N) / SR
mix = np.zeros((N, 2))

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    l, r = gain * (1 - max(0, pan)), gain * (1 + min(0, pan))
    mix[i:i + len(sig), 0] += sig * l
    mix[i:i + len(sig), 1] += sig * r

def env(n, a=0.005, d=0.3):
    x = np.arange(n) / SR
    return np.minimum(1, x / a) * np.exp(-x / d)

def note(f): return 440 * 2 ** ((f - 69) / 12)

# kick
def kick():
    n = int(.45 * SR); x = np.arange(n) / SR
    f = 50 + 120 * np.exp(-x * 35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 7)
K = kick()
def hat():
    n = int(.06 * SR); x = np.arange(n) / SR
    s = np.random.randn(n); s = np.diff(np.concatenate([[0], s]))
    return s * np.exp(-x * 60) * .5
def clap():
    n = int(.25 * SR); x = np.arange(n) / SR
    s = np.random.randn(n)
    s = np.convolve(s, np.ones(4) / 4, 'same') - np.convolve(s, np.ones(40) / 40, 'same')
    e = sum(np.exp(-np.maximum(0, x - o) * 30) * (x >= o) for o in (0, .012, .024)) / 3
    return s * e * .9
def pluck(f, d=.35):
    n = int(.9 * SR); x = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * x) / k ** 1.4 for k in range(1, 7))
    return s * env(n, .003, d) * .25
def pad(fs, length):
    n = int(length * SR); x = np.arange(n) / SR
    s = np.zeros(n)
    for f in fs:
        for det in (-0.12, 0, 0.12):
            ff = f * 2 ** (det / 12)
            s += np.sin(2 * np.pi * ff * x + np.sin(2 * np.pi * .3 * x)) * .5 + np.sin(2 * np.pi * 2 * ff * x) * .12
    a = np.minimum(1, x / .4) * np.minimum(1, (length - x) / .4)
    return s * a / (len(fs) * 3) * .5
def bass(f, length):
    n = int(length * SR); x = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * x) + .3 * np.sin(2 * np.pi * 2 * f * x)
    return s * np.minimum(1, x / .01) * np.exp(-x * 2.2) * .55

# chord progression C - G - Am - F (one bar each)
CH = [[60, 64, 67], [59, 62, 67], [57, 60, 64], [57, 60, 65]]
BS = [36, 43, 45, 41]
bar = 4 * beat
nbars = int(DUR / bar) + 1
intro = 2 * bar  # drums enter after intro
melody_pat = [0, 2, 1, 2, 0, 1, 2, 1]
for b in range(nbars):
    t0 = b * bar
    c = CH[b % 4]
    add(pad([note(m) for m in c], bar + .3), t0, .9)
    for i, off in enumerate([0, .75, 1.5, 2, 2.75, 3.5]):
        add(pluck(note(c[melody_pat[i % 8]] + 12)), t0 + off * beat, .55, pan=(-.3 if i % 2 else .3))
    if t0 >= intro:
        for k in range(4):
            add(K, t0 + k * beat, .9)
            add(hat(), t0 + (k + .5) * beat, .35, pan=.2)
            add(bass(note(BS[b % 4]), beat * .9), t0 + (k + .5) * beat, .8)
        add(clap(), t0 + beat, .35); add(clap(), t0 + 3 * beat, .35)

# whoosh on transitions
def whoosh(length=.9, up=True):
    n = int(length * SR); x = np.arange(n) / SR
    s = np.random.randn(n)
    out = np.zeros(n); y = 0
    cut = np.linspace(.02, .35, n) if up else np.linspace(.35, .02, n)
    for i in range(n):
        y += cut[i] * (s[i] - y); out[i] = y
    e = np.sin(np.pi * x / length) ** 2
    return out * e * 1.2
W = whoosh()
for tr in TRANS: add(W, tr - .45, .6)
for h in STEP_HITS: add(whoosh(.5), h - .3, .35)
# low impact at CTA
n = int(1.5 * SR); x = np.arange(n) / SR
boom = np.sin(2 * np.pi * (40 + 40 * np.exp(-x * 8)) * x) * np.exp(-x * 2.5)
add(boom, 40.4, .9)

# master: fades, normalize, soft clip
fade = np.minimum(1, t / .8) * np.minimum(1, (DUR - t) / 2.0)
mix *= fade[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.3) / np.tanh(1.3) * .8
pcm = (mix * 32767).astype('<i2')
with wave.open(sys.argv[2] if len(sys.argv) > 2 else 'music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
