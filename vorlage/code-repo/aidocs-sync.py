"""
Hält das Planungs-Repo in ./.aidocs aktuell.

1. Klont ./.aidocs, falls es fehlt.
2. Wechselt dort auf main; alle arbeiten auf main, unabhängig vom Branch im Code-Repo.
3. Holt den aktuellen Stand per pull --rebase, damit eigene, noch nicht gepushte Commits obenauf bleiben.
4. Installiert den post-checkout-Hook, der dieses Skript bei jedem Branchwechsel aufruft.

Die URL des Planungs-Repos wird aus origin abgeleitet (foo.git -> foo-aidocs.git),
außer AIDOCS_URL ist gesetzt.

Fehler (z. B. offline, Konflikt beim Rebase) werden gemeldet, brechen aber nie ab (Exit-Code immer 0).
Nur Python 3 Standardbibliothek.
"""

from pathlib import Path
import re
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent
AIDOCS_DIR = REPO_ROOT / ".aidocs"
AIDOCS_URL = ""  # leer = aus origin ableiten
AIDOCS_BRANCH = "main"
HOOK_MARKER = "aidocs-sync.py"
HOOK_SCRIPT = """#!/bin/sh
# Hält ./.aidocs auf dem aktuellen Stand von main (installiert von aidocs-sync.py).
[ "$3" = "1" ] || exit 0
python3 "$(git rev-parse --show-toplevel)/aidocs-sync.py" 2>/dev/null || python "$(git rev-parse --show-toplevel)/aidocs-sync.py" || true
"""


def git(*args: str, cwd: Path = AIDOCS_DIR) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def log(msg: str):
    print(f"[aidocs] {msg}")


def aidocs_url() -> str:
    if AIDOCS_URL:
        return AIDOCS_URL
    origin = git("remote", "get-url", "origin", cwd=REPO_ROOT).stdout.strip()
    if not origin:
        return ""
    return re.sub(r"(\.git)?/?$", "-aidocs.git", origin, count=1)


def install_hook():
    hooks_dir = Path(git("rev-parse", "--git-path", "hooks", cwd=REPO_ROOT).stdout.strip())
    if not hooks_dir.is_absolute():
        hooks_dir = REPO_ROOT / hooks_dir
    hook = hooks_dir / "post-checkout"
    if hook.exists():
        if HOOK_MARKER not in hook.read_text(encoding="utf-8", errors="replace"):
            log(f"{hook} existiert bereits ohne aidocs-Sync, bitte manuell ergänzen.")
        return
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook.write_text(HOOK_SCRIPT, encoding="utf-8", newline="\n")
    hook.chmod(0o755)
    log(f"post-checkout-Hook installiert: {hook}")


def sync():
    if not AIDOCS_DIR.exists():
        url = aidocs_url()
        if not url:
            log("Keine URL für das Planungs-Repo (kein origin, AIDOCS_URL leer).")
            return
        result = git("clone", url, str(AIDOCS_DIR), cwd=REPO_ROOT)
        if result.returncode != 0:
            log(f"Klonen von {url} fehlgeschlagen: {result.stderr.strip()}")
            return
        log(f"{url} nach {AIDOCS_DIR} geklont.")

    fetch = git("fetch", "--prune", "origin")
    if fetch.returncode != 0:
        log(f"fetch fehlgeschlagen, arbeite mit lokalem Stand: {fetch.stderr.strip()}")

    current = git("symbolic-ref", "--short", "-q", "HEAD").stdout.strip()
    if not current:
        return  # detached HEAD (z. B. während eines Rebase)
    if current != AIDOCS_BRANCH:
        result = git("checkout", AIDOCS_BRANCH)
        if result.returncode != 0:
            log(f"Wechsel von {current} auf {AIDOCS_BRANCH} fehlgeschlagen: {result.stderr.strip()}")
            return
        log(f".aidocs von {current} auf {AIDOCS_BRANCH} gewechselt.")

    if git("rev-parse", "--verify", "-q", "@{upstream}").returncode == 0:
        pull = git("pull", "--rebase", "--autostash", "-q")
        if pull.returncode != 0:
            git("rebase", "--abort")
            log(f"pull --rebase fehlgeschlagen, bitte von Hand zusammenführen: {pull.stderr.strip()}")


if __name__ == "__main__":
    try:
        install_hook()
        sync()
    except Exception as e:  # darf Checkout und Session-Start nie blockieren
        log(f"Fehler: {e}")
    sys.exit(0)
