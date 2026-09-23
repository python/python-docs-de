# Übersetzungsregeln für python-docs-de

Dieses Repository enthält die deutsche Übersetzung der Python-Dokumentation
als Gettext-Dateien (`.po`). Übersetzt wird ausschließlich der `msgstr`.

## Sprache und Terminologie
- Durchgehend „Du"-Form, niemals „Sie"
- „Built-in" → „integriert"
- „dictionary" → „Dictionary" (nicht „Wörterbuch")
- „string" → „Zeichenkette" (nicht „String" oder „Zeichenfolge")
- „iterable" → „iterierbares Objekt"
- Funktionsbeschreibungen in der 3. Person: „Gibt … zurück"
- Deutsche Anführungszeichen „…", nie um Rollen oder Code herum

## reST- und PO-Syntax
- `msgid` NIEMALS ändern, auch nicht bei Tippfehlern im Original
- Rollen (`:func:`, `:class:`, `:ref:`, `:term:`, `:meth:`, `:exc:`)
  exakt übernehmen; Anzahl und Reihenfolge müssen msgid und msgstr
  entsprechen
- Bei `:term:` und `:ref:` mit deutschem Anzeigetext immer das Ziel
  angeben: `:term:`Sequenz <sequence>``
- Parameternamen zwischen Sternchen bleiben englisch: *maxsplit*
- Nach `` ` `` oder `*` nie direkt ein Buchstabe oder Bindestrich
  (kein `*m*s`, kein `:class:`X`-Instanz`)
- Vor einer Rolle immer ein Leerzeichen
- Code-Literale, Programmausgaben und `::` am Zeilenende unverändert
- `#, fuzzy` nach dem Übersetzen entfernen

## Prüfungen nach jedem Abschnitt
    powrap <datei>
    msgfmt --check -o /dev/null <datei>
    sphinx-lint <datei>
    python3 check_roles.py <datei>

Gemeldete Fehler beheben und die Prüfungen erneut ausführen –
höchstens drei Versuche. Bleiben danach Fehler bestehen: nicht
committen, sondern die betroffenen Einträge und die Fehlermeldungen
auflisten und auf Rückmeldung warten.
