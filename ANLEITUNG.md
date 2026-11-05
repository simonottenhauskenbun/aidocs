# Anleitung für Agenten: aidocs-Muster einrichten

Du sollst das aidocs-Muster in dem Repo einrichten, in dem du gerade arbeitest. Übernimm das **Konzept**, nicht die Dateien eins zu eins: Passe Namen, Sprache, Dokumente und Werkzeuge an das Projekt und das Team an. Die Dateien unter `vorlage/` sind Beispiele aus einem echten Projekt.

## 1. Konzept verstehen

Lies [README.md](README.md) und die Dateien unter [vorlage/](vorlage/). Die tragenden Regeln, die erhalten bleiben sollen:

1. Planung liegt in einem **eigenen Git-Repo**, im Code-Repo als `./.aidocs/` ausgecheckt und per `.gitignore` ausgeschlossen (kein Submodul).
2. `.aidocs/` bleibt **immer auf `main`**, unabhängig vom Branch im Code-Repo. Ein Sync-Skript stellt das sicher und läuft automatisch.
3. In `.aidocs/` committen und pushen Agenten **selbständig** und sofort, mit `pull --rebase` vorher. Im Code-Repo nur auf ausdrückliche Anweisung.
4. Entscheidungen des Users, offene Fragen und noch zu bestätigende KI-Entscheidungen haben **stabile IDs** in eigenen Dateien. Eine KI-Entscheidung wird nie als User-Entscheidung eingetragen. Jeder Eintrag nennt die Person, von der er stammt (bei Agenten: Agent und die Person, für die er arbeitet). Neue IDs erst nach einem Pull vergeben, fortlaufend nach der höchsten.
5. `TODO.md` bleibt konkret und schlank. Code, Kommentare und Commits im Code-Repo verweisen nicht auf die Planungsdokumente.
6. Nach jedem umgesetzten Schritt gibt der Agent **zuerst eine kurze, klare Liste**: neue Fragen (Q-x), neue Agenten-Entscheidungen (K-x), neue Erkenntnisse (F-x, falls genutzt), jeweils mit ID und einer Zeile, oder „keine“. Erst danach folgt, was er sonst noch sagen will.

Optional, nur nach Rückfrage (Schritt 3):

- **`PLAN.md`:** Grobplanung, aus der die TODO-Liste am Anfang entsteht. Sinnvoll bei größeren Vorhaben mit Anforderungsdokumenten; bei kleinen Vorhaben entsteht `TODO.md` direkt.
- **`FINDINGS.md`:** Erkenntnisse aus der Arbeit (Ursachen, Eigenheiten, Messergebnisse, Sackgassen) kommen als F-x dorthin, **nicht als Code-Kommentare**. Im Code bleiben nur Kommentare, die der Code selbst zum Verständnis braucht. Bestehende erklärende Kommentare lässt du beim Einrichten stehen; die Regel gilt für neue Arbeit.
- **„Umgesetzt von <Name> auf <Branch>“** pro Arbeitspaket in `TODO.md`, sinnvoll, wenn mehrere Personen oder Agenten parallel auf verschiedenen Branches arbeiten.

Was nicht gewählt wird, lässt du in allen angelegten Dateien weg (Regeln, Inhaltstabelle, Verweise, ID-Präfixe).

Alles andere (Dateinamen, ID-Präfixe, zusätzliche Dokumente, Sprache) ist anpassbar.

## 2. Repo analysieren

Bevor du fragst, finde selbst heraus:

- Gibt es schon Planungsdokumente (TODO-Listen, `docs/`, Issues, ein bestehendes `.aidocs/`)? Dann übernehmen statt doppelt anlegen.
- Welche Agenten-Konfiguration existiert: `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, andere?
- Remote-URL und Hosting (`git remote get-url origin`), Sprache der vorhandenen Doku, Branch-Konventionen, ob mehrere Personen am Repo arbeiten.
- Welche Skriptsprache im Projekt ohnehin verfügbar ist (die Referenz `aidocs-sync.py` braucht nur Python 3 ohne Pakete).

## 3. Rückfragen stellen

Frag den User nur, was du nicht selbst klären kannst, gebündelt in einer Runde. Typische Fragen:

- **Ort und Name des Planungs-Repos.** Vorschlag: `<code-repo>-aidocs`, privat, beim selben Owner. Existiert es schon, oder sollst du es anlegen?
- **Variante.** Planungs-Repo neben einem Code-Repo (Standard) oder eigenständiges Planungs-Repo ohne Code (z. B. für Vorfälle, Audits, Recherchen)?
- **Plan.** Soll es eine `PLAN.md` als Grobplanung geben, aus der die TODO-Liste entsteht?
- **Erkenntnisse.** Soll es `FINDINGS.md` (F-x) geben, damit Erkenntnisse dort statt als Code-Kommentare landen?
- **Dokumente.** Reichen `TODO.md`, `DECISIONS.md`, `QUESTIONS.md`? Braucht es zusätzlich z. B. Fragen an einen Auftraggeber, ein Bug-Register, Anforderungsdokumente?
- **Sprache** der Planungsdokumente.
- **Team.** Arbeiten mehrere Personen bzw. Agenten parallel auf verschiedenen Branches? Soll jedes Arbeitspaket die Zeile „Umgesetzt von <Name> auf <Branch>“ bekommen?
- **Commit-Regeln im Code-Repo**, falls nicht schon festgelegt (z. B. Branch-Präfixe pro Person).

## 4. Einrichten

### Variante A: Planungs-Repo neben einem Code-Repo

1. **Planungs-Repo anlegen** (nach Rückfrage), z. B. mit `gh repo create <owner>/<name>-aidocs --private`, und als `./.aidocs/` klonen.
2. **Startdateien** in `.aidocs/` anlegen, angelehnt an [vorlage/aidocs-repo/](vorlage/aidocs-repo/):
   - `README.md` mit Zweck, Einbindung, Inhaltstabelle und **Agentenregeln**. Die Agentenregeln stehen im Planungs-Repo, damit sie für jeden Agenten gelten, der dort arbeitet.
   - `TODO.md`, `DECISIONS.md`, `QUESTIONS.md` und was in Schritt 3 vereinbart wurde (z. B. `PLAN.md`, `FINDINGS.md`). Bestehende Planung aus dem Code-Repo übernehmen.
   - Ersten Commit machen und pushen (das ist erlaubt, Regel 3).
3. **Code-Repo vorbereiten**, angelehnt an [vorlage/code-repo/](vorlage/code-repo/):
   - `/.aidocs/` in `.gitignore`.
   - Sync-Skript (`aidocs-sync.py` oder Entsprechung) ins Repo-Root. Es leitet die URL des Planungs-Repos aus `origin` ab (`foo` → `foo-aidocs`); weicht sie ab, die Konstante im Skript setzen.
   - Automatischer Start: Das Skript installiert beim ersten Lauf selbst einen `post-checkout`-Hook. Zusätzlich den Session-Start des Agenten nutzen, damit frische Klone sofort eingerichtet sind:
     - Claude Code: `SessionStart`-Hook in `.claude/settings.json` (siehe [claude-settings.json](vorlage/code-repo/claude-settings.json)); vorhandene Einstellungen zusammenführen, nicht überschreiben.
     - Andere Agenten (z. B. Codex): falls das Werkzeug Session-Hooks hat, dort eintragen; sonst in `AGENTS.md` anweisen, das Skript zu Beginn jeder Sitzung auszuführen.
   - Abschnitt zu `.aidocs/` in die Agenten-Anweisungen (`CLAUDE.md`, `AGENTS.md` oder beide), angelehnt an [agenten-abschnitt.md](vorlage/code-repo/agenten-abschnitt.md). Nutzt das Repo beide Dateien, den Abschnitt nur an einer Stelle pflegen und von der anderen verweisen.
4. **Prüfen:** Skript einmal ausführen, Branch im Code-Repo wechseln und zurück, kontrollieren, dass `.aidocs/` auf `main` bleibt und `git status` im Code-Repo sauber ist (außer den neuen Dateien).
5. Die Änderungen im **Code-Repo nicht committen**, sondern dem User zeigen, außer er sagt etwas anderes.

### Variante B: eigenständiges Planungs-Repo

Kein Sync-Skript, kein `.aidocs/`. Das Planungs-Repo ist das Arbeitsverzeichnis; die Agentenregeln stehen in dessen `CLAUDE.md`/`AGENTS.md` bzw. README. Für Claude Code kann ein `SessionStart`-Hook mit `git pull --ff-only` den aktuellen Stand holen. Untersuchte Repos oder Systeme werden nur gelesen, nicht eingebunden.

## 5. Abschluss

Fasse für den User zusammen: was angelegt wurde, welche Annahmen du getroffen hast (als K-x in `QUESTIONS.md` eintragen) und was er noch tun muss (z. B. Teammitglieder zum Planungs-Repo einladen).
