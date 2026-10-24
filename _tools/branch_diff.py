#!/usr/bin/env python3
"""Vergleicht die Uebersetzungen zweier Branches Datei fuer Datei.

Fuer jede .po-Datei wird verglichen, wie viele Eintraege in beiden Branches
denselben msgstr haben. Der Prozentwert bezieht sich auf die Anzahl der
Eintraege im *neueren* Branch (Vorgabe 3.15), weil der die Zielversion ist:

    Aehnlichkeit = identische Eintraege / Eintraege in 3.15

Ein Eintrag gilt als identisch, wenn msgid (samt msgctxt) und msgstr in
beiden Branches exakt uebereinstimmen -- auch dann, wenn beide leer sind.
Obsolete Eintraege (#~) und der Kopfblock bleiben aussen vor.

Aufruf:
    python branch_diff.py                 # 3.14 gegen 3.15
    python branch_diff.py 3.14 main
    python branch_diff.py --csv bericht.csv
    python branch_diff.py --nur-abweichungen

Es wird nichts ausgecheckt und nichts geaendert -- die Inhalte kommen
ueber "git show" direkt aus den Branches.
"""

import argparse
import csv
import os
import subprocess
import sys
import tempfile

try:
    import polib
except ImportError:
    sys.exit("polib fehlt. Im aktiven venv installieren: pip install polib")

AUSSCHLUSS = (".venv/", ".git/")

KLASSEN = [
    (100.0, "deckungsgleich"),
    (80.0, "ueber 80 %"),
    (50.0, "ueber 50 %"),
    (30.0, "ueber 30 %"),
    (0.0, "unter 30 %"),
]


def git(*args: str) -> str:
    """git aufrufen und stdout zurueckgeben."""
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout


def po_dateien(branch: str) -> dict:
    """Alle .po-Dateien eines Branches als {pfad: blob-hash}."""
    aus = {}
    for zeile in git("ls-tree", "-r", branch).splitlines():
        kopf, pfad = zeile.split("\t", 1)
        _modus, art, blob = kopf.split()
        if art != "blob" or not pfad.endswith(".po"):
            continue
        if pfad.startswith(AUSSCHLUSS):
            continue
        aus[pfad] = blob
    return aus


def eintraege(blob: str) -> dict:
    """Blob-Inhalt parsen: {(msgctxt, msgid): msgstr}."""
    inhalt = git("cat-file", "blob", blob)
    # polib will einen Dateipfad -- also kurz zwischenspeichern.
    with tempfile.NamedTemporaryFile(
        "w", suffix=".po", encoding="utf-8", delete=False
    ) as f:
        f.write(inhalt)
        tmp = f.name
    try:
        po = polib.pofile(tmp)
        return {(e.msgctxt, e.msgid): e.msgstr for e in po if not e.obsolete}
    finally:
        os.unlink(tmp)


def klasse_von(prozent: float) -> str:
    for grenze, name in KLASSEN:
        if prozent >= grenze:
            return name
    return KLASSEN[-1][1]


def uebersetzt(werte) -> int:
    return sum(1 for v in werte if v.strip())


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("alt", nargs="?", default="3.14", help="aelterer Branch")
    p.add_argument("neu", nargs="?", default="3.15", help="neuerer Branch")
    p.add_argument("--csv", metavar="DATEI", help="Ergebnis zusaetzlich als CSV")
    p.add_argument(
        "--nur-abweichungen",
        action="store_true",
        help="deckungsgleiche Dateien in der Tabelle weglassen",
    )
    args = p.parse_args()

    alt_dateien = po_dateien(args.alt)
    neu_dateien = po_dateien(args.neu)
    alle = sorted(set(alt_dateien) | set(neu_dateien))
    print(f"{len(alle)} Dateien werden verglichen ...", file=sys.stderr)

    zeilen = []
    for nr, pfad in enumerate(alle, 1):
        if nr % 50 == 0:
            print(f"  {nr}/{len(alle)}", file=sys.stderr)

        a_blob = alt_dateien.get(pfad)
        n_blob = neu_dateien.get(pfad)

        if a_blob is None:
            n = eintraege(n_blob)
            zeilen.append((pfad, 0, len(n), 0, uebersetzt(n.values()),
                           0, None, f"nur in {args.neu}"))
            continue
        if n_blob is None:
            a = eintraege(a_blob)
            zeilen.append((pfad, len(a), 0, uebersetzt(a.values()), 0,
                           0, None, f"nur in {args.alt}"))
            continue

        if a_blob == n_blob:
            # Gleicher Blob -- Inhalt garantiert identisch, kein Parsen noetig.
            a = eintraege(a_blob)
            u = uebersetzt(a.values())
            zeilen.append((pfad, len(a), len(a), u, u, len(a), 100.0,
                           "deckungsgleich"))
            continue

        a = eintraege(a_blob)
        n = eintraege(n_blob)
        gleich = sum(1 for k, v in n.items() if k in a and a[k] == v)
        prozent = 100.0 * gleich / len(n) if n else 0.0
        zeilen.append((pfad, len(a), len(n), uebersetzt(a.values()),
                       uebersetzt(n.values()), gleich, prozent,
                       klasse_von(prozent)))

    # --- Tabelle -----------------------------------------------------------
    rang = {name: i for i, (_g, name) in enumerate(KLASSEN)}
    rang[f"nur in {args.neu}"] = 90
    rang[f"nur in {args.alt}"] = 91
    zeilen.sort(key=lambda z: (rang.get(z[7], 99), -(z[6] or 0), z[0]))

    kopf = (f"| Datei | Eintraege {args.alt} | Eintraege {args.neu} | "
            f"uebers. {args.alt} | uebers. {args.neu} | identisch | "
            f"Aehnlichkeit | Klasse |")
    print()
    print(kopf)
    print("|---|---:|---:|---:|---:|---:|---:|---|")
    for pfad, ea, en, ua, un, gl, pz, kl in zeilen:
        if args.nur_abweichungen and kl == "deckungsgleich":
            continue
        pzt = "—" if pz is None else f"{pz:.1f} %"
        print(f"| `{pfad}` | {ea} | {en} | {ua} | {un} | {gl} | {pzt} | {kl} |")

    # --- Zusammenfassung ---------------------------------------------------
    print("\n### Zusammenfassung\n")
    print("| Klasse | Dateien |")
    print("|---|---:|")
    for _grenze, name in KLASSEN:
        anzahl = sum(1 for z in zeilen if z[7] == name)
        print(f"| {name} | {anzahl} |")
    for name in (f"nur in {args.neu}", f"nur in {args.alt}"):
        anzahl = sum(1 for z in zeilen if z[7] == name)
        if anzahl:
            print(f"| {name} | {anzahl} |")
    print(f"| **gesamt** | **{len(zeilen)}** |")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["datei", f"eintraege_{args.alt}", f"eintraege_{args.neu}",
                        f"uebersetzt_{args.alt}", f"uebersetzt_{args.neu}",
                        "identisch", "aehnlichkeit_prozent", "klasse"])
            for z in zeilen:
                w.writerow([z[0], z[1], z[2], z[3], z[4], z[5],
                            "" if z[6] is None else f"{z[6]:.1f}", z[7]])
        print(f"\nCSV geschrieben: {args.csv}", file=sys.stderr)


if __name__ == "__main__":
    main()
