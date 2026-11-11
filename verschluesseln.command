#!/bin/zsh
# Verschlüsselt alle HTML-Dateien aus originale/ nach docs/ (gleiche Unterordner).
# Passwort wird verdeckt abgefragt – nicht gespeichert, nicht in der Shell-History.
cd "$(dirname "$0")"
setopt null_glob
if [[ -z $(find originale -name '*.html' -print -quit) ]]; then
  echo "Keine HTML-Dateien in originale/ gefunden."; read -k1 "?Taste drücken …"; exit 1
fi
read -s "PW?Passwort (lange Passphrase): "; echo
read -s "PW2?Passwort wiederholen: "; echo
[[ "$PW" != "$PW2" ]] && { echo "Passwörter stimmen nicht überein."; read -k1 "?Taste drücken …"; exit 1; }
cd originale
STATICRYPT_PASSWORD="$PW" npx --prefix .. staticrypt * -r -d ../docs --remember 30 \
  --config ../.staticrypt.json \
  --template-title "Lerntrainer" \
  --template-instructions "Das Passwort bekommst du von deiner Lehrkraft." \
  --template-button "Öffnen" \
  --template-placeholder "Passwort" \
  --template-remember "Passwort 30 Tage merken" \
  --template-error "Falsches Passwort – bitte noch einmal." \
  --template-toggle-show "Passwort anzeigen" \
  --template-toggle-hide "Passwort verbergen"
unset PW PW2
cd ..
echo; echo "Fertig. Verschlüsselte Dateien:"; find docs -name '*.html' | sed 's/^/  /'
echo; echo "Prüfen, dann hochladen mit:  git add docs && git commit -m 'Update' && git push"
read -k1 "?Taste drücken …"
