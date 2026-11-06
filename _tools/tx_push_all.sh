#!/usr/bin/env bash
#
# tx_push_all.sh -- Uebersetzungen Ressource fuer Ressource nach Transifex
# schieben. Das Repo ist dabei die Quelle der Wahrheit: mit --force werden
# auch Strings ueberschrieben, die in Transifex von Hand bearbeitet wurden
# (ohne diesen Schalter laesst Transifex sie unangetastet, siehe
# replace_edited_strings in .tx/config).
#
# Ein Aufruf pro Ressource statt eines grossen Pushes, damit ein einzelner
# Fehlschlag den Rest nicht aufhaelt. Was fehlschlaegt, steht am Ende noch
# einmal gesammelt da.
#
# Voraussetzungen:
#   * tx-CLI installiert und im PATH
#   * API-Token in ~/.transifexrc (NICHT im Repo, nicht in dieser Datei)
#
# Nutzung:
#   ./_tools/tx_push_all.sh                     # alles ausser AUSNAHMEN
#   ./_tools/tx_push_all.sh --liste             # nur zeigen, was gepusht wuerde
#   ./_tools/tx_push_all.sh --nur library--     # nur passende Ressourcen
#   ./_tools/tx_push_all.sh --ohne-ausnahmen    # wirklich alles, auch die
#                                               # Dateien in AUSNAHMEN
#
set -uo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CONFIG="$REPO_ROOT/.tx/config"
ORGA="${ORGA:-python-doc}"
PROJEKT="${PROJEKT:-python-newest}"

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

while [[ $# -gt 0 ]]; do
    case "$1" in
        --liste)          NUR_LISTE=true ;;
        --ohne-ausnahmen) MIT_AUSNAHMEN=true ;;
        --nur)            NUR="${2:-}"; shift ;;
        -h|--help)        sed -n '2,24p' "${BASH_SOURCE[0]}"; exit 0 ;;
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

ausgenommen() {
    $MIT_AUSNAHMEN && return 1
    local r="$1" a
    for a in "${AUSNAHMEN[@]}"; do
        [[ "$r" == "$a" ]] && return 0
    done
    return 1
}

# Ressourcennamen aus den Abschnittskoepfen der .tx/config lesen
mapfile -t ALLE < <(
    grep -o "^\[o:$ORGA:p:$PROJEKT:r:[^]]*\]" "$CONFIG" \
        | sed "s/.*:r://; s/\]//"
)
if [[ ${#ALLE[@]} -eq 0 ]]; then
    echo "In $CONFIG keine Ressourcen fuer $ORGA/$PROJEKT gefunden."
    exit 1
fi

ZU_PUSHEN=()
UEBERSPRUNGEN=()
for r in "${ALLE[@]}"; do
    [[ -n "$NUR" && "$r" != *"$NUR"* ]] && continue
    if ausgenommen "$r"; then
        UEBERSPRUNGEN+=("$r")
        continue
    fi
    ZU_PUSHEN+=("$r")
done

echo "Ressourcen: ${#ALLE[@]} insgesamt, ${#ZU_PUSHEN[@]} werden gepusht,"
echo "            ${#UEBERSPRUNGEN[@]} ausgenommen"
for r in "${UEBERSPRUNGEN[@]}"; do
    echo "            ausgenommen: $r"
done

if $NUR_LISTE; then
    printf '%s\n' "${ZU_PUSHEN[@]}"
    exit 0
fi

echo
read -r -p "Jetzt ${#ZU_PUSHEN[@]} Ressourcen mit --force pushen? [j/N] " ANTWORT
[[ "$ANTWORT" =~ ^[jJyY]$ ]] || { echo "Abgebrochen."; exit 0; }

cd "$REPO_ROOT" || exit 1

OK=0
FEHLER=()
N=${#ZU_PUSHEN[@]}
I=0
for r in "${ZU_PUSHEN[@]}"; do
    I=$((I + 1))
    printf '[%3d/%3d] %s ... ' "$I" "$N" "$r"
    if tx push --translation --force --resource "$PROJEKT.$r" >/dev/null 2>&1; then
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
    echo "Einzeln wiederholen mit:"
    echo "  tx push --translation --force --resource $PROJEKT.<name>"
    exit 1
fi
