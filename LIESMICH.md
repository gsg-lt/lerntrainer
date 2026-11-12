# gsgb-web – verschlüsselte HTML für GitHub Pages

Getrennt vom Vault. Ins Netz geht **nur `docs/`** (verschlüsselt).

| Ordner/Datei | Zweck |
|---|---|
| `originale/` | unverschlüsselte HTML hier ablegen (Unterordner erlaubt) – bleibt lokal (.gitignore) |
| `docs/` | verschlüsselte Ausgabe → GitHub Pages (Branch `main`, Ordner `/docs`) |
| `verschluesseln.command` | Doppelklick: fragt Passwort verdeckt ab, verschlüsselt alles aus `originale/` nach `docs/` |
| `.staticrypt.json` | Salt – lokal behalten, damit „Passwort merken“ nach Neuverschlüsselung weiter gilt |

Regeln: keine Schülerdaten, keine Passwortdateien, Passphrase aus 4+ zufälligen Wörtern.
Einmalig: Repo auf github.com anlegen, `git remote add origin …`, Settings → Pages → main /docs.

## Drachengeschichten (eigenes Passwort)
`geschichten.command` (Doppelklick) holt die drei Drachen-Lesebücher aus
`04 Miscellaneous/Geschichten-Grundschule/`, fragt ein **eigenes** Passwort ab und verschlüsselt
nach `docs/geschichten/` → https://gsg-lt.github.io/lerntrainer/geschichten/
Eigener Salt (`.staticrypt-geschichten.json`, lokal) und eigene Merk-Schlüssel
(`vorlage_geschichten.html`), damit „Passwort merken“ für Trainer und Geschichten nebeneinander hält.
`verschluesseln.command` lässt `docs/geschichten/` unangetastet.
Hinweis: Die Geschichten enthalten den echten Vornamen von P02 — Ausnahme ausdrücklich
von der Lehrkraft entschieden (12.11.26).
