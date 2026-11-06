# Glossar der deutschen Python-Dokumentation

Diese Liste hält fest, wie wiederkehrende Fachbegriffe im Deutschen heißen.
Sie richtet sich an alle, die an der Übersetzung mitarbeiten – egal ob über
GitHub oder über Transifex.

Die Regeln zur reST-Auszeichnung, zu Codeblöcken und zum Prüfablauf stehen
nicht hier, sondern in [AI-SKILLS.md](AI-SKILLS.md).

## Was im Zweifel entscheidet

1. **`glossary.po`.** Wer einen Begriff übersetzt, der im Python-Glossar
   ein eigenes Stichwort hat, nimmt die dortige Fassung. Das Glossar ist
   die veröffentlichte Begriffsliste, auf die Leser verwiesen werden.
2. **Dieses Glossar.** Für alles, was im Python-Glossar nicht vorkommt.
3. **Der Bestand im Repo.** Gibt es weder dort noch hier eine Festlegung,
   lohnt ein Blick darauf, wie der Begriff schon übersetzt wurde. Ein
   `grep` über die `.po`-Dateien beantwortet das meist in einer Minute.
4. **Neu entscheiden.** Dann aber bitte die Entscheidung hier eintragen,
   damit die nächste Person nicht wieder von vorn anfängt.

Ein eigener Begriff lässt sich **nicht** in `glossary.po` ergänzen: Jeder
Eintrag dort hängt an einem `msgid` aus `Doc/glossary.rst` in CPython.
Soll ein Begriff wirklich ins veröffentlichte Glossar, führt der Weg über
einen Pull Request gegen CPython; beim nächsten Sync steht er dann allen
Sprachen zur Verfügung.

## Grundhaltung

- Durchgehend **Du**-Form, niemals „Sie".
- Funktionsbeschreibungen in der 3. Person: „Gibt … zurück", nicht
  „Gib … zurück".
- Kapitelüberschriften der Form „… Services" werden zu „Dienste …":
  „Dienste der Python-Laufzeitumgebung", „Dienste zur Textverarbeitung",
  „Dienste für die Python-Sprache".
- Lieber ein etabliertes Lehnwort als eine selbstgebaute Eindeutschung.
  Ein Begriff muss nachschlagbar bleiben: Wer „Factory-Funktion" liest,
  findet beim Suchen etwas, wer „Fabrikfunktion" liest, nicht.

## Zeichensetzung

Das englische Original setzt Zeichen anders als das Deutsche. Drei Stellen,
an denen fast jede Übersetzung zuerst stolpert:

- **Semikolon.** Verbindet das Original zwei vollständige Hauptsätze mit
  einem Semikolon, wird daraus im Deutschen ein Punkt mit Großschreibung –
  oder ein Komma, wenn der Satz es trägt. Das Semikolon bleibt nur dort, wo
  es gleichrangige Glieder einer Aufzählung trennt, etwa parallele
  „dass"-Sätze. Aus „Specifies that exactly *m* copies of the previous RE
  should be matched; fewer matches cause the entire RE not to match." wird
  also „Gibt an, dass genau *m* Kopien des vorangehenden RE passen sollen.
  Bei weniger Wiederholungen passt der gesamte RE nicht."
- **Anführungszeichen.** Deutsch „…", nie um eine Rolle oder um Code herum.
- **Satzabstand.** Ein Leerzeichen nach dem Punkt, nicht zwei – das Original
  setzt oft zwei.
- **„passen auf" braucht ein Subjekt.** Das englische „to match" steht oft
  im Passiv oder als Veranlassung; im Deutschen wird daraus beides ungelenk.
  Kein „wobei auf so viele Wiederholungen wie möglich gepasst wird" und kein
  „Lässt den entstehenden RE auf … passen", wo der Satz ein Subjekt haben
  kann: „Der entstehende RE passt auf …, und zwar auf so viele wie möglich."
  Häuft sich „passen" in einem Eintrag, hilft nicht ein anderes Wort für
  „match" – „erfassen" ist für *capture* vergeben, „finden" für *search* –,
  sondern eine andere Satzform: „Voreingestellt sind das alle Zeichen außer
  …", „deckt … ab", „ergibt eine Fundstelle". Die Veranlassung bleibt richtig,
  wo ein Flag das Verhalten setzt: „Lässt ``\w`` nur auf ASCII passen."

Wer mit dem Repo arbeitet, prüft eine Datei mit

    python3 _tools/check_satzzeichen.py <datei>

und behebt die Funde mit `--fix`. Wer über Transifex übersetzt und das Repo
nicht hat, findet die Semikolon-Stellen auch mit
`grep -n '; [a-zäöüß]' <datei>`; Treffer im PO-Kopf (`Content-Type:
text/plain; charset=UTF-8`, `Plural-Forms`) und in wörtlich übernommenen
Codeblöcken sind dabei Falschmeldungen.

## Begriffe

| Englisch | Deutsch | Anmerkung |
|---|---|---|
| archive member | Archiveintrag | nicht „Archivmitglied" |
| auditing event | Auditing-Ereignis | „audit event" im Fließtext ohne Rolle → „Audit-Ereignis" |
| broadcast address | Broadcast-Adresse | |
| built-in | integriert | nicht „eingebaut" |
| canvas | Zeichenfläche | |
| central directory | zentrales Verzeichnis | ZIP-Fachbegriff |
| code object | Code-Objekt | mit Bindestrich, nicht „Codeobjekt" |
| comprehension | Comprehension | nie „Kompression" oder „Abstraktion" |
| convenience function | Hilfsfunktion | |
| decompression bomb | Entpackbombe | „ZIP bomb" bleibt als benannter Verweis englisch |
| decorator | Dekorator | nicht „Decorator", erst recht nicht „Dekorateur" |
| dictionary | Dictionary | Plural „Dictionarys"; „dictionary view" → „Dictionary-View" |
| display (list/set/dict) | Display | nicht „Anzeige"; „Wörterbuch-Display" |
| event loop | Ereignisschleife | |
| exploded / compressed (IP) | ausgeschrieben / verkürzt | |
| factory function | Factory-Funktion | „factory" allein → „Factory", Plural „Factorys" |
| font | Schriftart | nicht „Schrift" |
| free-threaded build | Build mit freien Threads | laut Glossar |
| host mask | Hostmaske | |
| iterable | Iterable | nicht „iterierbares Objekt" |
| lazy import | verzögerter Import | |
| look and feel | Aussehen und Verhalten | |
| main window | Hauptfenster | |
| to match | passen auf | siehe „Zeichensetzung" zur Satzform |
| a match | Fundstelle | das Ergebnis, nicht der Vorgang |
| match object | Match-Objekt | |
| namespace package | Namespace-Paket | nicht „Namensraum-Paket" |
| net mask | Netzmaske | |
| numeric tower | numerischer Turm | |
| octet | Oktett | |
| path traversal | Pfadwechsel | |
| to pickle | serialisieren | nie „picklen"; das Substantiv „Pickle" bleibt (Pickle-Datei, Pickle-Funktion) |
| prefix / prefix length | Präfix / Präfixlänge | |
| probe point | Probepoint | DTrace/SystemTap |
| root window | Root-Fenster | nicht „Wurzelfenster" |
| scope zone ID | Scope-Zone-ID | |
| seekable | positionierbar | |
| soft keyword | weiches Schlüsselwort | |
| string | Zeichenkette | siehe „Offene Punkte" |
| subnet / supernet | Subnetz / Supernetz | |
| subscription expression | Indexausdruck | nicht „Abonnementausdruck" |
| themed widgets | Widgets mit Themes | |
| thread state | Thread-Zustand | nicht „Thread-Status"; „attached" dazu → „angehängt" |
| toplevel window | Toplevel-Fenster | |
| universal newlines | universelle Zeilenumbrüche | |
| unraisable exception | nicht weiterleitbare Ausnahme | beim ersten Vorkommen mit englischem Begriff in Klammern, danach kurz |
| wrapper | Hülle | |

### Kind-

„child" bleibt als Stamm „Kind-", steht aber nie allein. Immer als
Kompositum mit dem gemeinten Ding: „Kindeintrag" (Treeview),
„Kind-Widget" (Widget-Hierarchie), „Kind-Logger" (Logger-Hierarchie),
„Kindknoten" (abstrakter Baum). Das nackte „Kinder" und „Kinderliste"
sind falsch. Bestehende Komposita wie Kindprozess, Kindklasse und
Kindfenster bleiben.

## Begriffe, die englisch bleiben

Widget, Frame, Toplevel, Callback, Scrollbar, Tag, Mixin, Theme, Turtle,
Boilerplate, Loopback, Multicast, Big-Endian.

Dazu immer: Funktions-, Klassen-, Methoden- und Parameternamen, Typnamen
aus C, Schlüsselwörter und alles, was in ``doppelten Backticks`` steht.

## Zwei Dinge, die beide „Template" heißen

Das ist die häufigste Verwechslung in diesem Projekt, und sie betrifft
zwei verschiedene Sprachmerkmale:

- **`string.Template` mit `$`-Ersetzung** (seit Python 2.4) →
  **Vorlage-Zeichenkette**, die Überschrift lautet
  „Vorlage-Zeichenketten ($-Zeichenketten)".
- **t-Strings aus PEP 750** (seit Python 3.14) →
  **Template-String-Literal**, kurz **t-String**. Das Modul heißt
  „Unterstützung für Template-String-Literale".

Beide Begriffe nebeneinander stehen zu lassen ist Absicht: Zwei
verschiedene Dinge brauchen zwei verschiedene Namen. Wer hier
vereinheitlicht, macht die Dokumentation unverständlich.

## Offene Punkte

Diese Fragen sind noch nicht entschieden. Wer darauf stößt, möge die
vorhandene Schreibweise der Datei beibehalten und hier Bescheid geben,
statt im Alleingang umzustellen.

**„string" → „Zeichenkette" oder „String"?** Die Regel oben sagt
„Zeichenkette", der Bestand sagt etwas anderes: Allein in
`builtins/stdtypes.po` stehen 194 Fundstellen „String" gegen 24
„Zeichenkette". Die Angleichung wäre ein eigener Durchgang über mehrere
große Dateien. Bis dahin gilt: In einer Datei durchhalten, was dort schon
steht.

**Qualifizierte Comprehension-Formen.** Im Repo stehen 38 Fundstellen in
18 Schreibweisen; allein „list comprehension" kommt in sieben Varianten
vor. Das Glossar schreibt „List Comprehension", „Dictionary Comprehension"
und „Set Comprehension" – also englisch mit Leerzeichen –, das wäre die
Zielform. Betroffen sind neun Dateien, darunter `builtins/stdtypes.po`,
`glossary.po`, `howto/functional.po` und `reference/expressions.po`. Das
unqualifizierte „Comprehension" ist überall einheitlich und nicht
betroffen.
