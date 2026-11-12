#!/bin/zsh
# Drachengeschichten (Privatmaterial) -> docs/geschichten/ mit EIGENEM Passwort.
# Getrennt von verschluesseln.command; eigener Salt (.staticrypt-geschichten.json)
# und eigene Merk-Schluessel (vorlage_geschichten.html), damit sich das gemerkte
# Trainer-Passwort und das Geschichten-Passwort auf einem Geraet nicht gegenseitig loeschen.
cd "$(dirname "$0")"
QUELLE="/Users/zb/AI Helper/GSGB/04 Miscellaneous/Geschichten-Grundschule"
DATEIEN=(Das-Drachenkueken_Lesebuch.html Die-Drachenschule_Lesebuch.html Die-Zauberdrachen_Lesebuch.html Die-Reise-zur-Windharfe_Lesebuch.html)
fertig(){ read -k1 "?Taste drücken …"; exit ${1:-0}; }

rm -rf originale_geschichten && mkdir -p originale_geschichten
for f in $DATEIEN; do
  [[ -f "$QUELLE/$f" ]] || { echo "Fehlt: $f"; fertig 1; }
  cp "$QUELLE/$f" originale_geschichten/
done

# Uebersichtsseite
cat > originale_geschichten/index.html <<'HTML'
<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Drachengeschichten</title>
<style>
body{margin:0;font-family:Verdana,sans-serif;background:#f4f8fb;color:#1d2b36}
main{max-width:720px;margin:0 auto;padding:32px 16px}
h1{text-align:center;font-size:2rem;margin:0 0 8px}
p.sub{text-align:center;margin:0 0 28px;color:#4a5d6b}
a.k{display:flex;align-items:center;gap:16px;background:#fff;border:2px solid #cfe0ea;border-radius:16px;
 padding:20px;margin:0 0 16px;text-decoration:none;color:inherit;font-size:1.25rem}
a.k:hover{border-color:#2f7d8c}
a.k span{font-size:2.2rem}
</style></head><body><main>
<h1>🐉 Drachengeschichten</h1><p class="sub">Such dir eine Geschichte aus.</p>
<a class="k" href="Das-Drachenkueken_Lesebuch.html"><span>🐣</span>Das Drachenküken von Wolkenhain</a>
<a class="k" href="Die-Drachenschule_Lesebuch.html"><span>🏫</span>Die Drachenschule von Wolkenhain</a>
<a class="k" href="Die-Zauberdrachen_Lesebuch.html"><span>✨</span>Die Zauberdrachen von Wolkenhain</a>
<a class="k" href="Die-Reise-zur-Windharfe_Lesebuch.html"><span>🎶</span>Die Reise zur Windharfe</a>
</main></body></html>
HTML

ls originale_geschichten | sed 's/^/  /'
echo
read -s "PW?Passwort für die Geschichten (anders als das Trainer-Passwort): "; echo
read -s "PW2?Passwort wiederholen: "; echo
[[ "$PW" != "$PW2" ]] && { echo "Passwörter stimmen nicht überein."; fertig 1; }
[[ -z "$PW" ]] && { echo "Leeres Passwort."; fertig 1; }

rm -rf docs/geschichten && mkdir -p docs/geschichten
cd originale_geschichten
STATICRYPT_PASSWORD="$PW" npx --prefix .. staticrypt * -d ../docs/geschichten --remember 30 \
  --config ../.staticrypt-geschichten.json \
  -t ../vorlage_geschichten.html \
  --template-title "Drachengeschichten" \
  --template-instructions "Gib das Geschichten-Passwort ein." \
  --template-button "Öffnen" \
  --template-placeholder "Passwort" \
  --template-remember "Passwort 30 Tage merken" \
  --template-error "Falsches Passwort – bitte noch einmal." \
  --template-toggle-show "Passwort anzeigen" \
  --template-toggle-hide "Passwort verbergen"
rc=$?
unset PW PW2
cd ..
(( rc == 0 )) || { echo "StatiCrypt-Fehler (Code $rc)."; fertig 1; }
rm -rf originale_geschichten
echo "Fertig: $(ls docs/geschichten | wc -l | tr -d ' ') verschlüsselte Dateien in docs/geschichten/."
echo "Adresse: https://gsg-lt.github.io/lerntrainer/geschichten/"
echo; echo "Hochladen mit:  git add -A docs && git commit -m 'Drachengeschichten' && git push"
fertig
