#!/usr/bin/env python3
"""check_markup.py -- Findet Auszeichnungsfehler in deutschen .po-Uebersetzungen.

Ergaenzt check_roles.py: dort geht es um fehlende oder ueberzaehlige Rollen,
hier um Schaeden *innerhalb* der Auszeichnung, die Sphinx entweder gar nicht
meldet oder erst als Folgefehler. Die meisten stammen aus maschineller
Voruebersetzung, bei der reST-Syntax wie Fließtext behandelt wurde.

Geprueft werden sechs Fehlerarten (Kuerzel fuer --art):

  klammer     Ueberfluessige Backtick- oder Stern-Klammer um eine Rolle:
                  Ein ` :class:`tuple` `, der ...
              Sphinx paart Backticks von links nach rechts. Das einzelne
              Backtick findet seinen Partner im oeffnenden Backtick der Rolle,
              und ab da verrutscht die Paarung ueber den ganzen Satz -- alle
              folgenden Querverweise werden zu gewoehnlichem Text.

  anzeige     Rolle ohne Anzeigetext:  :term:` <parameter>`
              Der sichtbare Text ist beim Uebersetzen verloren gegangen.

  code        Codeblock, dessen Uebersetzung ausserhalb von Kommentarzeilen
              vom Original abweicht. Betrifft uebersetzte Schluesselwoerter
              (">>> x ist 7"), eingedeutschte Interpreter-Ausgaben
              ("Traceback (letzter Aufruf zuletzt):") und Beispiele, deren
              Eingabe und Ausgabe nicht mehr zueinander passen.

  literal     ``Literale`` aus dem Original fehlen in der Uebersetzung.
              Literale sind Code und duerfen nicht uebersetzt werden.
              Zusaetzliche Literale in der Uebersetzung sind erlaubt.

  typo        Typografische Anfuehrungszeichen innerhalb von Code oder
              Literalen:  "hello“  statt  "hello"

  verweis     Benannte Hyperlink-Verweise (`Text`_ oder `Text <url>`_) fehlen
              in der Uebersetzung oder haben den abschliessenden Unterstrich
              verloren. Ohne ihn ist es kein Verweis mehr, sondern Kursivtext.

  bindestrich Leerzeichen zwischen Rolle und angehaengtem Wort:
                  :exc:`GeneratorExit` -Ausnahme
              Technisch harmlos, im Satz aber ein Fremdkoerper.

Das Skript aendert nichts. Es meldet nur, wo etwas zu tun ist -- die
Korrekturen sind oft Ermessensfragen und gehoeren von Hand entschieden.

Aufruf:
    python tools/check_markup.py                      # ganzes Repo
    python tools/check_markup.py reference library    # nur diese Pfade
    python tools/check_markup.py --art code,klammer   # nur diese Fehlerarten
    python tools/check_markup.py --max 5              # je Art hoechstens 5 Beispiele
    python tools/check_markup.py -o bericht.md        # Markdown-Bericht schreiben
    python tools/check_markup.py --nur-zahlen         # nur die Zusammenfassung

Rueckgabewert: 0 wenn nichts gefunden wurde, sonst 1 -- damit laesst sich das
Skript in pre_push_check.sh und in die CI einhaengen.

Es werden nur .po-Dateien gelesen; nichts wird geschrieben.
"""

import argparse
import re
import sys
from pathlib import Path

AUSSCHLUSS = [".venv", ".git", "cpython-src", "__pycache__", "locales"]

# --- Fehlermuster ----------------------------------------------------------

ROLLE = r":[a-zA-Z][\w-]*:`"

MUSTER = {
    "klammer": [
        # Ein '*' direkt nach einem Wort schliesst eine Hervorhebung
        # (*keine* :attr:`...`) und ist kein Fehler.
        (re.compile(r'(?<![\w*])\*[ \t]+' + ROLLE), "Stern vor Rolle"),
        (re.compile(ROLLE + r'[^`]*`[ \t]*\*(?!\*)(?=[\s,.;:)])'), "Stern nach Rolle"),
    ],
    "anzeige": [
        (re.compile(ROLLE + r'[ \t]*<'), "Rolle ohne Anzeigetext"),
    ],
    "bindestrich": [
        (re.compile(r'(?:' + ROLLE + r'[^`]*`|``[^`]+``)[ \t]+-[A-Za-zÄÖÜäöüß]'),
         "Leerzeichen vor Bindestrich"),
    ],
}

# Spans, die zu gueltiger Auszeichnung gehoeren -- alles andere ist ein
# einzelnes, "loses" Backtick.
GUELTIG = re.compile(
    r'``[^`]+``'                      # ``Literal``
    r'|:[a-zA-Z][\w-]*:`[^`]*`'       # :rolle:`Text`
    r'|`[^`]+`__?'                    # `Link <url>`_ bzw. `_
)


def lose_klammer(text: str) -> str:
    """Meldet eine ueberfluessige Backtick-Klammer um eine Rolle/ein Literal.

    Gueltige Auszeichnung wird zuerst ausmaskiert. Was an Backticks uebrig
    bleibt, gehoert zur Standardrolle (`x`) -- und wenn so ein Paar eine
    Rolle oder ein Literal *umschliesst*, ist genau das der Schaden.
    """
    maske = bytearray(len(text))
    spans = []
    for m in GUELTIG.finditer(text):
        spans.append((m.start(), m.end()))
        for i in range(m.start(), m.end()):
            maske[i] = 1
    lose = [i for i, z in enumerate(text) if z == '`' and not maske[i]]
    for a, b in zip(lose[0::2], lose[1::2]):
        for s, e in spans:
            if a < s and e <= b:
                return text[max(0, a - 30):min(len(text), b + 20)].replace("\n", " ")
    if len(lose) % 2:
        i = lose[-1]
        return text[max(0, i - 30):i + 25].replace("\n", " ")
    return ""


TYPOGRAFISCH = "„“”‚‘’"
VERWEIS = re.compile(r'`[^`]+`__?(?![\w`])')
LITERAL = re.compile(r'``([^`]+)``')
CODE_START = re.compile(r'^(>>>|\.\.\.|def |class |async def |import |from )')


def ist_code(msgid: str) -> bool:
    return "\n" in msgid and bool(CODE_START.match(msgid.lstrip()))


# --- PO-Parser (bewusst ohne polib, damit das Skript ueberall laeuft) ------

ENTKOMMEN = {"\\n": "\n", "\\t": "\t", "\\r": "\r", "\\\"": "\"", "\\\\": "\\"}


def entkomme(s: str) -> str:
    aus, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            paar = s[i:i + 2]
            if paar in ENTKOMMEN:
                aus.append(ENTKOMMEN[paar]); i += 2; continue
        aus.append(s[i]); i += 1
    return "".join(aus)


def po_eintraege(pfad: Path):
    """Liefert (po_zeile, quelle, msgid, msgstr) je Eintrag."""
    zeilen = pfad.read_text(encoding="utf-8", errors="replace").split("\n")
    i, n = 0, len(zeilen)
    while i < n:
        if not zeilen[i].startswith(("#", "msgid", "msgctxt")):
            i += 1
            continue
        if zeilen[i].startswith("#~"):           # obsolet
            i += 1
            continue
        quelle = ""
        while i < n and zeilen[i].startswith("#"):
            if zeilen[i].startswith("#:") and not quelle:
                quelle = zeilen[i][2:].strip().split()[0] if zeilen[i][2:].strip() else ""
            i += 1
        if i < n and zeilen[i].startswith("msgctxt"):
            i += 1
            while i < n and zeilen[i].startswith('"'):
                i += 1
        if i >= n or not zeilen[i].startswith("msgid"):
            i += 1
            continue
        po_zeile = i + 1

        def sammle(start, schluessel):
            teile, j = [], start
            m = re.match(schluessel + r'\s+"(.*)"\s*$', zeilen[j])
            if m:
                teile.append(m.group(1))
            j += 1
            while j < n and zeilen[j].startswith('"'):
                teile.append(zeilen[j].strip()[1:-1])
                j += 1
            return "".join(teile), j

        msgid, i = sammle(i, "msgid")
        if i < n and zeilen[i].startswith("msgid_plural"):
            _, i = sammle(i, "msgid_plural")
        if i >= n or not zeilen[i].startswith("msgstr"):
            continue
        msgstr, i = sammle(i, re.escape("msgstr") + r'(?:\[\d+\])?')
        if msgid and msgstr:
            yield po_zeile, quelle, entkomme(msgid), entkomme(msgstr)


# --- Pruefungen ------------------------------------------------------------

def pruefe_eintrag(msgid: str, msgstr: str, arten: set) -> list:
    """Liefert [(art, beschreibung, ausschnitt), ...]."""
    funde = []

    if "klammer" in arten and not ist_code(msgid):
        # In Codebloecken sind Backticks gewoehnlicher Text -- dort greift
        # stattdessen die Pruefung "code".
        schaden = lose_klammer(msgstr)
        if schaden and not lose_klammer(msgid):
            funde.append(("klammer", "Backtick-Klammer um Rolle/Literal", schaden))

    for art in ("klammer", "anzeige", "bindestrich"):
        if art not in arten:
            continue
        for rx, name in MUSTER[art]:
            tr = rx.search(msgstr)
            if tr and not rx.search(msgid):
                a = max(0, tr.start() - 35)
                funde.append((art, name, msgstr[a:tr.end() + 25].replace("\n", " ")))
                break

    if "verweis" in arten:
        a = len(VERWEIS.findall(msgid.replace("\n", " ")))
        b = len(VERWEIS.findall(msgstr.replace("\n", " ")))
        if a != b:
            funde.append(("verweis", "Benannte Verweise weichen ab",
                          f"Original {a}, Uebersetzung {b}"))

    if "literal" in arten:
        a = sorted(LITERAL.findall(msgid.replace("\n", " ")))
        b = sorted(LITERAL.findall(msgstr.replace("\n", " ")))
        # Nur *verlorene* Literale sind ein Fehler. Zusaetzliche Literale in
        # der Uebersetzung sind meist Absicht (z. B. ein Objekttyp, den das
        # Original als Flie\u00dftext fuehrt) und werden nicht gemeldet.
        fehlt = [x for x in a if x not in b]
        if fehlt:
            funde.append(("literal", "Literale fehlen in der Uebersetzung",
                          f"fehlt: {fehlt}"))

    if "code" in arten and ist_code(msgid):
        za, zb = msgid.split("\n"), msgstr.split("\n")
        if len(za) != len(zb):
            funde.append(("code", "Zeilenzahl weicht ab",
                          f"{len(za)} Zeilen im Original, {len(zb)} in der Uebersetzung"))
        else:
            for x, y in zip(za, zb):
                if x != y and "#" not in x:
                    funde.append(("code", "Code ausserhalb von Kommentaren geaendert",
                                  f"{x.strip()[:55]!r} -> {y.strip()[:55]!r}"))
                    break

    if "typo" in arten:
        verdaechtig = []
        if ist_code(msgid):
            verdaechtig = [(msgid, msgstr)]
        else:
            verdaechtig = [(" ".join(LITERAL.findall(msgid.replace("\n", " "))),
                            " ".join(LITERAL.findall(msgstr.replace("\n", " "))))]
        for quelle_t, ziel_t in verdaechtig:
            treffer = [z for z in TYPOGRAFISCH if z in ziel_t and z not in quelle_t]
            if treffer:
                funde.append(("typo", "Typografische Anfuehrungszeichen im Code",
                              f"{''.join(treffer)} in: {ziel_t[:60]}"))
                break

    return funde


# --- Hauptprogramm ---------------------------------------------------------

ALLE_ARTEN = ["klammer", "anzeige", "verweis", "code", "literal", "typo",
              "bindestrich"]

ERKLAERUNG = {
    "klammer": "Ueberfluessige Backtick-/Stern-Klammer um eine Rolle -- zerstoert die folgenden Querverweise",
    "anzeige": "Rolle ohne Anzeigetext -- der sichtbare Text fehlt",
    "verweis": "Benannte Hyperlink-Verweise (`Text`_) fehlen oder sind beschaedigt",
    "code": "Codeblock ausserhalb von Kommentarzeilen veraendert -- Beispiel ist nicht mehr lauffaehig",
    "literal": "``Literale`` aus dem Original fehlen in der Uebersetzung -- Code wurde mituebersetzt",
    "typo": "Typografische Anfuehrungszeichen innerhalb von Code oder Literalen",
    "bindestrich": "Leerzeichen zwischen Rolle und angehaengtem Wort",
}


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pfade", nargs="*", default=["."],
                   help="zu pruefende Verzeichnisse oder Dateien (Vorgabe: alles)")
    p.add_argument("--art", help="nur diese Fehlerarten, kommagetrennt: "
                                 + ", ".join(ALLE_ARTEN))
    p.add_argument("--exclude", default=",".join(AUSSCHLUSS),
                   help="Verzeichnisse auslassen (kommagetrennt)")
    p.add_argument("--max", type=int, default=20, metavar="N",
                   help="hoechstens N Beispiele je Fehlerart (0 = alle)")
    p.add_argument("--nur-zahlen", action="store_true", dest="nur_zahlen",
                   help="nur die Zusammenfassung ausgeben")
    p.add_argument("-o", "--ausgabe", metavar="DATEI",
                   help="Bericht zusaetzlich als Markdown schreiben")
    args = p.parse_args()

    arten = set(ALLE_ARTEN)
    if args.art:
        gewaehlt = {a.strip() for a in args.art.split(",") if a.strip()}
        unbekannt = gewaehlt - set(ALLE_ARTEN)
        if unbekannt:
            sys.exit(f"Unbekannte Fehlerart(en): {', '.join(sorted(unbekannt))}")
        arten = gewaehlt

    aus = [a.strip() for a in args.exclude.split(",") if a.strip()]

    dateien = []
    for roh in args.pfade:
        pfad = Path(roh)
        if pfad.is_file() and pfad.suffix == ".po":
            dateien.append(pfad)
        else:
            dateien.extend(sorted(pfad.rglob("*.po")))
    dateien = [d for d in dateien if not any(t in d.parts for t in aus)]
    if not dateien:
        sys.exit("Keine .po-Dateien gefunden.")

    print(f"{len(dateien)} Dateien werden geprueft ...", file=sys.stderr)

    funde = {a: [] for a in ALLE_ARTEN}
    betroffene_dateien = {a: set() for a in ALLE_ARTEN}
    for nr, datei in enumerate(dateien, 1):
        if nr % 100 == 0:
            print(f"  {nr}/{len(dateien)}", file=sys.stderr)
        try:
            for po_zeile, quelle, msgid, msgstr in po_eintraege(datei):
                for art, name, ausschnitt in pruefe_eintrag(msgid, msgstr, arten):
                    funde[art].append((str(datei), po_zeile, quelle, name, ausschnitt))
                    betroffene_dateien[art].add(str(datei))
        except Exception as fehler:                      # defekte Datei nicht verschlucken
            print(f"  !! {datei}: {fehler}", file=sys.stderr)

    zeilen = []
    gesamt = sum(len(v) for v in funde.values())

    zeilen.append("## Zusammenfassung\n")
    zeilen.append("| Fehlerart | Eintraege | Dateien | Bedeutung |")
    zeilen.append("|---|---:|---:|---|")
    for art in ALLE_ARTEN:
        if art not in arten:
            continue
        zeilen.append(f"| `{art}` | {len(funde[art])} | "
                      f"{len(betroffene_dateien[art])} | {ERKLAERUNG[art]} |")
    zeilen.append(f"| **gesamt** | **{gesamt}** | "
                  f"**{len(set().union(*betroffene_dateien.values()) if gesamt else set())}** | |")

    if not args.nur_zahlen:
        for art in ALLE_ARTEN:
            if art not in arten or not funde[art]:
                continue
            zeilen.append(f"\n## {art} -- {ERKLAERUNG[art]}\n")
            zeigen = funde[art] if args.max == 0 else funde[art][:args.max]
            for datei, po_zeile, quelle, name, ausschnitt in zeigen:
                zeilen.append(f"- `{datei}:{po_zeile}` ({quelle}) -- {name}")
                zeilen.append(f"  - `{ausschnitt}`")
            if len(funde[art]) > len(zeigen):
                zeilen.append(f"- ... und {len(funde[art]) - len(zeigen)} weitere "
                              f"(mit `--max 0` vollstaendig)")

    bericht = "\n".join(zeilen)
    print()
    print(bericht)

    if args.ausgabe:
        Path(args.ausgabe).write_text(
            "# Auszeichnungspruefung der PO-Dateien\n\n" + bericht + "\n",
            encoding="utf-8")
        print(f"\nBericht geschrieben: {args.ausgabe}", file=sys.stderr)

    sys.exit(1 if gesamt else 0)


if __name__ == "__main__":
    main()
