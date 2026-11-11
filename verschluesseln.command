#!/bin/zsh
# 1. Holt alle Trainer frisch aus dem Vault nach originale/
#    (00 Fachbereiche/<Fach>/{Vokabeltrainer,Lerntrainer}/Jg <n>/*.html – ohne Unterordner
#    wie _generator/ oder Classtime/, ohne Einträge aus ausnahmen.txt)
# 2. Verschlüsselt alles nach docs/ (docs/ wird dabei neu aufgebaut)
# Passwort wird verdeckt abgefragt – nicht gespeichert, nicht in der Shell-History.
cd "$(dirname "$0")"
setopt null_glob extended_glob
VAULT="/Users/zb/AI Helper/GSGB/00 Fachbereiche"
fertig(){ read -k1 "?Taste drücken …"; exit ${1:-0}; }

[[ -d "$VAULT" ]] || { echo "Vault nicht gefunden: $VAULT"; fertig 1; }

# Ausnahmen laden (Dateinamen, # = Kommentar)
typeset -a AUSN
[[ -f ausnahmen.txt ]] && AUSN=(${(f)"$(grep -v '^\s*#' ausnahmen.txt | sed 's/[[:space:]]*$//' | grep -v '^$')"})

# --- 1. Holen ---
rm -rf originale && mkdir originale
typeset -i n=0 x=0
for jg in "$VAULT"/*/(Vokabeltrainer|Lerntrainer)/Jg\ *(/); do
  fach=${${jg:h:h:t}#[0-9][0-9] }          # "01 Englisch" -> "Englisch"
  case $fach in
    Englisch) k=en;; Spanisch) k=es;; Politik-Wirtschaft) k=powi;; *) k=${fach:l};;
  esac
  ziel="originale/$k${${jg:t}#Jg }"
  for f in "$jg"/*.html(.); do
    if (( ${AUSN[(Ie)${f:t}]} )); then x+=1; continue; fi
    mkdir -p "$ziel" && cp "$f" "$ziel/" && n+=1
  done
done
echo "Aus dem Vault geholt: $n Trainer ($x per ausnahmen.txt übersprungen)"
(( n > 0 )) || { echo "Keine Trainer gefunden."; fertig 1; }
python3 uebersicht.py || { echo "Fehler beim Erzeugen der Übersichtsseiten."; fertig 1; }
find originale -name '*.html' | sort | sed 's/^originale\//  /'
echo
read -k1 "ANTW?Diese Dateien verschlüsseln? (j/n) "; echo
[[ $ANTW == [jJyY] ]] || { echo "Abgebrochen."; fertig; }
echo

# --- 2. Verschlüsseln ---
read -s "PW?Passwort (lange Passphrase): "; echo
read -s "PW2?Passwort wiederholen: "; echo
[[ "$PW" != "$PW2" ]] && { echo "Passwörter stimmen nicht überein."; fertig 1; }
[[ -z "$PW" ]] && { echo "Leeres Passwort."; fertig 1; }

find docs -mindepth 1 ! -name .gitkeep -delete
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
  --template-toggle-hide "Passwort verbergen" >/dev/null
rc=$?
unset PW PW2
cd ..
(( rc == 0 )) || { echo "StatiCrypt-Fehler (Code $rc)."; fertig 1; }

echo; echo "Fertig: $(find docs -name '*.html' | wc -l | tr -d ' ') verschlüsselte Dateien in docs/."
git status --short docs | head -40
echo; echo "Hochladen mit:  git add -A docs && git commit -m 'Update' && git push"
fertig
