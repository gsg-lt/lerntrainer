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
