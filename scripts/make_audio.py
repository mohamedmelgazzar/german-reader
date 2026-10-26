"""Make MP3 clips with Microsoft's natural German voice (via edge-tts).

Runs automatically on GitHub (see .github/workflows/audio.yml) whenever
index.html changes. Only missing clips are made, so adding a story is quick.
Change VOICE below to switch voices; all clips are then remade.

Other German voices to try: de-DE-ConradNeural (male), de-DE-AmalaNeural,
de-DE-KillianNeural, de-DE-SeraphinaMultilingualNeural.
"""
import asyncio, json, os, shutil
import edge_tts

VOICE = "de-DE-KatjaNeural"
OUT = "audio"

def slug(k):
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("'", "_")]:
        k = k.replace(a, b)
    return k

LETTERS = dict(a="A", b="Be", c="Ze", d="De", e="E", f="Eff", g="Ge", h="Ha", i="I", j="Jott",
               k="Ka", l="Ell", m="Emm", n="Enn", o="O", p="Pe", q="Ku", r="Err", s="Ess", t="Te",
               u="U", v="Vau", w="We", x="Ix", y="Ypsilon", z="Zett")
LETTERS.update({"ä": "Ä", "ö": "Ö", "ü": "Ü", "ß": "Eszett", "é": "E", "'": "Apostroph"})

async def make(text, path, rate="+0%"):
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=rate).save(path)
            return
        except Exception as e:
            print("retry", path, e)
            await asyncio.sleep(2 + attempt * 3)
    raise SystemExit("could not make " + path)

async def main():
    marker = os.path.join(OUT, "voice.txt")
    if os.path.exists(marker) and open(marker).read().strip() != VOICE:
        shutil.rmtree(OUT)  # voice changed: remake everything
    os.makedirs(OUT, exist_ok=True)
    open(marker, "w").write(VOICE)

    items = json.load(open("scripts/items.json", encoding="utf8"))
    for s in items["sentences"]:
        await make(s["de"], f"{OUT}/s/{s['id']}.mp3", "-10%")
    for k, shown in items["words"].items():
        await make(shown, f"{OUT}/w/{slug(k)}.mp3", "-5%")
        await make(shown, f"{OUT}/ws/{slug(k)}.mp3", "-45%")
    letters = {c for k in items["words"] for c in k}
    for c in sorted(letters):
        await make(LETTERS.get(c, c.upper()), f"{OUT}/l/{slug(c)}.mp3", "-10%")
    await make("Hallo! Das ist deine deutsche Stimme.", f"{OUT}/test.mp3", "-5%")
    print("audio ready")

asyncio.run(main())
