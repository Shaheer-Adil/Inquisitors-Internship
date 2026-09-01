import sqlite3
import re
from pathlib import Path
from .config import settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "memory" / "chatbot.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS user_memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        fact TEXT NOT NULL,
        category TEXT NOT NULL,
        last_confirmed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, fact, category)
    )""")
    c.commit()
    return c


def get_history(session_id):
    c = _conn()
    rows = c.execute(
        """SELECT role,content FROM messages
           WHERE session_id=? ORDER BY id DESC LIMIT ?""",
        (session_id, settings.max_history_messages),
    ).fetchall()
    c.close()
    return [{"role": r, "content": x} for r, x in reversed(rows)]


def append(session_id, role, content):
    c = _conn()
    c.execute(
        "INSERT INTO messages(session_id,role,content) VALUES(?,?,?)",
        (session_id, role, content),
    )
    c.commit()
    c.close()


def get_long_term_memory(user_id, limit=20):
    """Return only explicitly stored, appropriate long-term facts."""
    c = _conn()
    rows = c.execute(
        """SELECT fact, category, last_confirmed_at
           FROM user_memory WHERE user_id=?
           ORDER BY last_confirmed_at DESC LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    c.close()
    return [
        {"fact": fact, "category": category, "last_confirmed_at": confirmed}
        for fact, category, confirmed in rows
    ]


def save_memory(user_id, fact, category):
    """Store a small, explicitly appropriate fact outside the public RAG corpus."""
    fact = fact.strip()
    category = category.strip()
    if not user_id or not fact or not category:
        return
    c = _conn()
    c.execute(
        """INSERT INTO user_memory(user_id,fact,category) VALUES(?,?,?)
           ON CONFLICT(user_id,fact,category) DO UPDATE SET
           last_confirmed_at=CURRENT_TIMESTAMP""",
        (user_id, fact, category),
    )
    c.commit()
    c.close()


def maybe_save_explicit_language_preference(user_id, message, language):
    """Persist only an explicitly requested response language.

    Language-request phrases can themselves be written in English, so the
    classifier's detected input language must not be used as the preference.
    """
    lower = message.lower().strip()
    requested_language = None

    if (
        "reply in roman urdu" in lower
        or "respond in roman urdu" in lower
        or "speak in roman urdu" in lower
        or "use roman urdu" in lower
    ):
        requested_language = "Roman Urdu"
    elif "reply in english" in lower or "respond in english" in lower or "speak in english" in lower:
        requested_language = "English"
    elif "reply in urdu" in lower or "respond in urdu" in lower or "speak in urdu" in lower:
        requested_language = "Urdu"

    if requested_language:
        save_memory(user_id, f"User prefers {requested_language} responses.", "language_preference")
def maybe_save_explicit_name(user_id, message):
    """Persist a user's name only when explicitly stated."""
    import re

    lower = message.lower().strip()

    patterns = [
        r"\bmy name is\s+([A-Za-z][A-Za-z .'-]{0,79}?)(?:[.!?]|$)",
        r"\bplease remember that my name is\s+([A-Za-z][A-Za-z .'-]{0,79}?)(?:[.!?]|$)",
        r"\bremember my name is\s+([A-Za-z][A-Za-z .'-]{0,79}?)(?:[.!?]|$)",
        r"\byou can call me\s+([A-Za-z][A-Za-z .'-]{0,79}?)(?:[.!?]|$)",
    ]

    name = None

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            break

    if name:
        name = re.sub(r"\s+", " ", name).strip(" .,!?:;")
        if name:
            save_memory(user_id, f"User's name is {name}.", "name")

def delete_user_memory(user_id):
    """Delete long-term memory for a user/session without touching public RAG."""
    c = _conn()
    c.execute("DELETE FROM user_memory WHERE user_id=?", (user_id,))
    deleted = c.rowcount
    c.commit()
    c.close()
    return deleted
