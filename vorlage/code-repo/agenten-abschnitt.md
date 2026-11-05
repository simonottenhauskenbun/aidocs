<!--
Abschnitt für CLAUDE.md und/oder AGENTS.md im Code-Repo.
In der Sprache der übrigen Agenten-Anweisungen des Repos formulieren.
-->

## Planungsdokumente (`.aidocs/`)

Die Planung läuft AI-first statt über Jira/Kanban. Ggf. Grobplanung (`PLAN.md`), TODOs (`TODO.md`), Entscheidungen des Users (`DECISIONS.md`) offene Fragen (`QUESTIONS.md`) und ggf. Erkenntnisse (`FINDINGS.md`) liegen im separaten Repo `<url-des-planungs-repos>`, ausgecheckt als `./.aidocs/` (hier gitignored, kein Submodul). Vor dem Planen oder Umsetzen dort lesen. Die Regeln für die Pflege stehen in `.aidocs/README.md`.

- `.aidocs/` bleibt auf `main`, egal welcher Branch hier ausgecheckt ist. `python aidocs-sync.py` klont es bei Bedarf, wechselt auf `main`, pullt mit `--rebase` und installiert einen `post-checkout`-Hook. Zu Beginn jeder Sitzung ausführen (bei Claude Code erledigt das der `SessionStart`-Hook in `.claude/settings.json`).
- In `.aidocs/` nach jeder Änderung sofort committen und pushen, ohne Rückfrage. In diesem Repo nur auf ausdrückliche Anweisung committen oder pushen.
- Nach jedem umgesetzten Schritt zuerst eine kurze, klare Liste geben: neue Fragen (Q-x), neue Agenten-Entscheidungen (K-x), neue Erkenntnisse (F-x), jeweils mit einer Zeile oder „keine“. Was der User wissen oder entscheiden muss, steht als Eintrag in `.aidocs/`, nicht nur in der Antwort.
- Eine KI-Entscheidung nie als Entscheidung des Users eintragen; sie kommt als K-x nach `QUESTIONS.md`.
- Jede Frage, Entscheidung und Erkenntnis nennt, von wem sie stammt (`Entschieden von:` / `Erfasst von: <Agent> für <Name>`).
- *(Optional, nur mit `FINDINGS.md`)* Erkenntnisse aus der Arbeit (Ursachen, Eigenheiten, Messergebnisse, Sackgassen, Gründe für nicht offensichtliche Lösungen) als F-x in `.aidocs/FINDINGS.md` festhalten, nicht als Kommentar im Code. Im Code nur Kommentare, die der Code selbst zum Verständnis braucht.
- Code, Kommentare und Commits in diesem Repo verweisen nicht auf die Planungsdokumente.
