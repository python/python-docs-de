#!/usr/bin/env python3
"""Ergaenzt fehlende Sprungziele in uebersetzten Sphinx-Rollen.

Hintergrund: Wer im Transifex-Editor uebersetzt, sieht nur den gerenderten
Text. Aus ":term:`bytecode`" wird dann ":term:`Bytecode`" -- der Verweis
zeigt ins Leere, weil das Glossar den englischen Begriff fuehrt. Richtig
waere ":term:`Bytecode <bytecode>`".

Dieses Skript holt das englische Ziel aus dem msgid und setzt es im msgstr
ein. Es aendert nur Faelle, in denen die Zuordnung eindeutig ist: genau eine
Rolle dieses Typs im msgid und genau eine im msgstr. Alles andere bleibt
unberuehrt und wird gemeldet.

Aufruf:
    python fix_roles.py reference/datamodel.po reference/expressions.po
    python fix_roles.py --dry-run reference/*.po
    python fix_roles.py --rollen term,ref reference/datamodel.po

Danach immer powrap ueber die geaenderten Dateien laufen lassen -- das
Skript schreibt msgstr einzeilig zurueck.
"""

import argparse
import re
import sys
from pathlib import Path

# Rollen, bei denen ein uebersetzter Anzeigetext zulaessig ist, sofern das
# Ziel in spitzen Klammern mitgegeben wird.
STANDARD_ROLLEN = ["term", "ref"]

# Ein Eintrag: msgid-Block gefolgt von msgstr-Block, beide ein- oder
# mehrzeilig. Vorangehende #-Kommentare bleiben unangetastet.
EINTRAG = re.compile(r'(?m)^msgid ((?:".*"\n)+)msgstr ((?:".*"\n)+)')

# Eine Rolle: :typ:`Text` oder :typ:`Text <ziel>`
ROLLE = re.compile(r':([a-z:+-]+):`([^`]*)`')


def zusammenfuegen(block: str) -> str:
    """PO-Mehrzeiler zu einer Zeichenkette verbinden (ohne Anfuehrungszeichen)."""
    return "".join(re.findall(r'"(.*)"', block))


def als_msgstr(text: str) -> str:
    """Zeichenkette als einzeiligen msgstr-Block ausgeben."""
    return f'msgstr "{text}"\n'


def ziel_von(inhalt: str) -> str:
    """Das Sprungziel einer Rolle: der Teil in <...>, sonst der Text selbst."""
    m = re.search(r'<([^<>]*)>\s*$', inhalt)
    return m.group(1) if m else inhalt.strip()


def hat_ziel(inhalt: str) -> bool:
    return re.search(r'<[^<>]*>\s*$', inhalt) is not None


def rollen_nach_typ(text: str, typ: str) -> list:
    return [m for m in ROLLE.finditer(text) if m.group(1) == typ]


def datei_bearbeiten(pfad: Path, rollen: list, probelauf: bool) -> tuple:
    text = pfad.read_text(encoding="utf-8")
    geaendert = []
    uebersprungen = []

    def ersetze(treffer):
        quelle = zusammenfuegen(treffer.group(1))
        ziel_text = zusammenfuegen(treffer.group(2))
        if not quelle or not ziel_text:
            return treffer.group(0)

        neu = ziel_text
        for typ in rollen:
            q = rollen_nach_typ(quelle, typ)
            z = rollen_nach_typ(neu, typ)
            if not z:
                continue
            offen = [m for m in z if not hat_ziel(m.group(2))]
            if not offen:
                continue
            if len(q) != 1 or len(z) != 1:
                uebersprungen.append(
                    (quelle[:60], typ, f"{len(q)} im msgid, {len(z)} im msgstr")
                )
                continue

            anzeige = offen[0].group(2).strip()
            sprungziel = ziel_von(q[0].group(2))
            if anzeige == sprungziel:
                continue  # unuebersetzt, loest korrekt auf
            if not anzeige:
                uebersprungen.append(
                    (quelle[:60], typ, "Anzeigetext ist leer -- von Hand pruefen")
                )
                continue
            if anzeige.startswith("-") or anzeige.endswith("-"):
                uebersprungen.append(
                    (quelle[:60], typ,
                     f"Anzeigetext '{anzeige}' faengt mit Bindestrich an oder hoert damit auf")
                )
                continue

            alt = offen[0].group(0)
            ersatz = f":{typ}:`{anzeige} <{sprungziel}>`"
            neu = neu.replace(alt, ersatz, 1)
            geaendert.append((typ, anzeige, sprungziel))

        if neu == ziel_text:
            return treffer.group(0)
        return "msgid " + treffer.group(1) + als_msgstr(neu)

    neuer_text = EINTRAG.sub(ersetze, text)

    if geaendert and not probelauf:
        pfad.write_text(neuer_text, encoding="utf-8")

    return geaendert, uebersprungen


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dateien", nargs="+", type=Path, help="zu pruefende .po-Dateien")
    p.add_argument("--dry-run", action="store_true",
                   help="nur anzeigen, nichts schreiben")
    p.add_argument("--rollen", default=",".join(STANDARD_ROLLEN),
                   help=f"Rollentypen, Komma-getrennt (Vorgabe: {','.join(STANDARD_ROLLEN)})")
    args = p.parse_args()

    rollen = [r.strip() for r in args.rollen.split(",") if r.strip()]
    summe = 0

    for pfad in args.dateien:
        if not pfad.is_file():
            print(f"!! nicht gefunden: {pfad}", file=sys.stderr)
            continue
        geaendert, uebersprungen = datei_bearbeiten(pfad, rollen, args.dry_run)
        if not geaendert and not uebersprungen:
            continue
        print(f"\n{pfad}")
        for typ, anzeige, sprungziel in geaendert:
            print(f"   :{typ}:`{anzeige}`  ->  :{typ}:`{anzeige} <{sprungziel}>`")
        for quelle, typ, grund in uebersprungen:
            print(f"   ubersprungen ({typ}, {grund}): {quelle}...")
        summe += len(geaendert)

    modus = "waeren zu aendern" if args.dry_run else "geaendert"
    print(f"\n{summe} Rollen {modus}.")
    if summe and not args.dry_run:
        print("Jetzt powrap ueber die geaenderten Dateien laufen lassen.")


if __name__ == "__main__":
    main()
