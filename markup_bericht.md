# Auszeichnungspruefung der PO-Dateien

## Zusammenfassung

| Fehlerart | Eintraege | Dateien | Bedeutung |
|---|---:|---:|---|
| `klammer` | 20 | 4 | Ueberfluessige Backtick-/Stern-Klammer um eine Rolle -- zerstoert die folgenden Querverweise |
| `anzeige` | 0 | 0 | Rolle ohne Anzeigetext -- der sichtbare Text fehlt |
| `code` | 89 | 16 | Codeblock ausserhalb von Kommentarzeilen veraendert -- Beispiel ist nicht mehr lauffaehig |
| `literal` | 25 | 9 | ``Literale`` aus dem Original fehlen in der Uebersetzung -- Code wurde mituebersetzt |
| `typo` | 12 | 1 | Typografische Anfuehrungszeichen innerhalb von Code oder Literalen |
| `bindestrich` | 19 | 5 | Leerzeichen zwischen Rolle und angehaengtem Wort |
| **gesamt** | **165** | **20** | |

## klammer -- Ueberfluessige Backtick-/Stern-Klammer um eine Rolle -- zerstoert die folgenden Querverweise

- `builtins/functions.po:2616` (../../builtins/functions.rst:1347) -- Stern vor Rolle
  - `von :class:`object` besitzen *keine* :attr:`~object.__dict__`-Attribu`
- `c-api/arg.po:270` (../../c-api/arg.rst:114) -- Backtick-Klammer um Rolle/Literal
  - `Ähnlich wie bei ` ``s```, allerdings kann d`
- `c-api/arg.po:285` (../../c-api/arg.rst:118) -- Backtick-Klammer um Rolle/Literal
  - `Ähnlich wie bei ` ``s*```, wobei das Python-`
- `c-api/arg.po:302` (../../c-api/arg.rst:122) -- Backtick-Klammer um Rolle/Literal
  - `Ähnlich wie bei ` ``s#```, allerdings kann d`
- `c-api/arg.po:341` (../../c-api/arg.rst:137) -- Backtick-Klammer um Rolle/Literal
  - `Diese Variante von ` ``s*`` ` akzeptiert keine U`
- `c-api/arg.po:358` (../../c-api/arg.rst:142) -- Backtick-Klammer um Rolle/Literal
  - `Diese Variante von ` ``s#`` ` akzeptiert keine U`
- `c-api/arg.po:435` (../../c-api/arg.rst:167) -- Backtick-Klammer um Rolle/Literal
  - `Diese Variante von ` ``s`` ` dient dazu, Unicod`
- `c-api/arg.po:463` (../../c-api/arg.rst:178) -- Backtick-Klammer um Rolle/Literal
  - `h der Verwendung die Funktion ` :c:func:`PyMem_Free` ` aufzurufen, um den`
- `c-api/arg.po:1531` (../../c-api/arg.rst:660) -- Backtick-Klammer um Rolle/Literal
  - `er auf den Unicode-Puffer auf ` ``NULL``` verweist, wird die`
- `c-api/arg.po:1576` (../../c-api/arg.rst:683) -- Backtick-Klammer um Rolle/Literal
  - `vertiert ein C-Objekt vom Typ `c:c:expr:`unsigned char``
- `c-api/arg.po:1582` (../../c-api/arg.rst:686) -- Backtick-Klammer um Rolle/Literal
  - `vertiert ein C-Objekt vom Typ `c:c:expr:`unsigned short`
- `c-api/arg.po:1588` (../../c-api/arg.rst:689) -- Backtick-Klammer um Rolle/Literal
  - `vertiert ein C-Objekt vom Typ `c:c:expr:`unsigned int` `
- `c-api/arg.po:1594` (../../c-api/arg.rst:692) -- Backtick-Klammer um Rolle/Literal
  - `vertiert ein C-Objekt vom Typ `c:c:expr:`unsigned long``
- `c-api/arg.po:1675` (../../c-api/arg.rst:734) -- Backtick-Klammer um Rolle/Literal
  - `hme ausgelöst hat. Daher gibt ` :c:func:`Py_BuildValue` ` ` ``NULL`` ` zurüc`
- `library/csv.po:105` (../../library/csv.rst:56) -- Backtick-Klammer um Rolle/Literal
  - `newline=''`` geöffnet werden. ` [1]_ Ein optionaler *di`
- `library/csv.po:396` (../../library/csv.rst:220) -- Backtick-Klammer um Rolle/Literal
  - `zugrunde liegende Instanz von ` :class:`writer` ` übergeben.`
- `library/csv.po:704` (../../library/csv.rst:391) -- Stern vor Rolle
  - `Weist Objekte von * :class:`writer` an, Felder niemal`
- `library/csv.po:887` (../../library/csv.rst:487) -- Backtick-Klammer um Rolle/Literal
  - `ndardmäßig ist dies ``'\r\n'```.`
- `tutorial/datastructures.po:223` (../../tutorial/datastructures.rst:139) -- Backtick-Klammer um Rolle/Literal
  - `s Stapels abzurufen, verwende ` :meth:`~list.pop` ` ohne expliziten In`
- `tutorial/datastructures.po:1271` (../../tutorial/datastructures.rst:601) -- Backtick-Klammer um Rolle/Literal
  - `Der Konstruktor ` :func:`dict` ` erstellt Wörterbüc`

## code -- Codeblock ausserhalb von Kommentarzeilen veraendert -- Beispiel ist nicht mehr lauffaehig

- `builtins/functions.po:2971` (../../builtins/functions.rst:1511) -- Code ausserhalb von Kommentaren geaendert
  - `"...     print('This will be written to somedir/spamspam" -> "...     print('Das wird geschrieben in somedir/spamspam"`
- `builtins/functions.po:3299` (../../builtins/functions.rst:1674) -- Code ausserhalb von Kommentaren geaendert
  - `'x = property(getx, setx, delx, "I\'m the \'x\' property.")' -> 'x = property(getx, setx, delx, "Ich bin die \'x\' Eigensc'`
- `builtins/functions.po:3351` (../../builtins/functions.rst:1696) -- Code ausserhalb von Kommentaren geaendert
  - `'"""Get the current voltage."""' -> '"""Hole die aktuelle Spannung."""'`
- `builtins/functions.po:3394` (../../builtins/functions.rst:1718) -- Code ausserhalb von Kommentaren geaendert
  - `'"""I\'m the \'x\' property."""' -> '"""Ich bin die \'x\' Eigenschaft."""'`
- `faq/windows.po:122` (../../faq/windows.rst:77) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> print("Hello")' -> '>>> print("Moin")'`
- `glossary.po:4313` (../../glossary.rst:1704) -- Code ausserhalb von Kommentaren geaendert
  - `'class C:' -> 'Klasse C:'`
- `library/csv.po:435` (../../library/csv.rst:242) -- Code ausserhalb von Kommentaren geaendert
  - `"fieldnames = ['first_name', 'last_name']" -> "fieldnames = ['Vorname', 'Nachname']"`
- `library/csv.po:502` (../../library/csv.rst:275) -- Code ausserhalb von Kommentaren geaendert
  - `'import csv' -> 'csv importieren'`
- `library/csv.po:1101` (../../library/csv.rst:625) -- Code ausserhalb von Kommentaren geaendert
  - `'import csv' -> 'csv importieren'`
- `library/csv.po:1119` (../../library/csv.rst:633) -- Code ausserhalb von Kommentaren geaendert
  - `'import csv' -> 'csv importieren'`
- `library/csv.po:1137` (../../library/csv.rst:641) -- Code ausserhalb von Kommentaren geaendert
  - `'import csv' -> 'csv importieren'`
- `library/csv.po:1160` (../../library/csv.rst:650) -- Code ausserhalb von Kommentaren geaendert
  - `'import csv' -> 'csv importieren'`
- `library/csv.po:1207` (../../library/csv.rst:668) -- Code ausserhalb von Kommentaren geaendert
  - `"sys.exit(f'file {filename}, line {reader.line_num}: {e}" -> "sys.exit(f'Datei {filename}, Zeile {reader.line_num}: {"`
- `library/string.po:1315` (../../library/string.rst:674) -- Code ausserhalb von Kommentaren geaendert
  - `">>> '{0}, {1}, {2}'.format('a', 'b', 'c')" -> '">>> \'{0}, {1}, {2}\'.format(\'a\', \'b\', \'c\')'`
- `library/string.po:1345` (../../library/string.rst:687) -- Code ausserhalb von Kommentaren geaendert
  - `"'Coordinates: 37.24N, -115.81W'" -> '"\'Coordinates: 37.24N, -115.81W\''`
- `library/string.po:1365` (../../library/string.rst:695) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> c = 3-5j' -> '">>> c = 3-5j'`
- `library/string.po:1413` (../../library/string.rst:716) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> "repr() shows quotes: {!r}; str() doesn\'t: {!s}".fo' -> '>>> "repr() zeigt Anführungszeichen: {!r}; str() nicht:'`
- `library/string.po:1427` (../../library/string.rst:721) -- Code ausserhalb von Kommentaren geaendert
  - `">>> '{:<30}'.format('left aligned')" -> ">>> '{:<30}'.format('linksbündig')"`
- `library/string.po:1478` (../../library/string.rst:741) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}"' -> '>>> \\"int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}'`
- `library/turtle.po:2084` (../../library/turtle.rst:1136) -- Zeilenzahl weicht ab
  - `6 Zeilen im Original, 3 in der Uebersetzung`
- `tutorial/classes.po:416` (../../tutorial/classes.rst:168) -- Code ausserhalb von Kommentaren geaendert
  - `'global spam' -> 'global spam"'`
- `tutorial/classes.po:1822` (../../tutorial/classes.rst:831) -- Code ausserhalb von Kommentaren geaendert
  - `'"""Iterator for looping over a sequence backwards."""' -> '"""Iterator zum Durchlaufen einer Sequenz in umgekehrte'`
- `tutorial/classes.po:1991` (../../tutorial/classes.rst:916) -- Zeilenzahl weicht ab
  - `20 Zeilen im Original, 15 in der Uebersetzung`
- `tutorial/controlflow.po:48` (../../tutorial/controlflow.rst:19) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> x = int(input("Please enter an integer: "))' -> 'x = int(input("Bitte gib eine ganzzahlige Zahl ein: "))'`
- `tutorial/controlflow.po:392` (../../tutorial/controlflow.rst:183) -- Zeilenzahl weicht ab
  - `14 Zeilen im Original, 10 in der Uebersetzung`
- `tutorial/controlflow.po:474` (../../tutorial/controlflow.rst:221) -- Zeilenzahl weicht ab
  - `17 Zeilen im Original, 10 in der Uebersetzung`
- `tutorial/controlflow.po:1045` (../../tutorial/controlflow.rst:473) -- Code ausserhalb von Kommentaren geaendert
  - `'...     """Print a Fibonacci series less than n."""' -> '...     """Fibonacci-Folge kleiner als n ausgeben."""'`
- `tutorial/controlflow.po:1207` (../../tutorial/controlflow.rst:545) -- Code ausserhalb von Kommentaren geaendert
  - `'...     """Return a list containing the Fibonacci serie' -> '...     """Gibt eine Liste zurück, die die Fibonacci-Fo'`
- `tutorial/controlflow.po:2317` (../../tutorial/controlflow.rst:1047) -- Code ausserhalb von Kommentaren geaendert
  - `'...     """Do nothing, but document it.' -> '...     """Tut nichts, dokumentiert dies aber.'`
- `tutorial/datastructures.po:146` (../../tutorial/datastructures.rst:100) -- Code ausserhalb von Kommentaren geaendert
  - `">>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiw" -> ">>> fruits = ['Orange', 'Apfel', 'Birne', 'Banane', 'Ki"`
- `tutorial/datastructures.po:413` (../../tutorial/datastructures.rst:226) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y' -> '>>> [(x, y) für x in [1, 2, 3] für y in [3, 1, 4], wenn'`
- `tutorial/datastructures.po:425` (../../tutorial/datastructures.rst:231) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> for x in [1,2,3]:' -> '>>> for x in [1, 2, 3]:'`
- `tutorial/datastructures.po:461` (../../tutorial/datastructures.rst:246) -- Code ausserhalb von Kommentaren geaendert
  - `'File "<stdin>", line 1' -> 'Datei "<stdin>", Zeile 1'`
- `tutorial/datastructures.po:529` (../../tutorial/datastructures.rst:276) -- Code ausserhalb von Kommentaren geaendert
  - `"['3.1', '3.14', '3.142', '3.1416', '3.14159']" -> "['3,1', '3,14', '3,142', '3,1416', '3,14159']"`
- `tutorial/datastructures.po:615` (../../tutorial/datastructures.rst:313) -- Code ausserhalb von Kommentaren geaendert
  - `'...     transposed.append(transposed_row)' -> '...     transponiert.append(transponierte_Zeile)'`
- `tutorial/datastructures.po:786` (../../tutorial/datastructures.rst:384) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> a = [-1, 1, 66.25, 333, 333, 1234.5]' -> '>>> a = [-1, 1, 66,25, 333, 333, 1234,5]'`
- `tutorial/datastructures.po:1046` (../../tutorial/datastructures.rst:502) -- Code ausserhalb von Kommentaren geaendert
  - `">>> basket = {'apple', 'orange', 'apple', 'pear', 'oran" -> ">>> basket = {'Apfel', 'Orange', 'Apfel', 'Birne', 'Ora"`
- `tutorial/datastructures.po:1219` (../../tutorial/datastructures.rst:576) -- Code ausserhalb von Kommentaren geaendert
  - `'Traceback (most recent call last):' -> 'Traceback (letzter Aufruf zuletzt):'`
- `tutorial/datastructures.po:1360` (../../tutorial/datastructures.rst:640) -- Code ausserhalb von Kommentaren geaendert
  - `">>> knights = {'gallahad': 'the pure', 'robin': 'the br" -> ">>> knights = {'gallahad': 'der Reine', 'robin': 'der T"`
- `tutorial/datastructures.po:1409` (../../tutorial/datastructures.rst:660) -- Code ausserhalb von Kommentaren geaendert
  - `">>> questions = ['name', 'quest', 'favorite color']" -> ">>> Fragen = ['Name', 'Aufgabe', 'Lieblingsfarbe']"`
- `tutorial/datastructures.po:1467` (../../tutorial/datastructures.rst:684) -- Code ausserhalb von Kommentaren geaendert
  - `">>> basket = ['apple', 'orange', 'apple', 'pear', 'oran" -> ">>> basket = ['Apfel', 'Orange', 'Apfel', 'Birne', 'Ora"`
- `tutorial/datastructures.po:1503` (../../tutorial/datastructures.rst:699) -- Code ausserhalb von Kommentaren geaendert
  - `">>> basket = ['apple', 'orange', 'apple', 'pear', 'oran" -> ">>> basket = ['Apfel', 'Orange', 'Apfel', 'Birne', 'Ora"`
- `tutorial/datastructures.po:1532` (../../tutorial/datastructures.rst:711) -- Code ausserhalb von Kommentaren geaendert
  - `'[56.2, 51.7, 55.3, 52.5, 47.8]' -> '[56,2, 51,7, 55,3, 52,5, 47,8]'`
- `tutorial/errors.po:51` (../../tutorial/errors.rst:20) -- Code ausserhalb von Kommentaren geaendert
  - `'File "<stdin>", line 1' -> 'Datei "<stdin>“, Zeile 1'`
- `tutorial/errors.po:107` (../../tutorial/errors.rst:46) -- Code ausserhalb von Kommentaren geaendert
  - `'Traceback (most recent call last):' -> 'Traceback (letzter Aufruf zuletzt):'`
- `tutorial/errors.po:217` (../../tutorial/errors.rst:95) -- Code ausserhalb von Kommentaren geaendert
  - `'...         x = int(input("Please enter a number: "))' -> '...         x = int(input("Bitte gib eine Zahl ein: "))'`
- `tutorial/errors.po:483` (../../tutorial/errors.rst:203) -- Code ausserhalb von Kommentaren geaendert
  - `'print("OS error:", err)' -> 'print("OS-Fehler:", err)'`
- `tutorial/errors.po:569` (../../tutorial/errors.rst:240) -- Code ausserhalb von Kommentaren geaendert
  - `"...     print('Handling run-time error:', err)" -> "...     print('Behandlung eines Laufzeitfehlers:', err)"`
- `tutorial/errors.po:603` (../../tutorial/errors.rst:259) -- Code ausserhalb von Kommentaren geaendert
  - `'Traceback (most recent call last):' -> 'Traceback (letzter Aufruf zuletzt):'`
- `tutorial/errors.po:646` (../../tutorial/errors.rst:277) -- Code ausserhalb von Kommentaren geaendert
  - `"...     print('An exception flew by!')" -> "...     print('Eine Ausnahme ist aufgetreten!')"`
- `tutorial/errors.po:686` (../../tutorial/errors.rst:299) -- Code ausserhalb von Kommentaren geaendert
  - `'...     raise RuntimeError("unable to handle error")' -> '...     raise RuntimeError("Fehler kann nicht behandelt'`
- `tutorial/errors.po:748` (../../tutorial/errors.rst:325) -- Code ausserhalb von Kommentaren geaendert
  - `"...     raise RuntimeError('Failed to open database') f" -> "...     raise RuntimeError('Datenbank konnte nicht geöf"`
- `tutorial/errors.po:804` (../../tutorial/errors.rst:350) -- Code ausserhalb von Kommentaren geaendert
  - `'Traceback (most recent call last):' -> 'Traceback (letzter Aufruf zuletzt):'`
- `tutorial/errors.po:891` (../../tutorial/errors.rst:392) -- Code ausserhalb von Kommentaren geaendert
  - `"...     print('Goodbye, world!')" -> "...     print('Auf Wiedersehen, Welt!')"`
- `tutorial/errors.po:1022` (../../tutorial/errors.rst:452) -- Code ausserhalb von Kommentaren geaendert
  - `'...         print("division by zero!")' -> '...         print("Division durch Null!")'`
- `tutorial/errors.po:1260` (../../tutorial/errors.rst:564) -- Code ausserhalb von Kommentaren geaendert
  - `'...                 "group2",' -> '...                 group2,'`
- `tutorial/errors.po:1356` (../../tutorial/errors.rst:610) -- Code ausserhalb von Kommentaren geaendert
  - `'...    raise ExceptionGroup("Test Failures", excs)' -> '...    raise ExceptionGroup("Testfehler", excs)'`
- `tutorial/errors.po:1403` (../../tutorial/errors.rst:634) -- Code ausserhalb von Kommentaren geaendert
  - `"...     raise TypeError('bad type')" -> "...     raise TypeError('falscher Typ')"`
- `tutorial/errors.po:1446` (../../tutorial/errors.rst:653) -- Code ausserhalb von Kommentaren geaendert
  - `"...     raise OSError('operation failed')" -> "...     raise OSError('Vorgang fehlgeschlagen')"`
- `tutorial/floatingpoint.po:263` (../../tutorial/floatingpoint.rst:113) -- Code ausserhalb von Kommentaren geaendert
  - `'False' -> 'Falsch'`
- `tutorial/floatingpoint.po:534` (../../tutorial/floatingpoint.rst:235) -- Code ausserhalb von Kommentaren geaendert
  - `'8.042178034628478e-13' -> '8.0421778034628478e-13'`
- `tutorial/floatingpoint.po:775` (../../tutorial/floatingpoint.rst:351) -- Code ausserhalb von Kommentaren geaendert
  - `"Decimal('0.10000000000000000555111512312578270211815834" -> "Decimal('0,10000000000000000555111512312578270211815834"`
- `tutorial/inputoutput.po:81` (../../tutorial/inputoutput.rst:32) -- Code ausserhalb von Kommentaren geaendert
  - `">>> f'Results of the {year} {event}'" -> ">>> f'Ergebnisse des {year} {event} '"`
- `tutorial/inputoutput.po:108` (../../tutorial/inputoutput.rst:46) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> percentage = yes_votes / total_votes' -> '>>> prozent = Ja-Stimmen / Gesamtstimmen'`
- `tutorial/inputoutput.po:184` (../../tutorial/inputoutput.rst:77) -- Code ausserhalb von Kommentaren geaendert
  - `">>> s = 'Hello, world.'" -> ">>> s = 'Hallo, Welt.'"`
- `tutorial/inputoutput.po:270` (../../tutorial/inputoutput.rst:126) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print(f'The value of pi is approximately {math.pi:." -> ">>> print(f'Der Wert von Pi beträgt ungefähr {math.pi:."`
- `tutorial/inputoutput.po:317` (../../tutorial/inputoutput.rst:145) -- Code ausserhalb von Kommentaren geaendert
  - `">>> animals = 'eels'" -> ">>> animals = 'Aale'"`
- `tutorial/inputoutput.po:361` (../../tutorial/inputoutput.rst:171) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> print(\'We are the {} who say "{}!"\'.format(\'knights' -> '>>> print(\'Wir sind die {}, die "{}!" sagen\'.format(\'Ri'`
- `tutorial/inputoutput.po:382` (../../tutorial/inputoutput.rst:179) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print('{0} and {1}'.format('spam', 'eggs'))" -> ">>> print('{0} und {1}'.format('Spam', 'Eier'))"`
- `tutorial/inputoutput.po:402` (../../tutorial/inputoutput.rst:187) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print('This {food} is {adjective}.'.format(" -> ">>> print('Diese {food} lautet {adjective}.'.format("`
- `tutorial/inputoutput.po:417` (../../tutorial/inputoutput.rst:193) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print('The story of {0}, {1}, and {other}.'.format(" -> ">>> print('Die Geschichte von {0}, {1} und {other}.'.fo"`
- `tutorial/inputoutput.po:482` (../../tutorial/inputoutput.rst:217) -- Code ausserhalb von Kommentaren geaendert
  - `'>>> message = " ".join([f\'{k}: \' + \'{\' + k +\'};\' for k ' -> '>>> message = " ".join([f\'{k}: \' + \'{\' + k + \'};\' for k'`
- `tutorial/inputoutput.po:624` (../../tutorial/inputoutput.rst:279) -- Code ausserhalb von Kommentaren geaendert
  - `"'-003.14'" -> "'-003,14'"`
- `tutorial/inputoutput.po:658` (../../tutorial/inputoutput.rst:297) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print('The value of pi is approximately %5.3f.' % m" -> ">>> print('Der Wert von Pi beträgt ungefähr %5.3f.' % m"`
- `tutorial/inputoutput.po:810` (../../tutorial/inputoutput.rst:379) -- Code ausserhalb von Kommentaren geaendert
  - `'Traceback (most recent call last):' -> 'Traceback (letzter Aufruf zuletzt):'`
- `tutorial/inputoutput.po:858` (../../tutorial/inputoutput.rst:403) -- Code ausserhalb von Kommentaren geaendert
  - `"'This is the entire file.\\n'" -> "'Das ist der gesamte Inhalt der Datei.\\n'"`
- `tutorial/inputoutput.po:887` (../../tutorial/inputoutput.rst:415) -- Code ausserhalb von Kommentaren geaendert
  - `"'This is the first line of the file.\\n'" -> "'Dies ist die erste Zeile der Datei.\\n'"`
- `tutorial/inputoutput.po:912` (../../tutorial/inputoutput.rst:425) -- Code ausserhalb von Kommentaren geaendert
  - `'This is the first line of the file.' -> 'Dies ist die erste Zeile der Datei.'`
- `tutorial/inputoutput.po:942` (../../tutorial/inputoutput.rst:437) -- Code ausserhalb von Kommentaren geaendert
  - `">>> f.write('This is a test\\n')" -> ">>> f.write('Das ist ein Test\\n')"`
- `tutorial/inputoutput.po:958` (../../tutorial/inputoutput.rst:443) -- Code ausserhalb von Kommentaren geaendert
  - `">>> value = ('the answer', 42)" -> ">>> value = ('die Antwort', 42)"`
- `tutorial/introduction.po:532` (../../tutorial/introduction.rst:230) -- Code ausserhalb von Kommentaren geaendert
  - `">>> text = ('Put several strings within parentheses '" -> ">>> text = ('Setze mehrere Strings in Klammern, '"`
- `tutorial/introduction.po:1293` (../../tutorial/introduction.rst:550) -- Code ausserhalb von Kommentaren geaendert
  - `">>> print('The value of i is', i)" -> ">>> print('Der Wert von i ist', i)"`
- `tutorial/modules.po:643` (../../tutorial/modules.rst:283) -- Code ausserhalb von Kommentaren geaendert
  - `"C> print('Yuck!')" -> "C> print('Igitt!')"`
- `tutorial/stdlib.po:73` (../../tutorial/stdlib.rst:32) -- Zeilenzahl weicht ab
  - `5 Zeilen im Original, 3 in der Uebersetzung`
- `tutorial/stdlib.po:179` (../../tutorial/stdlib.rst:83) -- Code ausserhalb von Kommentaren geaendert
  - `"description='Show top lines from each file')" -> "description='Die ersten Zeilen jeder Datei anzeigen')"`
- `tutorial/stdlib.po:226` (../../tutorial/stdlib.rst:107) -- Code ausserhalb von Kommentaren geaendert
  - `">>> sys.stderr.write('Warning, log file not found start" -> ">>> sys.stderr.write('Warning, log file not found start"`
- `tutorial/stdlib.po:391` (../../tutorial/stdlib.rst:185) -- Code ausserhalb von Kommentaren geaendert
  - `'Last updated on Nov 11, 2025 (20:11 UTC).' -> '"      Last updated on Nov 11, 2025 (20:11 UTC).'`
- `tutorial/stdlib.po:609` (../../tutorial/stdlib.rst:295) -- Code ausserhalb von Kommentaren geaendert
  - `'"""Computes the arithmetic mean of a list of numbers.' -> '"""Berechnet das arithmetische Mittel einer Liste von Z'`
- `tutorial/stdlib2.po:483` (../../tutorial/stdlib2.rst:218) -- Code ausserhalb von Kommentaren geaendert
  - `"logging.debug('Debugging information')" -> "logging.debug('Informationen zur Fehlersuche')"`

## literal -- ``Literale`` aus dem Original fehlen in der Uebersetzung -- Code wurde mituebersetzt

- `builtins/functions.po:1560` (../../builtins/functions.rst:704) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['exec']`
- `builtins/functions.po:3038` (../../builtins/functions.rst:1548) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['flags', 'mode']`
- `builtins/functions.po:3083` (../../builtins/functions.rst:1568) -- Literale fehlen in der Uebersetzung
  - `fehlt: ["'namereplace'"]`
- `builtins/functions.po:3102` (../../builtins/functions.rst:1576) -- Literale fehlen in der Uebersetzung
  - `fehlt: ["'U'"]`
- `builtins/functions.po:4522` (../../builtins/functions.rst:2289) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['strict=True']`
- `builtins/functions.po:4676` (../../builtins/functions.rst:2361) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['import spam']`
- `builtins/stdtypes.po:82` (../../builtins/stdtypes.rst:46) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['False']`
- `builtins/stdtypes.po:175` (../../builtins/stdtypes.rst:93) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['x and y']`
- `builtins/stdtypes.po:5281` (../../builtins/stdtypes.rst:2782) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['None']`
- `builtins/stdtypes.po:5355` (../../builtins/stdtypes.rst:2825) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['s.swapcase().swapcase() == s']`
- `c-api/call.po:529` (../../c-api/call.rst:363) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['_PyObject_Vectorcall']`
- `library/string.po:1683` (../../library/string.rst:841) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['"identifier"', '"identifier"']`
- `library/string.po:1700` (../../library/string.rst:848) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['"${noun}ification"']`
- `library/turtle.po:2394` (../../library/turtle.rst:1310) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['with turtle.fill():']`
- `library/turtle.po:3231` (../../library/turtle.rst:1895) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['"#33cc8c"', '"red"', '"yellow"']`
- `tutorial/classes.po:635` (../../tutorial/classes.rst:276) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['"A simple example class"']`
- `tutorial/classes.po:1357` (../../tutorial/classes.rst:605) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['BaseClassName.methodname(self, arguments)']`
- `tutorial/classes.po:1521` (../../tutorial/classes.rst:685) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['_classname__spam', 'classname']`
- `tutorial/controlflow.po:78` (../../tutorial/controlflow.rst:33) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['case', 'switch']`
- `tutorial/controlflow.po:945` (../../tutorial/controlflow.rst:428) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['"bandwidth"', '"latency"', '{"bandwidth": b, "latency": l}']`
- `tutorial/controlflow.po:1251` (../../tutorial/controlflow.rst:564) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['methodname', 'obj.methodname']`
- `tutorial/controlflow.po:1466` (../../tutorial/controlflow.rst:665) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['kwarg=value']`
- `tutorial/floatingpoint.po:632` (../../tutorial/floatingpoint.rst:282) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['< 2**53', '>= 2**52']`
- `tutorial/interpreter.po:119` (../../tutorial/interpreter.rst:51) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['python -c command [arg] ...']`
- `tutorial/interpreter.po:133` (../../tutorial/interpreter.rst:57) -- Literale fehlen in der Uebersetzung
  - `fehlt: ['python -m module [arg] ...']`

## typo -- Typografische Anfuehrungszeichen innerhalb von Code oder Literalen

- `tutorial/errors.po:51` (../../tutorial/errors.rst:20) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> while True print('Hello world')
  Datei "<stdin>“, Zeile`
- `tutorial/errors.po:107` (../../tutorial/errors.rst:46) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> 10 * (1/0)
Traceback (letzter Aufruf zuletzt):
  Datei "`
- `tutorial/errors.po:603` (../../tutorial/errors.rst:259) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> raise NameError('HiThere')
Traceback (letzter Aufruf zul`
- `tutorial/errors.po:646` (../../tutorial/errors.rst:277) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> try:
...     raise NameError('HiThere')
... except NameE`
- `tutorial/errors.po:686` (../../tutorial/errors.rst:299) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> try:
...     open("database.sqlite")
... except OSError:`
- `tutorial/errors.po:748` (../../tutorial/errors.rst:325) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> def func():
...     raise ConnectionError
...
>>> try:
.`
- `tutorial/errors.po:804` (../../tutorial/errors.rst:350) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> try:
...     open('database.sqlite')
... except OSError:`
- `tutorial/errors.po:891` (../../tutorial/errors.rst:392) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> try:
...     raise KeyboardInterrupt
... finally:
...   `
- `tutorial/errors.po:1022` (../../tutorial/errors.rst:452) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> def divide(x, y):
...     try:
...         result = x / `
- `tutorial/errors.po:1260` (../../tutorial/errors.rst:564) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> def f():
...     raise ExceptionGroup(
...         "grou`
- `tutorial/errors.po:1403` (../../tutorial/errors.rst:634) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> try:
...     raise TypeError('falscher Typ')
... except `
- `tutorial/errors.po:1446` (../../tutorial/errors.rst:653) -- Typografische Anfuehrungszeichen im Code
  - `“ in: >>> def f():
...     raise OSError('Vorgang fehlgeschlagen')`

## bindestrich -- Leerzeichen zwischen Rolle und angehaengtem Wort

- `c-api/arg.po:143` (../../c-api/arg.rst:63) -- Leerzeichen vor Bindestrich
  - ` :class:`bytes`, und stellen einen ``const char *`` -Zeiger auf dessen Puffer b`
- `c-api/arg.po:251` (../../c-api/arg.rst:107) -- Leerzeichen vor Bindestrich
  - `nicode-Objekte werden mithilfe der ``'utf-8'`` -Kodierung in C-Zeichenkett`
- `c-api/arg.po:760` (../../c-api/arg.rst:292) -- Leerzeichen vor Bindestrich
  - `:class:`bytearray` -Objekte zulassen.`
- `c-api/arg.po:798` (../../c-api/arg.rst:306) -- Leerzeichen vor Bindestrich
  - `plexe Zahl aus Python in eine C- :c:type:`Py_complex` -Struktur.`
- `c-api/arg.po:1551` (../../c-api/arg.rst:671) -- Leerzeichen vor Bindestrich
  - `Konvertiert eine einfache C- :c:expr:`int` -Variable in ein Python-Int`
- `c-api/arg.po:1609` (../../c-api/arg.rst:703) -- Leerzeichen vor Bindestrich
  - `Konvertieren Sie eine C- :c:type:`Py_ssize_t` -Zahl in eine Python-Ganzza`
- `c-api/arg.po:1614` (../../c-api/arg.rst:706) -- Leerzeichen vor Bindestrich
  - `Konvertiert ein C- :c:expr:`int` -Objekt in ein Python- :cla`
- `c-api/arg.po:1638` (../../c-api/arg.rst:717) -- Leerzeichen vor Bindestrich
  - `ein Byte darstellt, in ein Python- :class:`bytes` -Objekt der Länge 1.`
- `c-api/arg.po:1646` (../../c-api/arg.rst:721) -- Leerzeichen vor Bindestrich
  - ` Zeichen darstellt, in ein Python- :class:`str` -Objekt der Länge 1.`
- `c-api/arg.po:1654` (../../c-api/arg.rst:725) -- Leerzeichen vor Bindestrich
  - `Konvertieren Sie eine C- :c:expr:`double` -Zahl in eine Python-Gleitk`
- `c-api/arg.po:1660` (../../c-api/arg.rst:728) -- Leerzeichen vor Bindestrich
  - `Konvertieren Sie eine C- :c:expr:`float` -Zahl in eine Python-Gleitk`
- `c-api/arg.po:1669` (../../c-api/arg.rst:731) -- Leerzeichen vor Bindestrich
  - `Konvertieren Sie eine C- :c:type:`Py_complex` -Struktur in eine komplexe `
- `library/csv.po:959` (../../library/csv.rst:534) -- Leerzeichen vor Bindestrich
  - `Reader-Objekte (:class:`DictReader` -Instanzen und Objekte, die`
- `tutorial/errors.po:305` (../../tutorial/errors.rst:129) -- Leerzeichen vor Bindestrich
  - `Eine Klasse in einer  :keyword:`except` -Klausel deckt Ausnahmen ab`
- `tutorial/errors.po:978` (../../tutorial/errors.rst:431) -- Leerzeichen vor Bindestrich
  - `Wenn eine  :keyword:`!finally` -Klausel eine  :keyword:`!r`
- `tutorial/modules.po:584` (../../tutorial/modules.rst:253) -- Leerzeichen vor Bindestrich
  - `nicht schneller, wenn es aus einer ``.pyc`` -Datei geladen wird, als we`
- `tutorial/modules.po:991` (../../tutorial/modules.rst:441) -- Leerzeichen vor Bindestrich
  - `Die :file:`__init__.py`  -Dateien sind erforderlich,`
- `tutorial/modules.po:1203` (../../tutorial/modules.rst:534) -- Leerzeichen vor Bindestrich
  - `le des Pakets, die durch vorherige :keyword:`import` -Anweisungen explizit gelad`
- `tutorial/stdlib2.po:386` (../../tutorial/stdlib2.rst:174) -- Leerzeichen vor Bindestrich
  - `de Code zeigt, wie das High-Level- :mod:`threading` -Modul Aufgaben im Hintergr`
