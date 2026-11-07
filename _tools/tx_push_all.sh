#!/usr/bin/env bash
#
# tx_push_all.sh -- Uebersetzungen Ressource fuer Ressource nach Transifex
# schieben. Das Repo ist dabei die Quelle der Wahrheit: ein Push mit
# --translation ersetzt die dortigen Uebersetzungen durch unseren Stand.
#
# Warum ueber ein Staging-Verzeichnis?
# Das tx-CLI liest die Sprache einer Datei ausschliesslich aus dem Pfad, am
# Platzhalter <lang> im file_filter. Unsere .tx/config zeigt aber auf
# "library/colorsys.po" -- ohne <lang>, weil in diesem Repo nur Deutsch
# liegt und die Dateien im Wurzelverzeichnis stehen. Folge: tx findet
# keine einzige lokale Sprache, laedt nichts hoch und endet trotzdem mit
# Status 0 ("Getting info about resources ... Done", danach nichts).
# Darum legt dieses Skript unter $TMPDIR einen Baum
# <staging>/de/<pfad> aus Symlinks auf die echten Dateien an, schreibt
# dort eine .tx/config mit "file_filter = <lang>/<pfad>" und pusht von
# dort. Das Repo bleibt unberuehrt, das Staging wird am Ende geloescht.
#
# --force heisst NICHT "bearbeitete Strings ueberschreiben". Laut tx-Hilfe
# umgeht es nur die Pruefung der Aenderungszeiten ("Push source files
# without checking modification times"). Ohne den Schalter uebergeht tx
# Dateien, die aelter sind als die Ressource im Server -- und genau das
# trifft auf einen Teil unserer Dateien zu.
#
# Voraussetzungen:
#   * tx-CLI installiert und im PATH
#   * API-Token in ~/.transifexrc (NICHT im Repo, nicht in dieser Datei)
#   * Bash ab 3.2, also auch die von macOS mitgelieferte /bin/bash
#
# Nutzung:
#   ./_tools/tx_push_all.sh                     # alles ausser AUSNAHMEN
#   ./_tools/tx_push_all.sh --liste             # nur zeigen, was gepusht wuerde
#   ./_tools/tx_push_all.sh --nur library--     # nur passende Ressourcen
#   ./_tools/tx_push_all.sh --ohne-ausnahmen    # wirklich alles, auch die
#                                               # Dateien in AUSNAHMEN
#   ./_tools/tx_push_all.sh --behalten          # Staging nicht loeschen
#
set -uo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CONFIG="$REPO_ROOT/.tx/config"
ORGA="${ORGA:-python-doc}"
PROJEKT="${PROJEKT:-python-newest}"
SPRACHE="${SPRACHE:-de}"

# Ressourcen, die NICHT gepusht werden. Hier stehen die vier grossen
# extending-Dateien: die sind in Transifex in Arbeit, unser Repo-Stand ist
# nur mechanisch bereinigt und soll die dortige Fassung nicht ueberschreiben.
AUSNAHMEN=(
    "extending--extending"
    "extending--first-extension-module"
    "extending--newtypes"
    "extending--newtypes_tutorial"
)

NUR=""
MIT_AUSNAHMEN=false
NUR_LISTE=false
BEHALTEN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --liste)          NUR_LISTE=true ;;
        --ohne-ausnahmen) MIT_AUSNAHMEN=true ;;
        --behalten)       BEHALTEN=true ;;
        --nur)            NUR="${2:-}"; shift ;;
        -h|--help)        sed -n '2,40p' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "Unbekannte Option: $1"; exit 2 ;;
    esac
    shift
done

if [[ ! -f "$CONFIG" ]]; then
    echo "Keine .tx/config unter $CONFIG gefunden."
    exit 1
fi
if ! command -v tx >/dev/null 2>&1; then
    echo "Das tx-CLI liegt nicht im PATH. Installation:"
    echo "  https://developers.transifex.com/docs/cli"
    exit 1
fi
if [[ ! -f "$HOME/.transifexrc" ]]; then
    echo "~/.transifexrc fehlt -- ohne API-Token kann nicht gepusht werden."
    echo "Anlegen mit: tx init"
    exit 1
fi

BRANCH="$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null)"
echo "Repo:    $REPO_ROOT"
echo "Branch:  ${BRANCH:-unbekannt}"
echo "Projekt: $ORGA / $PROJEKT"
echo "Sprache: $SPRACHE"

ausgenommen() {
    $MIT_AUSNAHMEN && return 1
    local r="$1" a
    for a in "${AUSNAHMEN[@]}"; do
        [[ "$r" == "$a" ]] && return 0
    done
    return 1
}

# Ressourcenname und zugehoerige Datei aus der .tx/config lesen. Bewusst
# eine Leseschleife statt "mapfile": das gibt es erst ab Bash 4, macOS
# liefert /bin/bash 3.2 aus. Bash 3.2 kennt auch keine assoziativen
# Arrays, daher zwei parallele Listen.
ALLE=()
PFADE=()
while IFS=$'\t' read -r name pfad; do
    [ -n "$name" ] && { ALLE+=("$name"); PFADE+=("$pfad"); }
done < <(
    awk -v o="$ORGA" -v p="$PROJEKT" '
        $0 ~ "^\\[o:" o ":p:" p ":r:" {
            r = $0; sub(/.*:r:/, "", r); sub(/\]$/, "", r); next
        }
        /^file_filter/ && r != "" {
            v = $0; sub(/^file_filter[ \t]*=[ \t]*/, "", v)
            print r "\t" v; r = ""
        }
    ' "$CONFIG"
)
if [[ ${#ALLE[@]} -eq 0 ]]; then
    echo "In $CONFIG keine Ressourcen fuer $ORGA/$PROJEKT gefunden."
    exit 1
fi

ZU_PUSHEN=()
ZU_PUSHEN_PFAD=()
UEBERSPRUNGEN=()
OHNE_DATEI=()
I=0
while [ $I -lt ${#ALLE[@]} ]; do
    r="${ALLE[$I]}"
    f="${PFADE[$I]}"
    I=$((I + 1))
    [[ -n "$NUR" && "$r" != *"$NUR"* ]] && continue
    if ausgenommen "$r"; then
        UEBERSPRUNGEN+=("$r")
        continue
    fi
    if [ ! -f "$REPO_ROOT/$f" ]; then
        OHNE_DATEI+=("$r")
        continue
    fi
    ZU_PUSHEN+=("$r")
    ZU_PUSHEN_PFAD+=("$f")
done

echo "Ressourcen: ${#ALLE[@]} insgesamt, ${#ZU_PUSHEN[@]} werden gepusht,"
echo "            ${#UEBERSPRUNGEN[@]} ausgenommen, ${#OHNE_DATEI[@]} ohne Datei"
if [ ${#UEBERSPRUNGEN[@]} -gt 0 ]; then
    for r in "${UEBERSPRUNGEN[@]}"; do
        echo "            ausgenommen: $r"
    done
fi
if [ ${#OHNE_DATEI[@]} -gt 0 ]; then
    for r in "${OHNE_DATEI[@]}"; do
        echo "            ohne Datei:  $r"
    done
fi

if $NUR_LISTE; then
    if [ ${#ZU_PUSHEN[@]} -gt 0 ]; then
        printf '%s\n' "${ZU_PUSHEN[@]}"
    fi
    exit 0
fi

if [ ${#ZU_PUSHEN[@]} -eq 0 ]; then
    echo
    echo "Keine Ressource passt auf die Auswahl -- nichts zu tun."
    exit 0
fi

echo
read -r -p "Jetzt ${#ZU_PUSHEN[@]} Ressourcen mit --force pushen? [j/N] " ANTWORT
[[ "$ANTWORT" =~ ^[jJyY]$ ]] || { echo "Abgebrochen."; exit 0; }

# --- Staging aufbauen ----------------------------------------------------
STAGING="$(mktemp -d "${TMPDIR:-/tmp}/tx_push_all.XXXXXX")" || exit 1
aufraeumen() {
    if $BEHALTEN; then
        echo "Staging behalten: $STAGING"
    else
        rm -rf "$STAGING"
    fi
}
trap aufraeumen EXIT

mkdir -p "$STAGING/.tx"
{
    echo "[main]"
    echo "host = https://www.transifex.com"
} > "$STAGING/.tx/config"

I=0
while [ $I -lt ${#ZU_PUSHEN[@]} ]; do
    r="${ZU_PUSHEN[$I]}"
    f="${ZU_PUSHEN_PFAD[$I]}"
    I=$((I + 1))
    mkdir -p "$STAGING/$SPRACHE/$(dirname "$f")"
    ln -s "$REPO_ROOT/$f" "$STAGING/$SPRACHE/$f"
    {
        echo
        echo "[o:$ORGA:p:$PROJEKT:r:$r]"
        echo "file_filter  = <lang>/$f"
        echo "source_file  = $SPRACHE/$f"
        echo "type         = PO"
        echo "minimum_perc = 0"
    } >> "$STAGING/.tx/config"
done
echo "Staging: $STAGING"

cd "$STAGING" || exit 1

OK=0
FEHLER=()
N=${#ZU_PUSHEN[@]}
I=0
for r in "${ZU_PUSHEN[@]}"; do
    I=$((I + 1))
    printf '[%3d/%3d] %s ... ' "$I" "$N" "$r"
    AUSGABE="$(tx push --translation --force "$PROJEKT.$r" 2>&1)"
    if [ $? -eq 0 ] && printf '%s' "$AUSGABE" | grep -q "Pushing translations"; then
        echo "ok"
        OK=$((OK + 1))
    else
        echo "FEHLGESCHLAGEN"
        FEHLER+=("$r")
    fi
done

echo
echo "Fertig: $OK von $N Ressourcen gepusht."
if [[ ${#FEHLER[@]} -gt 0 ]]; then
    echo "Fehlgeschlagen (${#FEHLER[@]}):"
    for r in "${FEHLER[@]}"; do
        echo "  $r"
    done
    echo
    echo "Einzeln wiederholen mit --nur <name> oder, im Staging-Verzeichnis:"
    echo "  tx push --translation --force $PROJEKT.<name>"
    exit 1
fi
