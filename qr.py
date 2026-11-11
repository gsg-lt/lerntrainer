#!/usr/bin/env python3
"""Erzeugt QR-Codes zu allen veröffentlichten Lerntrainern (lokal, segno).
Ausgabe in qr/ (nicht im Repo):
  qr/<gruppe>/00_uebersicht.png   – Übersichtsseite der Lerngruppe
  qr/<gruppe>/<trainer>.png       – je Trainer
  qr/Lerntrainer_QR-Codes.html/.pdf – Druckfassung, eine A4-Seite je Lerngruppe
Wird von verschluesseln.command aufgerufen; einzeln: python3 qr.py"""
import html, re, shutil, subprocess, sys
from pathlib import Path

import segno

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uebersicht import FACH, eintrag  # gleiche Titel/Farben wie die Übersichtsseiten

BASIS = "https://gsg-lt.github.io/lerntrainer"
WURZEL = Path(__file__).resolve().parent
ORIG, QR = WURZEL / "originale", WURZEL / "qr"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def png(url: str, ziel: Path):
    segno.make(url, error="m").save(str(ziel), scale=20, border=2)


def svg(url: str, farbe: str) -> str:
    s = segno.make(url, error="m").svg_inline(scale=1, border=2, dark=farbe, omitsize=True)
    return s.replace("<svg ", '<svg class="qr" ', 1)


def main():
    if QR.exists():
        shutil.rmtree(QR)
    QR.mkdir()
    seiten, n = [], 0
    for ordner in sorted((p for p in ORIG.iterdir() if p.is_dir()),
                         key=lambda p: (re.sub(r"\d+", "", p.name), int(re.sub(r"\D", "", p.name) or 0))):
        m = re.match(r"([a-z]+)(\d+\w*)$", ordner.name)
        if not m:
            continue
        name, ak, akd, tint, linie, mark = FACH.get(m[1], (m[1].upper(),) + FACH["en"][1:])
        eintraege = [eintrag(f) for f in ordner.glob("*.html") if f.name != "index.html"]
        if not eintraege:
            continue
        eintraege.sort(key=lambda e: (e["datum"], e["titel"]), reverse=True)
        (QR / ordner.name).mkdir()
        ue_url = f"{BASIS}/{ordner.name}/"
        png(ue_url, QR / ordner.name / "00_uebersicht.png"); n += 1
        kacheln = []
        for e in eintraege:
            url = f"{BASIS}/{ordner.name}/{e['datei']}"
            png(url, QR / ordner.name / e["datei"].replace(".html", ".png")); n += 1
            kacheln.append(f'<div class="k">{svg(url, akd)}<div class="t">{html.escape(e["titel"])}</div>'
                           f'<div class="d">{e["datum"].strftime("%d.%m.%Y")}</div></div>')
        seiten.append(f"""<section class="seite" style="--ak:{ak};--akd:{akd};--tint:{tint};--linie:{linie}">
<div class="fach">{name} · Jahrgang {m[2]}</div><h1>Lerntrainer</h1>
<div class="haupt">{svg(ue_url, akd)}<div><p class="lbl">Alle Trainer der Lerngruppe</p>
<p class="url">{html.escape(ue_url.replace("https://", ""))}</p>
<p class="hinweis">Mit der Kamera-App scannen. Passwort von der Lehrkraft – es gilt 30 Tage für alle Trainer.</p></div></div>
<h2>Einzelne Trainer</h2><div class="raster">{''.join(kacheln)}</div></section>""")

    doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Lerntrainer QR-Codes</title>
<style>
@page{{size:A4;margin:14mm 14mm 16mm;@bottom-center{{content:"Seite " counter(page) " von " counter(pages);
  font:8pt Verdana,sans-serif;color:#777}}}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Verdana,Geneva,sans-serif;color:#1B1F26;background:#fff}}
.seite{{break-after:page;border-top:6px solid var(--ak);padding-top:6mm}}.seite:last-child{{break-after:auto}}
.fach{{font-size:9pt;letter-spacing:.06em;text-transform:uppercase;color:var(--ak);font-weight:bold}}
h1{{margin:1mm 0 5mm;font-size:20pt;color:var(--akd)}}
h2{{font-size:11pt;color:var(--akd);margin:7mm 0 3mm;border-bottom:1px solid var(--linie);padding-bottom:1.5mm}}
.haupt{{display:flex;gap:8mm;align-items:center;border:1px solid var(--linie);border-left:5px solid var(--ak);
  border-radius:3mm;padding:5mm}}
.haupt .qr{{width:55mm;height:55mm;flex:none}}
.lbl{{margin:0 0 2mm;font-weight:bold;font-size:12pt;color:var(--akd)}}
.url{{margin:0 0 3mm;font-size:9pt;word-break:break-all}}.hinweis{{margin:0;font-size:9pt;color:#555;text-align:justify}}
.raster{{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}}
.k{{border:1px solid var(--linie);border-radius:2.5mm;padding:3mm;text-align:center;break-inside:avoid}}
.k .qr{{width:34mm;height:34mm;display:block;margin:0 auto 2mm}}
.t{{font-size:8.5pt;font-weight:bold;color:var(--akd)}}.d{{font-size:7pt;color:#777}}
</style></head><body>
{chr(10).join(seiten)}
</body></html>"""
    h = QR / "Lerntrainer_QR-Codes.html"
    h.write_text(doc, encoding="utf-8")
    pdf = QR / "Lerntrainer_QR-Codes.pdf"
    if Path(CHROME).exists():
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", h.as_uri()], capture_output=True, timeout=120)
    print(f"  QR-Codes: {n} PNG + {'PDF' if pdf.exists() else 'HTML (PDF fehlgeschlagen)'} in qr/")


if __name__ == "__main__":
    main()
