#!/usr/bin/env python3
"""QR-Codes für die Drachengeschichten (lokal, segno) – Druckseite A4 + PNG.
Ausgabe: 04 Miscellaneous/Geschichten-Grundschule/QR/ im Vault."""
import subprocess
from pathlib import Path
import segno

BASIS = "https://gsg-lt.github.io/lerntrainer/geschichten/"
ZIEL = Path("/Users/zb/AI Helper/GSGB/04 Miscellaneous/Geschichten-Grundschule/QR")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AK, AKD, LINIE = "#2f7d8c", "#1d4f59", "#cfe0ea"
GESCH = [("Die-Drachenschule_Lesebuch.html", "Die Drachenschule von Wolkenhain", "🏫"),
         ("Die-Zauberdrachen_Lesebuch.html", "Die Zauberdrachen von Wolkenhain", "✨"),
         ("Die-Reise-zur-Windharfe_Lesebuch.html", "Die Reise zur Windharfe", "🎶")]

def svg(url):
    s = segno.make(url, error="m").svg_inline(scale=1, border=2, dark=AKD, omitsize=True)
    return s.replace("<svg ", '<svg class="qr" ', 1)

ZIEL.mkdir(parents=True, exist_ok=True)
segno.make(BASIS, error="m").save(str(ZIEL / "00_Drachengeschichten.png"), scale=20, border=2)
kacheln = []
for datei, titel, emo in GESCH:
    url = BASIS + datei
    segno.make(url, error="m").save(str(ZIEL / datei.replace(".html", ".png")), scale=20, border=2)
    kacheln.append(f'<div class="k">{svg(url)}<div class="t">{emo} {titel}</div></div>')

doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Drachengeschichten QR</title>
<style>@page{{size:A4;margin:16mm}}*{{box-sizing:border-box}}
body{{margin:0;font-family:Verdana,Geneva,sans-serif;color:#1B1F26;background:#fff}}
.seite{{border-top:6px solid {AK};padding-top:8mm}}
h1{{margin:0 0 8mm;font-size:26pt;color:{AKD};text-align:center}}
.haupt{{text-align:center;border:1px solid {LINIE};border-radius:4mm;padding:8mm}}
.haupt .qr{{width:90mm;height:90mm}}
.lbl{{font-size:15pt;font-weight:bold;color:{AKD};margin:4mm 0 2mm}}
.url{{font-size:10pt;margin:0 0 2mm}}.hinweis{{font-size:10pt;color:#555;margin:0}}
h2{{font-size:12pt;color:{AKD};margin:9mm 0 4mm;border-bottom:1px solid {LINIE};padding-bottom:2mm}}
.raster{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm}}
.k{{border:1px solid {LINIE};border-radius:3mm;padding:4mm;text-align:center}}
.k .qr{{width:42mm;height:42mm;display:block;margin:0 auto 3mm}}
.t{{font-size:10pt;font-weight:bold;color:{AKD}}}
</style></head><body><section class="seite">
<h1>🐉 Drachengeschichten</h1>
<div class="haupt">{svg(BASIS)}<p class="lbl">Alle Geschichten</p>
<p class="url">{BASIS.replace("https://", "")}</p>
<p class="hinweis">Mit der Kamera scannen und das Geschichten-Passwort eingeben.</p></div>
<h2>Einzelne Geschichten</h2><div class="raster">{''.join(kacheln)}</div></section></body></html>"""
h = ZIEL / "Drachengeschichten_QR-Codes.html"
h.write_text(doc, encoding="utf-8")
pdf = h.with_suffix(".pdf")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", h.as_uri()], capture_output=True, timeout=120)
print("PDF ok" if pdf.exists() else "PDF fehlgeschlagen", "->", ZIEL)
