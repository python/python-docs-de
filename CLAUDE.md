# Übersetzungsregeln für python-docs-de

Dieses Repository enthält die deutsche Übersetzung der Python-Dokumentation
als Gettext-Dateien (`.po`). Übersetzt wird ausschließlich der `msgstr`.

## Sprache und Terminologie
- Durchgehend „Du"-Form, niemals „Sie"
- Funktionsbeschreibungen in der 3. Person: „Gibt … zurück"
- Bei Fachbegriffen ist `glossary.po` maßgeblich. Im Zweifel dort
  nachschlagen, bevor ein Begriff neu übersetzt wird
- „Built-in" → „integriert" (nicht „eingebaut")
- „dictionary" → „Dictionary", „dictionary comprehension" →
  „Dictionary Comprehension", „dictionary view" → „Dictionary-View",
  „list comprehension" → „List Comprehension". So lauten die
  Glossar-Stichwörter, und das Glossar entscheidet
- „string" → „Zeichenkette" (nicht „String" oder „Zeichenfolge")
- „iterable" → „Iterable" (im Repo 66 zu 42 gegenüber „iterierbares Objekt")
- „comprehension" → „Comprehension", nie „Kompression" oder „Abstraktion"
- „display" (list/set/dict display) → „Display", nicht „Anzeige". Dafür
  gibt es kein Glossar-Stichwort; die Wortbildung lautet
  „Wörterbuch-Display" (13 Fundstellen gegen keine andere Variante)
- „decorator" → „Decorator" (nicht „Dekorateur")
- „font" → „Schriftart", nicht „Schrift"
- „root window" → „Root-Fenster", „toplevel window" → „Toplevel-Fenster",
  „main window" → „Hauptfenster"
- „event loop" → „Ereignisschleife"
- „canvas" → „Zeichenfläche"
- „namespace package" → „Namespace-Paket"
- „thread state" → „Thread-Zustand", „attached" dazu → „angehängt"
- „lazy import" → „verzögerter Import"
- „subscription expression" → „Indexausdruck"
- „universal newlines" → „universelle Zeilenumbrüche"
- „unraisable exception" → „nicht weiterleitbare Ausnahme
  (unraisable exception)" beim ersten Vorkommen, danach kurz
- „free-threaded build" → „Build mit freien Threads" (laut Glossar)
- „look and feel" → „Aussehen und Verhalten"
- „themed widgets" → „Widgets mit Themes"
- „wrapper" → „Hülle", „convenience function" → „Hilfsfunktion"
- „factory function" → „Factory-Funktion", „factory" allein → „Factory".
  Nicht „Fabrikfunktion": zwar die Ableitung von „Fabrikmethode" aus der
  deutschen Muster-Literatur, klingt aber gestelzt und ist nicht
  nachschlagbar. Plural „Factorys" wie „Dictionarys" (Duden-Linie für
  englische Lehnwörter auf -y)
- Englisch bleiben im tkinter-Bestand: Widget, Frame, Toplevel, Callback,
  Scrollbar, Tag, Mixin, Theme

Offen und größer als es aussieht: die Schreibweise der *qualifizierten*
Comprehension-Formen. Im Repo stehen dafür 38 Fundstellen in 18
verschiedenen Schreibweisen. Allein „list comprehension" kommt in sieben
Varianten vor — „Listen-Comprehension", „Listen-Comprehensions",
„List Comprehension", „List Comprehensions", „List-Comprehension",
„List-Comprehensions" und „Listenkomprimierung". Das Glossar schreibt
„List Comprehension", „Dictionary Comprehension" und „Set Comprehension",
also englisch mit Leerzeichen; danach wäre das die Zielform. Vor dem
Angleichen entscheiden, dann in einem Durchgang über alle neun betroffenen
Dateien (builtins/stdtypes, glossary, howto/functional, reference/expressions,
tutorial/classes, tutorial/datastructures, whatsnew/3.15 und zwei weitere).
Das bloße Wort „Comprehension" ohne Qualifikation ist überall einheitlich
und nicht betroffen.

## Zeichensetzung
- Deutsche Anführungszeichen „…", nie um Rollen oder Code herum
- Kein Semikolon mit kleingeschriebener Fortsetzung. Stattdessen Komma,
  wenn der Satz es trägt, sonst Punkt und Großschreibung — auch dann,
  wenn das englische Original ein Semikolon setzt
- Ein Leerzeichen nach dem Satzende, nicht zwei (das Original setzt oft zwei)
- Kein verwaistes schließendes Anführungszeichen am Satzende
- Tippfehler im englischen Original werden im `msgstr` korrigiert, nicht
  nachgebildet. Für Code-Literale gilt das Gegenteil: buchstabengetreu

## reST- und PO-Syntax
- `msgid` NIEMALS ändern, auch nicht bei Tippfehlern im Original. Eine
  unquotierte Zeile im `msgid` lässt `msgmerge` mit „missing 'msgstr'
  section" abbrechen und blockiert damit die ganze CI
- Rollen (`:func:`, `:class:`, `:ref:`, `:term:`, `:meth:`, `:exc:`)
  exakt übernehmen; Anzahl und Reihenfolge müssen msgid und msgstr
  entsprechen
- Bei `:term:` und `:ref:` mit deutschem Anzeigetext immer das Ziel
  angeben: `:term:`Sequenz <sequence>``. Der Bezeichner in spitzen
  Klammern bleibt zwingend englisch
- `:dfn:` ist kein Querverweis — der Text wird übersetzt, ein Ziel ist
  weder nötig noch erlaubt
- Keine zusätzliche Backtick- oder Stern-Klammer um eine Rolle:
  `` ` :class:`tuple` ` `` ist falsch. Sphinx paart Backticks von links
  nach rechts, dadurch zerfallen alle folgenden Verweise im selben Absatz
- Nach dem schließenden Backtick einer Rolle kein Leerzeichen vor einem
  angehängten Wort: `` :exc:`GeneratorExit`-Ausnahme ``, nicht
  `` :exc:`GeneratorExit` -Ausnahme ``. Ein Bindestrich direkt am
  schließenden Backtick ist erlaubt, ein Buchstabe nicht
- Vor einer Rolle immer ein Leerzeichen
- Parameternamen zwischen Sternchen bleiben englisch: *maxsplit*
- Code-Literale, Programmausgaben und `::` am Zeilenende unverändert.
  ``Literale`` aus dem Original bleiben erhalten und werden nicht durch
  deutsche Anführungszeichen ersetzt
- Codeblöcke bleiben buchstabengetreu; übersetzt werden höchstens die
  Kommentarzeilen. Nie übersetzt werden Schlüsselwörter,
  Interpreter-Ausgaben und String-Literale, auf die sich eine Ausgabe bezieht
- Platzhalter wie `%s`, `{0}` oder `<TRANSLATION_REPO_>` bleiben unverändert
- `#, fuzzy` nach dem Übersetzen entfernen

## Zwei Fallen, die den Build mit `-W` abbrechen
- **Seitentitel.** Die erste Überschrift eines LaTeX-Wurzeldokuments darf
  nicht mit Auszeichnung beginnen — nicht mit ``Literal``, nicht mit einer
  Rolle, nicht mit *kursiv*. Falsch ist `` ``optparse``-Code nach
  ``argparse`` migrieren ``, richtig `` Migration von ``optparse``-Code zu
  ``argparse`` ``. Betroffen sind alle `howto/*.po` außer `index.po`,
  `whatsnew/3.x.po` und die Wurzeldokumente (about, bugs, contents,
  glossary, `*/index.po`). CPython baut aus jedem davon ein eigenes
  LaTeX-Dokument, dessen erste Überschrift zum `\title{}` wird; Sphinx
  verlangt dort einen reinen Textknoten und warnt sonst „document title is
  not a single Text node". Im Fließtext und in Zwischenüberschriften ist
  Auszeichnung am Anfang unbedenklich. `check_markup.py` prüft das als
  Fehlerart `titel`
- **Benannte Verweise auf eigene Überschriften.** `` `Tab Options`_ ``
  zielt auf das implizite Ziel der Überschrift „Tab options", und Sphinx
  bildet dieses Ziel aus dem *übersetzten* Text. Überschrift und Verweis
  müssen deshalb gemeinsam und zeichengenau gleich übersetzt werden, sonst
  bricht der Build mit „Unknown target name" ab. In `library/tkinter.ttk.po`
  betrifft das sechs Paare. Benannte Verweise mit eigener URL
  (`` `Titel <https://…>`_ ``) sind davon nicht betroffen, ihr Anzeigetext
  ist frei übersetzbar. Benannte Verweise ohne URL und ohne eigene
  Überschrift im Dokument (`` `complex arrays`_ ``) bleiben unübersetzt

## Prüfungen nach jedem Abschnitt
Am einfachsten über das Skript, das genau diese Kette abbildet:

    ./pre_push_check.sh

Stufe 1 sind fünf Schritte: `powrap -m`, `msgfmt --check --check-format`,
`sphinx-lint`, `check_roles.py` und `tools/check_markup.py` mit acht
Fehlerarten (klammer, anzeige, verweis, code, literal, typo, bindestrich,
titel). Einzeln für eine Datei:

    msgfmt --check --check-format -o /dev/null <datei>
    sphinx-lint <datei>
    python3 tools/check_markup.py <datei>

`powrap` nur mit `-m` auf geänderte Dateien anwenden. Auf eine Datei, die
vorher nicht powrap-sauber war, erzeugt es hunderte Zeilen Fremddiff. Die CI
formatiert nach jedem Push ohnehin selbst nach.

Achtung, Stufe 1 deckt den LaTeX-Teil der CI nicht ab: `pre_push_check.sh`
baut nur `html`, der Workflow `test-build.yml` baut `html` **und** `latex`,
beides mit `-W`. Die Titelregel oben ist genau die Fehlerklasse, die lokal
grün ist und erst in der CI auffliegt.

Gemeldete Fehler beheben und die Prüfungen erneut ausführen – höchstens
drei Versuche. Bleiben danach Fehler bestehen: nicht committen, sondern die
betroffenen Einträge und die Fehlermeldungen auflisten und auf Rückmeldung
warten.

## Arbeitsweise
- Keine Git-Schreibbefehle in diesem Repository. Committen, Branch-Wechsel
  und Pushen macht Swen selbst über PyCharm
- Keine neuen Skripte im Repository anlegen, ohne vorher zu fragen
- Vor einer Korrektur erst zeigen, was geändert werden soll — mit Datei und
  Zeilennummer, nicht als Umschreibung
- Dateien unter `.github/workflows/` sind über die Gerätebrücke nicht
  schreibbar; solche Änderungen gehen als fertige Datei in den Chat
