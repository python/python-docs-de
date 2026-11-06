#!/usr/bin/env python3
"""
check_satzzeichen.py — Prüft die deutschen Zeichensetzungsregeln aus
_doc/AI-SKILLS.md gegen die msgstr-Felder von .po-Dateien, ohne Sphinx-Build.

Geprüft werden zwei Fehlerklassen, die beim Übersetzen mechanisch aus dem
englischen Original mitwandern:

  semikolon  Ein Semikolon verbindet zwei vollständige Hauptsätze. Im
             Deutschen steht dort ein Punkt mit Großschreibung (oder ein
             Komma, wenn der Satz es trägt). Erlaubt bleibt das Semikolon
             zwischen gleichrangigen Gliedern einer Aufzählung, etwa
             parallelen "dass"-Sätzen — die erkennt der Check und übergeht
             sie.
  abstand    Zwei Leerzeichen nach dem Satzende. Das englische Original
             setzt sie oft, im Deutschen steht eines.

Übergangen werden immer: der PO-Kopf (msgid ""), veraltete Einträge (#~),
leere msgstr und Einträge, deren msgstr wörtlich dem msgid entspricht —
das sind die unübersetzten Codeblöcke, in denen ein Semikolon dazugehört.

Nutzung:
    check_satzzeichen.py <verzeichnis-oder-datei> [optionen]

Optionen:
    --exclude dir1,dir2   Verzeichnisse überspringen
    --nur-geaendert       Nur Dateien prüfen, die git gegenüber HEAD als
                          geändert oder unverfolgt meldet. Damit blockiert
                          der Check neue Fehler, ohne am Altbestand
                          hängenzubleiben.
    --mit-abstand         Auch die abstand-Funde in den Rückgabewert
                          einrechnen (sonst nur gezählt und angezeigt)
    --max N               So viele gewertete Funde sind noch in Ordnung
                          (Vorgabe 0)
    --fix                 Funde beheben statt nur melden: Semikolon wird
                          Punkt + Großbuchstabe, doppelter Abstand wird
                          einfacher. Nur mit --mit-abstand auch der Abstand.

Rückgabewert 1, sobald mehr als --max gewertete Funde übrig sind.
"""
import re
import subprocess
import sys
from pathlib import Path

# "; " gefolgt von einem Kleinbuchstaben
SEMIKOLON_RE = re.compile(r"; (?=[a-zäöüß])")
# Satzende, dann zwei oder mehr Leerzeichen, dann ein Satzanfang
ABSTAND_RE = re.compile(r"(?<=[.!?])  +(?=[A-ZÄÖÜ„*`\"'])")

KLEIN = "aäbcdefghijklmnoöpqrstuüvwxyzß"


def po_bloecke(text: str) -> list[list[str]]:
    """Teilt den Dateiinhalt an Leerzeilen in Einträge."""
    bloecke, akt = [], []
    for zeile in text.split("\n"):
        akt.append(zeile)
        if zeile == "":
            bloecke.append(akt)
            akt = []
    if akt:
        bloecke.append(akt)
    return bloecke


def entschluesseln(zeilen: list[str]) -> str:
    """Hängt die Zeichenketten einer Folge von PO-Zeilen aneinander."""
    teile = []
    for zeile in zeilen:
        zeile = zeile.strip()
        a, b = zeile.find('"'), zeile.rfind('"')
        if a >= 0 and b > a:
            teile.append(zeile[a + 1:b])
    return "".join(teile)


def rst_zeile(zeilen: list[str]) -> str:
    """Liest die Quellzeile aus dem #: -Kommentar des Eintrags."""
    for zeile in zeilen:
        if zeile.startswith("#:"):
            m = re.search(r":(\d+)", zeile)
            if m:
                return m.group(1)
    return "?"


def ist_aufzaehlung(msgstr: str, pos: int) -> bool:
    """
    Gleichrangige Glieder statt zweier Hauptsätze? Dann ist das Semikolon
    richtig. Erkannt wird das daran, dass dasselbe einleitende Wort vor und
    nach dem Semikolon steht, etwa "..., dass A; dass B; und dass C".
    """
    BINDEWOERTER = {"und", "oder", "sowie", "aber", "beziehungsweise", "bzw."}
    danach = msgstr[pos + 2:pos + 40].split()
    if not danach:
        return False
    # Ein "; und dass …" leitet dasselbe Glied ein wie "; dass …", darum das
    # Bindewort überspringen und das Wort dahinter prüfen.
    kandidaten = [danach[0]]
    if danach[0].strip(",.:;").lower() in BINDEWOERTER and len(danach) > 1:
        kandidaten.append(danach[1])
    for roh in kandidaten:
        wort = roh.strip(",.:;")
        if len(wort) < 3:
            continue
        if re.search(r"\b%s\b" % re.escape(wort), msgstr[:pos]):
            return True
    return False


def pruefe_datei(pfad: Path, fix: bool, mit_abstand: bool):
    """Liefert (funde, geaendert). funde: Liste von (art, rst, auszug)."""
    original = pfad.read_text(encoding="utf-8", errors="replace")
    bloecke = po_bloecke(original)
    funde = []
    geaendert = False

    for block in bloecke:
        if any(z.startswith("#~") for z in block):
            continue
        ia = next((k for k, z in enumerate(block) if z.startswith("msgid ")), None)
        sa = next((k for k, z in enumerate(block) if z.startswith("msgstr")), None)
        if ia is None or sa is None or sa <= ia:
            continue
        msgid = entschluesseln(block[ia:sa])
        msgstr = entschluesseln(block[sa:])
        if msgid == "" or not msgstr or msgstr == msgid:
            continue

        rst = rst_zeile(block)
        semi_offen = 0          # Semikolon-Funde, die zu beheben sind
        semi_aufzaehlung = 0    # richtige Semikolons in diesem Eintrag

        for m in SEMIKOLON_RE.finditer(msgstr):
            i = m.start()
            if ist_aufzaehlung(msgstr, i):
                semi_aufzaehlung += 1
                continue
            semi_offen += 1
            funde.append(("semikolon", rst,
                          msgstr[max(0, i - 45):i + 55].replace("\n", " ")))
        for m in ABSTAND_RE.finditer(msgstr):
            i = m.start()
            funde.append(("abstand", rst,
                          msgstr[max(0, i - 45):i + 55].replace("\n", " ")))

        if not fix:
            continue

        # --- Reparatur, zeilenweise auf dem Rohtext ----------------------
        # Enthaelt ein Eintrag auch ein richtiges Semikolon (Aufzaehlung),
        # bleibt er beim Semikolon unangetastet: lieber von Hand nachsehen
        # als eine richtige Stelle kaputtmachen.
        semi_fix = semi_offen > 0 and semi_aufzaehlung == 0

        for k in range(sa, len(block)):
            alt = block[k]
            neu = alt

            if semi_fix:
                # Semikolon samt Fortsetzung in derselben Zeile
                neu = re.sub(r"; ([a-zäöüß])",
                             lambda m: ". " + m.group(1).upper(), neu)
                # Semikolon am Zeilenende, Fortsetzung in der naechsten Zeile
                if neu.endswith('; "') and k + 1 < len(block):
                    nx = block[k + 1].lstrip()
                    if len(nx) > 1 and nx[0] == '"' and nx[1] in KLEIN:
                        neu = neu[:-3] + '. "'
                        block[k + 1] = block[k + 1].replace(
                            '"' + nx[1], '"' + nx[1].upper(), 1)
                        geaendert = True

            if mit_abstand:
                neu = ABSTAND_RE.sub(" ", neu)

            if neu != alt:
                block[k] = neu
                geaendert = True

    if fix and geaendert:
        pfad.write_text("\n".join("\n".join(b) for b in bloecke),
                        encoding="utf-8")
    return funde, geaendert


def geaenderte_dateien(root: Path) -> set[Path] | None:
    """Dateien, die git gegenueber HEAD als geaendert oder neu meldet."""
    try:
        a = subprocess.run(["git", "-C", str(root), "diff", "--name-only", "HEAD"],
                           capture_output=True, text=True, check=True).stdout
        b = subprocess.run(["git", "-C", str(root), "ls-files", "--others",
                            "--exclude-standard"],
                           capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {(root / z).resolve() for z in (a + b).split("\n") if z.strip()}


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    root = Path(sys.argv[1])
    argv = sys.argv[2:]
    excludes = set()
    if "--exclude" in argv:
        excludes = set(argv[argv.index("--exclude") + 1].split(","))
    hoechst = 0
    if "--max" in argv:
        hoechst = int(argv[argv.index("--max") + 1])
    fix = "--fix" in argv
    mit_abstand = "--mit-abstand" in argv
    nur_geaendert = "--nur-geaendert" in argv

    if root.is_file():
        dateien = [root]
    else:
        dateien = sorted(p for p in root.rglob("*.po")
                         if not excludes.intersection(p.relative_to(root).parts))

    uebersprungen = 0
    if nur_geaendert:
        erlaubt = geaenderte_dateien(root if root.is_dir() else root.parent)
        if erlaubt is None:
            print("git nicht verfuegbar -- --nur-geaendert wird ignoriert.")
        else:
            vorher = len(dateien)
            dateien = [p for p in dateien if p.resolve() in erlaubt]
            uebersprungen = vorher - len(dateien)

    zahl = {"semikolon": 0, "abstand": 0}
    betroffen = 0
    repariert = 0
    for pfad in dateien:
        funde, g = pruefe_datei(pfad, fix, mit_abstand)
        if g:
            repariert += 1
        if not funde:
            continue
        betroffen += 1
        rel = pfad.relative_to(root) if root.is_dir() else pfad
        print(f"\n{rel}")
        for art, rst, auszug in funde:
            zahl[art] += 1
            print(f"  rst:{rst:<6} [{art}]  …{auszug}…")

    gewertet = zahl["semikolon"] + (zahl["abstand"] if mit_abstand else 0)

    print(f"\n{'=' * 60}")
    print(f"{zahl['semikolon']} Semikolon-Fund(e), {zahl['abstand']} Fund(e) mit "
          f"doppeltem Satzabstand in {betroffen} von {len(dateien)} geprueften Dateien.")
    if uebersprungen:
        print(f"{uebersprungen} unveraenderte Datei(en) uebersprungen (--nur-geaendert).")
    if not mit_abstand and zahl["abstand"]:
        print("Der Satzabstand ist nur gemeldet, nicht gewertet -- "
              "mit --mit-abstand zaehlt er mit.")
    if fix:
        print(f"{repariert} Datei(en) geaendert (--fix).")
    if gewertet > hoechst:
        print(f"Erlaubt waren {hoechst}. Regeln: _doc/AI-SKILLS.md, Abschnitt "
              f"Zeichensetzung.")
    sys.exit(1 if gewertet > hoechst else 0)


if __name__ == "__main__":
    main()
