# Unterstützung an der deutschen Python-Dokumentation

Willkommen!
Dieses Repository enthält die deutsche Übersetzung der
Python-Dokumentation. 
[Generelles](https://devguide.python.org/documentation/translations/translating/)  

Format sind Gettext-Dateien (`.po`). Übersetzt wird ausschließlich der `msgstr`. 
Das englische `msgid` bleibt unverändert.

Unterstützung ist willkommen bei:

- Übersetzen noch offener Dateien
- Korrekturlesen bereits übersetzter Dateien
- Vereinheitlichen von Fachbegriffen
- Fehlermeldungen zu Formulierungen, Links oder Auszeichnung

---

## Zwei Wege

| | Repository (GitHub) | Transifex |
|---|---|---|
| Für wen | wer mit Git und einem PO-Editor arbeitet | wer nur übersetzen will |
| Ablauf | Fork → Branch → Pull Request | Online-Editor |
| Prüfung | lokal vor dem Pull Request | durch den Maintainer beim Übernehmen |
| Vorteil | Prüfskripte, voller Dateikontext | kein Setup nötig |

Das Repository ist die führende Quelle.
Der Stand wird regelmäßig nach Transifex geschoben, damit die File in Transifex
syncronisiert bleiben. Dateien an denen gearbeitet wird, werden ausgelassen.

---

## Bevor du anfängst

**Öffne ein Issue** mit der Datei, die du übernehmen willst, zum Beispiel
„Übersetzung `library/pathlib.po`“. Das gilt für beide Wege und verhindert,
dass zwei Leute dieselbe Datei übersetzen.

### Welche Dateien sind offen?

**Ohne Installation:** In
[Transifex](https://explore.transifex.com/python-doc/python-newest/) steht in
der Ressourcenliste für jede Datei der Fortschritt in Prozent. Dafür brauchst
du nur ein Transifex-Konto.


**Im Terminal:** Einmal das Repository holen, dann im Wurzelverzeichnis des
Repositorys:

```
git clone https://github.com/python/python-docs-de.git
cd python-docs-de
git checkout 3.15
python3 _tools/po_status.py . --sort percent --max-percent 99
```

Ausgegeben werden Übersetzungsstand (`x/y`), Prozent, Größe und Pfad, die am
wenigsten übersetzten Dateien zuletzt. `--max-percent 99` blendet die
fertigen Dateien aus.

Das Skript ruft `msgfmt` auf, du brauchst also **gettext**:

| | |
|---|---|
| macOS | `brew install gettext` |
| Debian/Ubuntu | `sudo apt install gettext` |
| Fedora | `sudo dnf install gettext` |
| Windows | über [WSL](https://learn.microsoft.com/windows/wsl/install) oder [Git Bash](https://gitforwindows.org/) mit gettext |

---

## Weg 1: Im Repository

### 1. Fork und Branch

Auf GitHub oben rechts **Fork**, dann im Terminal:

```
git clone https://github.com/<dein-konto>/python-docs-de.git
cd python-docs-de
git checkout 3.15
git checkout -b uebersetzung-pathlib
```

Alle weiteren Befehle in dieser Datei laufen in diesem Verzeichnis, also im
Wurzelverzeichnis des Repositorys.

Für eine kleine Korrektur, kann direkt die Datei auf GitHub geöffnen werden, 
Stift-Symbol -> ändern -> Pull Request.
Die Prüfungen laufen dann in der CI. Für eine ganze Datei ist der
Browser-Editor nicht geeignet, dafür fehlt ihm die PO-Unterstützung.
Empfohlen ist z.B. **[Poedit](https://poedit.net/)**.

### 2. Prüfen

```
./_tools/pre_push_check.sh --quick
```

Dauert etwa eine Minute und prüft:

| Prüfung | findet |
|---|---|
| `msgfmt --check` | Syntaxfehler in der PO-Datei |
| `sphinx-lint` | kaputte reST-Auszeichnung |
| `check_roles.py` | fehlende, zusätzliche oder veränderte Rollen (`:ref:`, `:term:`, …) |
| `check_markup.py` | übersetzte Codeblöcke, abweichende ``Literale`` |
| `check_satzzeichen.py` | Semikolon mit kleingeschriebener Fortsetzung, doppelter Satzabstand |

Erst wenn das durchläuft, lohnt der Pull Request. `--full` hängt zusätzlich
einen echten Sphinx-Build an (10–20 Minuten) – nötig nur bei größeren
Änderungen.

Voraussetzung neben gettext: `pip install sphinx-lint`. Sobald du in deinen
Fork pushst, laufen Syntax- und Lint-Prüfung außerdem automatisch als
GitHub Action.

### 3. Pull Request

Gegen `python/python-docs-de`, akuteller Branch `3.15`. Eine Datei oder ein Thema
pro Pull Request. In der Beschreibung das zugehörige Issue verlinken.

---

## Weg 2: Über Transifex

Projekt: [python-newest](https://explore.transifex.com/python-doc/python-newest/),
Sprache Deutsch.

Der Transifex-Editor zeigt nur den sichtbaren Text – die reST-Syntax
dahinter bleibt unsichtbar. Genau dort entstehen die Fehler, die später
Nacharbeit kosten. **Lies vorher
[`_doc/TRANSIFEX-TRANSLATION.md`](_doc/TRANSIFEX-TRANSLATION.md).**

Die häufigsten Fälle in einem Satz:

- `:ref:`-Ziele sind Anker, kein Text: `` :term:`Bytecode <bytecode>` ``,
  nie `` :term:`Bytecode` ``.
- Jede Rolle aus dem Original muss in der Übersetzung wieder vorkommen.
- Platzhalter (`%s`, `{0}`, `%(release)s`) bleiben unverändert.
- Durchgehend „Du“-Form. DeepL übersetzt automatisch mit „Sie“.

Auch hier gilt: **Issue aufmachen**, bevor du eine Datei beginnst.

---

## Terminologie

Bei Fachbegriffen entscheidet in dieser Reihenfolge:

1. **`glossary.po`** – die veröffentlichte Begriffsliste.
2. **[`_doc/GLOSSAR.md`](_doc/GLOSSAR.md)** – alles, was dort nicht vorkommt.
3. **Der Bestand im Repo** – ein `grep` über die `.po`-Dateien zeigt, wie
   der Begriff bisher übersetzt wurde.

Ist ein Begriff nirgends festgelegt, entscheide und trage ihn in
`_doc/GLOSSAR.md` nach. Dort stehen auch die Regeln zu Du-Form,
Zeichensetzung und Anführungszeichen.

---

## KI-Unterstützung

Wer mit einem KI-Assistenten übersetzt, findet in
[`_doc/AI-SKILLS.md`](_doc/AI-SKILLS.md) die Regeln in einer Form, die
sich direkt als Kontext übergeben lässt: Terminologie, reST-Auszeichnung,
Codeblöcke, Prüfablauf.

Zwei Grenzen:

- Maschinell übersetzte Dateien ohne eigene Durchsicht werden nicht
  übernommen.
- Das `msgid` wird nie verändert.

---

## Fragen

Öffne ein [Issue](https://github.com/python/python-docs-de/issues). Auch
für Fragen zur Formulierung, nicht nur für Fehler.
