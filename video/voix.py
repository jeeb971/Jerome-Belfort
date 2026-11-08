"""Génère la voix off (synthèse vocale Piper), calée sur les scènes de la vidéo.
Usage : SID=1 python3 voix.py <dossier_modele_piper> voix.wav [vitesse]
"""
import sys, wave, os
import numpy as np
from piper import PiperVoice, SynthesisConfig

MODEL_DIR = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else 'voix.wav'
SPEED = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
SID = int(os.environ.get('SID', 0))

# (début en secondes, texte) — début = scène + petit décalage
SCRIPT = [
    (0.35,  "Vous avez un terrain... et le projet d'une maison à votre image ?"),
    (4.95,  "Jérôme Belfort, conducteur de travaux chez Bravos Habitat, en Guadeloupe."),
    (10.45, "Il vous accompagne de A à Z : des plans... à la construction."),
    (14.75, "La conception de votre maison, en 3D."),
    (17.75, "Le permis de construire, bien étudié."),
    (20.80, "Les plans d'exécution, avant de couler la dalle."),
    (23.85, "Le suivi de chantier, et la coordination des artisans."),
    (27.05, "Jusqu'aux finitions, et la remise des clés."),
    (30.00, "Du gros œuvre... à la maison de vos rêves."),
    (35.90, "Un seul interlocuteur, pour tout votre projet."),
    (40.80, "Parlons de votre projet ! Appelez, ou écrivez sur WhatsApp, au : zéro six, quatre-vingt-dix ; trente-trois ; soixante-six ; vingt-six."),
]

onnx = [f for f in os.listdir(MODEL_DIR) if f.endswith('.onnx')][0]
voice = PiperVoice.load(f'{MODEL_DIR}/{onnx}')
sr = voice.config.sample_rate
cfg = SynthesisConfig(speaker_id=SID if voice.config.num_speakers > 1 else None,
                      length_scale=1.0 / SPEED, noise_scale=0.6, noise_w_scale=0.7)
segs = []
for start, text in SCRIPT:
    s = np.concatenate([c.audio_float_array for c in voice.synthesize(text, cfg)])
    segs.append((start, s))
    print(f'{start:6.2f}s  {len(s)/sr:5.2f}s  -> fin {start+len(s)/sr:6.2f}  {text[:50]}')
end = max(st + len(s) / sr for st, s in segs) + 0.5
out = np.zeros(int(end * sr), dtype=np.float32)
for st, s in segs:
    i = int(st * sr); out[i:i + len(s)] += s
out = out / (np.max(np.abs(out)) + 1e-9) * 0.95
with wave.open(OUT, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('fin voix', round(end, 2))
