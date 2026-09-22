#!/usr/bin/env python3
"""
po_status.py — listet alles .po-Dateien in einem Verzeichnisbaum mit
Übersetzungsstand (x/y), Prozent, Dateigröße und Pfad und Status Gesamtübersetzung.
Gleicht Strings mit englischen Original-Dateien ab.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

STATS_RE = re.compile(
    r"(?:(\d+) translated messages?)?"
    r"(?:, (\d+) fuzzy translations?)?"
    r"(?:, (\d+) untranslated messages?)?"
)
CORE_FILES = {"bugs.po", "builtins/functions.po"}
CORE_DIRS = ("tutorial/",)
FUZZY_FLAG_RE = re.compile(r"^#,.*\bfuzzy\b", re.MULTILINE)


def get_stats(po_file: Path):
    """Ruft msgfmt --statistics auf und parst das Ergebnis."""
    try:
        result = subprocess.run(
            ["msgfmt", "--statistics", "-o", "/dev/null", str(po_file)],
            capture_output=True, text=True, timeout=15,
        )
    except FileNotFoundError:
        sys.exit("Fehler: 'msgfmt' wurde nicht gefunden. Ist gettext installiert "
                 "(z.B. 'brew install gettext' + PATH-Anpassung)?")

    output = (result.stderr or "") + (result.stdout or "")
    if "error" in output.lower() and "translated" not in output.lower():
        return None  # Syntaxfehler in der Datei

    m = STATS_RE.search(output)
    if not m:
        return {"translated": 0, "fuzzy": 0, "untranslated": 0}
    translated, fuzzy, untranslated = (int(x) if x else 0 for x in m.groups())
    return {"translated": translated, "fuzzy": fuzzy, "untranslated": untranslated}


def count_fuzzy_flags(po_file: Path) -> int:
    """Zählt alle fuzzy-Markierungen direkt im Dateitext."""
    text = po_file.read_text(encoding="utf-8", errors="replace")
    return len(FUZZY_FLAG_RE.findall(text))


def is_core(rel_path: Path) -> bool:
    """Prüft, ob die Datei zu den Pflichtartikeln gehört."""
    rel = rel_path.as_posix()
    return rel in CORE_FILES or rel.startswith(CORE_DIRS)


def find_missing(pot_dir: Path, root: Path, excludes: set) -> list:
    """Liefert .po-Pfade, zu denen es eine Vorlage, aber keine Übersetzung gibt."""
    missing = []
    for pot in sorted(pot_dir.rglob("*.pot")):
        rel = pot.relative_to(pot_dir).with_suffix(".po")
        if excludes.intersection(rel.parts):
            continue
        if not (root / rel).exists():
            missing.append(rel)
    return missing


def human_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB"):
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}" if unit == "B" else f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} GB"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", default=".", help="Wurzelverzeichnis (Standard: .)")
    parser.add_argument("--exclude", default="c-api,.venv,.git",
                         help="Kommagetrennte Ordnernamen, die übersprungen werden")
    parser.add_argument("--sort", choices=["path", "percent", "size"], default="percent")
    parser.add_argument("--max-percent", type=float, default=100.1,
                         help="Nur Dateien mit weniger als diesem Prozentwert anzeigen")
    parser.add_argument("--pot-dir",
                        help="Ordner mit .pot-Vorlagen; listet Seiten ohne .po-Datei")

    args = parser.parse_args()

    root = Path(args.path).resolve()
    excludes = {e.strip() for e in args.exclude.split(",") if e.strip()}

    po_files = sorted(
        p for p in root.rglob("*.po")
        if not excludes.intersection(p.relative_to(root).parts)
    )

    if not po_files:
        print(f"Keine .po-Dateien unter {root} gefunden.")
        return

    rows = []
    for po_file in po_files:
        stats = get_stats(po_file)
        rel_path = po_file.relative_to(root)
        size = po_file.stat().st_size
        marker = "* " if is_core(rel_path) else "  "
        if stats is None:
            rows.append((marker + str(rel_path), "FEHLER (Syntax)", -1.0, size))
            continue
        total = stats["translated"] + stats["fuzzy"] + stats["untranslated"]
        pct = (stats["translated"] / total * 100) if total else 100.0
        label = f"{stats['translated']}/{total}"
        fuzzy_count = count_fuzzy_flags(po_file)
        if fuzzy_count:
            label += f" ({fuzzy_count} fuzzy)"
        rows.append((marker + str(rel_path), label, pct, size))

    # Gesamtstatistik wird VOR dem --max-percent-Filter berechnet (über alle Dateien)
    complete_count = sum(1 for r in rows if r[2] >= 100.0)
    error_count = sum(1 for r in rows if r[2] < 0)
    total_translated = sum(int(r[1].split("/")[0]) for r in rows if r[2] >= 0)
    total_strings = sum(int(r[1].split("/")[1].split(" ")[0]) for r in rows if r[2] >= 0)
    overall_pct = (total_translated / total_strings * 100) if total_strings else 0.0

    rows = [r for r in rows if r[2] < args.max_percent or r[2] < 0]

    if not rows:
        print(f"Alle {len(po_files)} Dateien liegen bei/über --max-percent {args.max_percent} "
              f"— nichts anzuzeigen.")
        return

    if args.sort == "percent":
        rows.sort(key=lambda r: r[2], reverse=True)  # 100% -> 0%
    elif args.sort == "size":
        rows.sort(key=lambda r: -r[3])

    path_w = max(len(r[0]) for r in rows) + 2
    label_w = max(len(r[1]) for r in rows) + 2

    print(f"{'  Pfad':<{path_w}}{'Übersetzt':<{label_w}}{'%':>7}   {'Größe':>8}")
    print("-" * (path_w + label_w + 20))
    for rel_path, label, pct, size in rows:
        pct_str = "  n/a" if pct < 0 else f"{pct:6.1f}%"
        print(f"{rel_path:<{path_w}}{label:<{label_w}}{pct_str:>7}   {human_size(size):>8}")

    print("-" * (path_w + label_w + 20))
    print(f"{len(rows)} von {len(po_files)} Dateien angezeigt "
          f"(Filter: --max-percent {args.max_percent})")
    print()
    print(f"Vollständig übersetzt (100%): {complete_count} von {len(po_files)} Dateien")
    if error_count:
        print(f"Dateien mit Syntaxfehler:      {error_count}")
    print(f"Gesamtstand über alle Dateien:  {total_translated}/{total_strings} Strings "
          f"({overall_pct:.2f}%)")
    print()
    print("* Pflichtdatei für den Sprachumschalter")

    if args.pot_dir:
        missing = find_missing(Path(args.pot_dir).resolve(), root, excludes)
        print()
        if missing:
            print(f"Fehlende Übersetzungsdateien ({len(missing)}):")
            for rel in missing:
                marker = "* " if is_core(rel) else "  "
                print(f"{marker}{rel}")
        else:
            print("Keine fehlenden Übersetzungsdateien.")


if __name__ == "__main__":
    main()
