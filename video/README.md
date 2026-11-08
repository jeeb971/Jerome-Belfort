# Vidéo pub — Bravos Habitat / Jérôme Belfort

- `BravosHabitat_JeromeBelfort_9x16.mp4` : vidéo finale 1080×1920, 30 i/s, 50,5 s, avec voix off et musique (Reels, Stories, TikTok, Facebook)
- `couverture.jpg` : image de couverture

Modifier les textes dans `index.html` (aperçu animé : ouvrir `index.html?play`), puis régénérer :

```
# voix off : modèle Piper fr_FR-upmc-medium (voix « pierre », CC BY-SA 4.0, voir voix_MODEL_CARD.txt)
SID=1 python3 voix.py <dossier_modele_upmc> voix.wav 1.05
python3 music.py 50.5 music.wav
ffmpeg -i music.wav -i voix.wav -filter_complex "[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad,asplit[v1][v2];[0:a]volume=0.55[m];[m][v1]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=400[duck];[duck][v2]amix=inputs=2:duration=first:weights=1 1.6:normalize=0,alimiter=limit=0.95" -ar 44100 mix.wav
node render.js BravosHabitat_JeromeBelfort_9x16.mp4 mix.wav
```
