#!/usr/bin/env python3
"""Interaktiver Transifex-Push: fragt, welche Dateien hochgeladen werden.

Das Skript liest .tx/config des aktuellen Branches, ordnet jeder .po-Datei
ihren Transifex-Resource-Namen zu und stellt sie zur Auswahl. Gepusht wird
mit der forcierten Kombination, die wir beim Abgleich benutzen:

    tx push -t -l de -f --skip --replace-edited-strings <resource> ...

      -t                        nur Uebersetzungen (die Quelltexte kommen
                                aus CPython, nicht von uns)
      -l de                      nur die deutsche Sprache
      -f                        Zeitstempel-Sperre aus ("remote is newer")
      --replace-edited-strings   ueberschreibt auch in Transifex bearbeitete
                                Strings -- GitHub ist die Quelle der Wahrheit
      --skip                     bricht nicht ab, wenn eine Ressource zickt

Aufruf:
    python tools/tx_push.py                  # geaenderte Dateien vorschlagen
    python tools/tx_push.py --alle           # alle Dateien aus .tx/config
    python tools/tx_push.py howto            # nach Pfad filtern
    python tools/tx_push.py library/csv.po
    python tools/tx_push.py --dry-run howto  # nur zeigen, nicht pushen
"""

import argparse
import configparser
import re
import subprocess
import sys
from pathlib import Path

try:
    import polib
except ImportError:
    polib = None  # Fortschrittsanzeige ist dann eben leer


def git(*args: str) -> str:
    e = subprocess.run(["git", *args], capture_output=True, text=True)
    return e.stdout if e.returncode == 0 else ""


def repo_wurzel() -> Path:
    aus = git("rev-parse", "--show-toplevel").strip()
    if not aus:
        sys.exit("Kein Git-Repository -- bitte im python-docs-de-Verzeichnis starten.")
    return Path(aus)


def ressourcen(wurzel: Path) -> dict:
    """{po-Pfad: (projekt, resource)} aus .tx/config."""
    pfad = wurzel / ".tx" / "config"
    if not pfad.is_file():
        sys.exit(f"{pfad} nicht gefunden.")

    cfg = configparser.ConfigParser()
    cfg.read(pfad, encoding="utf-8")

    aus = {}
    for name in cfg.sections():
        # [o:python-doc:p:python-314:r:howto--index]
        m = re.match(r"o:([^:]+):p:([^:]+):r:(.+)", name)
        if not m:
            continue
        _org, projekt, resource = m.groups()
        abschnitt = cfg[name]
        datei = abschnitt.get("trans.de") or abschnitt.get("file_filter", "")
        datei = datei.replace("<lang>", "de").strip()
        if datei:
            aus[datei] = (projekt, resource)
    if not aus:
        sys.exit("In .tx/config wurden keine Ressourcen gefunden.")
    return aus


def geaenderte_dateien(wurzel: Path) -> set:
    """.po-Dateien, die sich gegenueber origin/<branch> oder im Baum geaendert haben."""
    branch = git("branch", "--show-current").strip()
    kandidaten = set()
    for befehl in (
        ["diff", "--name-only"],                       # unversionierte Aenderungen
        ["diff", "--name-only", "--cached"],           # gestaged
        ["diff", "--name-only", f"origin/{branch}...HEAD"],  # noch nicht gepusht
    ):
        for zeile in git(*befehl).splitlines():
            if zeile.endswith(".po"):
                kandidaten.add(zeile)
    return kandidaten


def stand(wurzel: Path, datei: str) -> str:
    """'123/456 (27 %)' -- oder leer, wenn polib fehlt."""
    if polib is None:
        return ""
    p = wurzel / datei
    if not p.is_file():
        return "fehlt lokal"
    try:
        po = polib.pofile(str(p))
    except Exception:
        return "nicht lesbar"
    gesamt = len([e for e in po if not e.obsolete])
    fertig = len([e for e in po if not e.obsolete and e.translated()])
    prozent = 100 * fertig // gesamt if gesamt else 0
    return f"{fertig}/{gesamt} ({prozent} %)"


def auswahl_lesen(anzahl: int) -> list:
    """'1,3-5' oder 'a' einlesen und in Indizes uebersetzen."""
    while True:
        roh = input("\nNummern (z. B. 1,3-5), a = alle, q = Abbruch: ").strip().lower()
        if roh in ("q", ""):
            sys.exit("Abgebrochen.")
        if roh == "a":
            return list(range(anzahl))
        indizes = set()
        try:
            for teil in roh.replace(" ", "").split(","):
                if "-" in teil:
                    von, bis = teil.split("-", 1)
                    indizes.update(range(int(von) - 1, int(bis)))
                else:
                    indizes.add(int(teil) - 1)
        except ValueError:
            print("Das habe ich nicht verstanden.")
            continue
        if any(i < 0 or i >= anzahl for i in indizes):
            print(f"Nur 1 bis {anzahl} sind gueltig.")
            continue
        return sorted(indizes)


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("muster", nargs="*", help="Pfadteile zum Filtern, z. B. howto")
    p.add_argument("--alle", action="store_true",
                   help="alle Dateien aus .tx/config zur Auswahl stellen")
    p.add_argument("--dry-run", action="store_true",
                   help="Befehl nur anzeigen, nicht ausfuehren")
    args = p.parse_args()

    wurzel = repo_wurzel()
    branch = git("branch", "--show-current").strip()
    karte = ressourcen(wurzel)
    projekt = next(iter(karte.values()))[0]

    dateien = sorted(karte)
    herkunft = "alle Ressourcen aus .tx/config"

    if args.muster:
        dateien = [d for d in dateien if any(m in d for m in args.muster)]
        herkunft = "Treffer fuer " + ", ".join(args.muster)
    elif not args.alle:
        geaendert = geaenderte_dateien(wurzel) & set(karte)
        if geaendert:
            dateien = sorted(geaendert)
            herkunft = "geaenderte Dateien"
        else:
            print("Keine geaenderten .po-Dateien gefunden -- zeige alle.\n")

    if not dateien:
        sys.exit("Keine passende Datei gefunden.")

    print(f"Branch {branch}  ->  Transifex-Projekt {projekt}   ({herkunft})\n")
    breite = max(len(d) for d in dateien)
    for i, d in enumerate(dateien, 1):
        print(f"  {i:>3}  {d:<{breite}}   {karte[d][1]:<28} {stand(wurzel, d)}")

    gewaehlt = [dateien[i] for i in auswahl_lesen(len(dateien))]
    ziele = [f"{karte[d][0]}.{karte[d][1]}" for d in gewaehlt]

    befehl = ["tx", "push", "-t", "-l", "de", "-f", "--skip",
              "--replace-edited-strings", *ziele]

    print("\nBefehl:\n  " + " ".join(befehl) + "\n")
    for d in gewaehlt:
        print(f"  {d}  ->  {karte[d][1]}")

    if args.dry_run:
        print("\n--dry-run: nichts gepusht.")
        return

    if input("\nJetzt pushen? [j/N] ").strip().lower() not in ("j", "ja"):
        sys.exit("Abgebrochen.")

    print()
    sys.exit(subprocess.run(befehl, cwd=wurzel).returncode)


if __name__ == "__main__":
    main()
