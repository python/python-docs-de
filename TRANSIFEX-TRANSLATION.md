# Übersetzen über Transifex – typische Fehler und wie du sie vermeidest

Der Transifex-Editor zeigt beim Übersetzen nur den sichtbaren Text. 
Die reST-Syntax dahinter bleibt unsichtbar – und genau dort entstehen fast 
alle Fehler, die wir beim Zurückholen ins Repository finden.

Dies ist eine Liste typischer Fehler bei den Testläufen. 
Wer sie kennt, produziert Übersetzungen, die ohne Nacharbeit 
übernommen werden können.

---

## 1. Verweisziel im Link  `:term:` und `:ref:` fehlt

**Falsch** `:term:`Bytecode`` · **Richtig** `` :term:`Bytecode <bytecode>` ``

Im Englischen ist der sichtbare Text zugleich der Verweis. Übersetzt du ihn
ohne spitze Klammern, zeigt der Verweis ins Leere. Der Teil vor der Klammer
wird angezeigt und darf übersetzt werden, der Teil in der Klammer ist der
englische Bezeichner und bleibt unverändert.

## 2. `:ref:`-Ziele niemals übersetzen

**Falsch** `:ref:`gebunden`` (aus `:ref:`method-binding``)

Ein `:ref:`-Ziel ist ein technischer Anker im Dokument, kein Text. Entweder du
lässt die Rolle unverändert oder du nutzt die Form aus Punkt 1:
`` :ref:`gebunden <method-binding>` ``

## 3. Keine Rolle weglassen

Jede Rolle aus dem Original muss in der Übersetzung wieder auftauchen. Baust
du den Satz um, verschiebt sich die Auszeichnung – verschwinden darf sie
nicht. Ebenso wenig darf eine Rolle leer bleiben: `` :ref:`` `` ist kaputt.

## 4. Konsequente Du-Form

Deutsche Übersetzungen durchgängig im informellen „Du", nie im „Sie".
Funktionsbeschreibungen in der dritten Person: „Gibt … zurück", nicht
„Geben Sie … zurück".

## 5. reST-Fallen

- Kein Buchstabe und kein Bindestrich direkt **nach** einem schließenden
  `` ` `` oder `*` – `` `Text`s `` bricht. Notfalls mit `` \ `` trennen.
- Kein Leerzeichen direkt vor einem schließenden Backtick.
- Maskierte Zeichen wie `\*` unverändert übernehmen.
- Platzhalter wie `%s`, `%(release)s`, `{0}` und HTML bleiben
  exakt stehen.
- Benannte Verweise der Form `` `Text`_ `` unverändert lassen.

## 6. Formatierung

- Keine doppelten Leerzeichen, besonders nicht rund um Rollen.
- Kein Leerzeichen vor Komma oder Punkt.

---

## Vor dem Commit ins Repository

Für jede aus Transifex geholte Datei:

```
python fix_roles.py --dry-run <datei>.po   # zeigt fehlende Sprungziele
python fix_roles.py <datei>.po             # setzt die eindeutigen Fälle
powrap <datei>.po                          # Zeilenumbrüche bei 80 Zeichen
msgfmt --check -o /dev/null <datei>.po     # Syntax
sphinx-lint <datei>.po                     # reST
python check_roles.py <datei>.po           # Rollen gegen msgid
```

`fix_roles.py` erledigt die Fälle aus Punkt 1 automatisch, sofern die
Zuordnung eindeutig ist. Alles andere meldet es und bleibt für dich liegen.

## Dateikopf

Aus Transifex geladene Dateien bringen ein `#, fuzzy` im Kopfblock mit. Das
muss weg, sonst werten `potodo` und die CI-Prüfungen die Datei als
unvollständig. Der Kopf sieht so aus:

```
# German translation of the Python documentation.
# Copyright (C) 2001 Python Software Foundation
# This file is distributed under the same license as the Python package.
#
# Translators:
# <Name oder Transifex>, <Jahr>
#
msgid ""
msgstr ""
"Project-Id-Version: Python 3.14\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: <aus der Datei übernehmen>\n"
"PO-Revision-Date: <Zeitpunkt der Bearbeitung>\n"
"Last-Translator: <Name oder Transifex>\n"
"Language-Team: German (https://github.com/python/python-docs-de)\n"
"Language: de\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
```

Die Zeilen `msgid ""` und `msgstr ""` gehören zwingend dazu – fehlen sie,
bricht `msgcat` mit einem Syntaxfehler ab. Und es darf genau **einen** solchen
Kopfblock pro Datei geben; das PyCharm-Gettext-Plugin hat schon mehrfach
weitere ans Dateiende angehängt.
