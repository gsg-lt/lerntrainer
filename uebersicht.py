#!/usr/bin/env python3
"""Erzeugt in jedem Lerngruppen-Ordner von originale/ eine index.html mit Kacheln
zu allen Trainern (neueste zuerst). Wird von verschluesseln.command aufgerufen."""
import html, re, sys
from datetime import date
from pathlib import Path

ORIG = Path(__file__).resolve().parent / "originale"

FACH = {  # Kürzel: (Name, akzent, akzent-dunkel, tint, linie, markierung)
    "en":   ("Englisch",           "#2C5A8C", "#133260", "#ECF5F7", "#C8E3E8", "#61AFBC"),
    "es":   ("Spanisch",           "#316C7C", "#2F5F76", "#FEF8E6", "#FCEBB7", "#F7CC4C"),
    "powi": ("Politik-Wirtschaft", "#535E72", "#3B4455", "#F1F5F0", "#DCE7DA", "#7D928B"),
}
NEU_TAGE = 14


def titel(datei: Path) -> str:
    m = re.search(r"<title>(.*?)</title>", datei.read_text(encoding="utf-8", errors="ignore"), re.S | re.I)
    t = html.unescape(m.group(1).strip()) if m else datei.stem
    return t.split(" · ")[0].strip()


def eintrag(datei: Path):
    m = re.match(r"\d+_[A-Za-z]+_(\d{4})-(\d{2})-(\d{2})_(.+)$", datei.stem)
    d = date(int(m[1]), int(m[2]), int(m[3])) if m else date.min
    return {"datei": datei.name, "titel": titel(datei), "datum": d}


def seite(kuerzel: str, jg: str, eintraege) -> str:
    name, ak, akd, tint, linie, mark = FACH.get(kuerzel, (kuerzel.upper(),) + FACH["en"][1:])
    heute = date.today()
    kacheln = []
    for e in eintraege:
        neu = (heute - e["datum"]).days <= NEU_TAGE
        badge = '<span class="neu">neu</span>' if neu else ""
        dat = e["datum"].strftime("%d.%m.%Y") if e["datum"] != date.min else ""
        kacheln.append(
            f'<a class="kachel" href="{html.escape(e["datei"])}">'
            f'<span class="titel">{html.escape(e["titel"])}{badge}</span>'
            f'<span class="datum">{dat}</span><span class="pfeil" aria-hidden="true">›</span></a>'
        )
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} {jg} · Lerntrainer</title>
<style>
:root{{--ak:{ak};--akd:{akd};--tint:{tint};--linie:{linie};--mark:{mark}}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:#1B1F26;font-family:Verdana,Geneva,sans-serif;line-height:1.45}}
header{{border-top:8px solid var(--ak);padding:28px 16px 12px;max-width:760px;margin:0 auto}}
.fach{{font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ak);font-weight:bold}}
h1{{margin:.2em 0 .1em;font-size:1.7rem;color:var(--akd)}}
.hinweis{{margin:0;color:#555;font-size:.9rem}}
main{{max-width:760px;margin:0 auto;padding:8px 16px 40px;display:grid;gap:12px}}
.kachel{{display:grid;grid-template-columns:1fr auto;grid-template-areas:"t p" "d p";align-items:center;
  gap:2px 12px;padding:18px 18px 16px 20px;min-height:76px;text-decoration:none;color:inherit;
  border:1px solid var(--linie);border-left:6px solid var(--ak);border-radius:10px;background:#fff;
  transition:background .15s}}
.kachel:hover,.kachel:focus-visible{{background:var(--tint);outline:none}}
.titel{{grid-area:t;font-size:1.15rem;font-weight:bold;color:var(--akd)}}
.datum{{grid-area:d;font-size:.8rem;color:#666}}
.pfeil{{grid-area:p;font-size:2rem;color:var(--ak);line-height:1}}
.neu{{display:inline-block;margin-left:.6em;padding:1px 8px;border-radius:999px;background:var(--mark);
  color:#1B1F26;font-size:.7rem;font-weight:bold;vertical-align:middle;text-transform:uppercase;letter-spacing:.05em}}
footer{{max-width:760px;margin:0 auto;padding:0 16px 32px;color:#888;font-size:.75rem}}
</style></head><body>
<header><div class="fach">{name} · Jahrgang {jg}</div><h1>Lerntrainer</h1>
<p class="hinweis">Tippe auf einen Trainer. Der neueste steht oben.</p></header>
<main>
{chr(10).join(kacheln)}
</main>
<footer>Stand {heute.strftime("%d.%m.%Y")} · {len(eintraege)} Trainer</footer>
</body></html>
"""


def main():
    n = 0
    for ordner in sorted(p for p in ORIG.iterdir() if p.is_dir()):
        m = re.match(r"([a-z]+)(\d+\w*)$", ordner.name)
        if not m:
            continue
        eintraege = [eintrag(f) for f in ordner.glob("*.html") if f.name != "index.html"]
        if not eintraege:
            continue
        eintraege.sort(key=lambda e: (e["datum"], e["titel"]), reverse=True)
        (ordner / "index.html").write_text(seite(m[1], m[2], eintraege), encoding="utf-8")
        print(f"  Übersicht: {ordner.name}/ ({len(eintraege)} Trainer)")
        n += 1
    if n == 0:
        sys.exit("Keine Lerngruppen-Ordner in originale/ gefunden.")


if __name__ == "__main__":
    main()
