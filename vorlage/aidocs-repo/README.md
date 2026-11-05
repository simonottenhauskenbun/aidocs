# <projekt>-aidocs

Planungsdokumente für [<projekt>](<url-zum-code-repo>). Die Planung läuft AI-first statt über Jira/Kanban: Dieses Repo wird vollständig von KI-Agenten gepflegt.

## Einbindung

- Ausgecheckt als `./.aidocs/` im Code-Repo (dort per `.gitignore` ausgeschlossen, kein Submodul).
- Steht immer auf `main`, unabhängig vom Branch im Code-Repo. `aidocs-sync.py` im Code-Repo sorgt dafür, ausgelöst durch einen `post-checkout`-Git-Hook und den Session-Start des Agenten.
- Relative Links auf Code zeigen über `../` ins Code-Repo, z. B. `../src/main.rs`.

## Inhalt

| Datei | Zweck |
|---|---|
| `PLAN.md` | Optional: Grobplanung, aus der `TODO.md` entsteht |
| `TODO.md` | Arbeitsschritte mit Checkboxen und Abhängigkeiten |
| `DECISIONS.md` | Entscheidungen des Users (D-x) |
| `QUESTIONS.md` | Offene Fragen (Q-x) und noch zu bestätigende KI-Entscheidungen (K-x) |
| `FINDINGS.md` | Optional: Erkenntnisse beim Arbeiten (F-x), statt Code-Kommentaren |

## Workflow

- **Planen:** Idee, Anforderungen und weitere Informationen → `PLAN.md` (Grobplanung, mit dem User iterieren) → in `TODO.md` überführen.
- **TODO ändern:** „Füge neuen Schritt X.y hinzu: …“, „Streiche Schritt X.y.“
- **Umsetzen:** „Setze TODO-Schritt X.y um.“ Der Agent implementiert, hakt ab und legt bei Bedarf Q-x, K-x und F-x an.
- **Klären:** Beantwortete Fragen (Q-x) und bestätigte Agenten-Entscheidungen (K-x) werden zu Entscheidungen (D-x).

## Regeln für Agenten

- **Nach jedem umgesetzten Schritt zuerst eine kurze, klare Liste** geben, bevor irgendetwas anderes kommt:
  - Neue Fragen: Q-x mit einer Zeile, oder „keine“
  - Neue Agenten-Entscheidungen: K-x mit einer Zeile, oder „keine“
  - Neue Erkenntnisse: F-x mit einer Zeile, oder „keine“ *(nur mit `FINDINGS.md`)*

  Alles, was der User wissen oder entscheiden muss, steht als Eintrag in den Dateien, nicht nur in der Antwort.
- *(Optional, nur mit `PLAN.md`)* Der Plan wird mit dem User iteriert und dann in Schritte in `TODO.md` überführt. Danach nur bei grundlegenden Kursänderungen anpassen; der laufende Stand steht in `TODO.md`.

- Fortschritt (Checkboxen), neue Entscheidungen und offene Fragen direkt hier pflegen und **immer sofort committen und pushen**, ohne Rückfrage. Vor dem Bearbeiten und vor dem Pushen `git pull --rebase`; Konflikte sofort lösen und dabei die Inhalte beider Seiten behalten.
- Im Code-Repo nie automatisch committen oder pushen, nur auf ausdrückliche Anweisung.
- Jede Frage, Entscheidung und Erkenntnis nennt die Person, von der sie stammt: „Entschieden von: <Name>“ bei D-x, „Erfasst von: <Name>“ bei Q-x und F-x. Erzeugt ein Agent den Eintrag, steht dort der Agent und die Person, für die er arbeitet („Erfasst von: Claude für <Name>“); die Person ergibt sich aus der Sitzung oder `git config user.name`.
- Vor dem Vergeben einer neuen ID (D-, Q-, K-, F-, …) pullen und nach der höchsten vorhandenen weiterzählen.
- Ist ein TODO-Schritt umgesetzt, nur relevante Erkenntnisse notieren (Überraschungen, Abweichungen vom Plan, Entscheidungen mit Folgen). Ohne Auffälligkeiten nur abhaken. `TODO.md` bleibt konkret und schlank.
- Entscheidungen des Users in `DECISIONS.md`, offene Fragen und eigene KI-Entscheidungen in `QUESTIONS.md`. Eine KI-Entscheidung nie als Entscheidung des Users eintragen. `TODO.md` verweist nur per ID.
- *(Optional, nur mit `FINDINGS.md`)* Erkenntnisse (Ursachen, Eigenheiten von Bibliotheken, Messergebnisse, Sackgassen, Gründe für nicht offensichtliche Lösungen) als F-x in `FINDINGS.md`, nicht als Kommentar im Code. Im Code nur Kommentare, die der Code selbst zum Verständnis braucht. `TODO.md` verweist auf die F-x, statt die Erkenntnis zu wiederholen.
- Ist eine Frage geklärt oder eine KI-Entscheidung bestätigt, den Punkt aus `QUESTIONS.md` streichen und in `DECISIONS.md` übernehmen.
- *(Optional, für Teams)* Arbeiten mehrere Personen parallel: Jedes Arbeitspaket bekommt beim Start die Zeile „Umgesetzt von <Name> auf <Code-Branch>“. Abgehakt heißt dann nur: auf diesem Branch erledigt.
- Commit-Format: eine Betreffzeile, kein Body.
- Im Code-Repo (Code, Kommentare, Commits) wird nicht auf diese Dokumente verwiesen.
