"""SQLite SessionStore adapter for the Claude Agent SDK.

Usage:
    from claude_agent_sdk import ClaudeAgentOptions, query
    from sqlite_session_store import SqliteSessionStore

    store = SqliteSessionStore()          # defaults to "session.db"
    options = ClaudeAgentOptions(session_store=store)
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Optional, Union

from claude_agent_sdk import fold_session_summary

DEFAULT_DB_PATH = "session.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS keys (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    project_key TEXT NOT NULL,
    session_id  TEXT NOT NULL,
    subpath     TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    mtime       INTEGER NOT NULL DEFAULT 0,
    UNIQUE (project_key, session_id, subpath)
);

CREATE TABLE IF NOT EXISTS entries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    key_id     INTEGER NOT NULL
               REFERENCES keys (id) ON DELETE CASCADE,
    uuid       TEXT,
    entry      TEXT NOT NULL CHECK (json_valid(entry)),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS entries_key_idx
ON entries (key_id, id);

CREATE TABLE IF NOT EXISTS summaries (
    key_id     INTEGER PRIMARY KEY
               REFERENCES keys (id) ON DELETE CASCADE,
    summary    TEXT NOT NULL CHECK (json_valid(summary)),
    mtime      INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
"""

# (table, column, DDL) added to databases created by an older version.
_MIGRATIONS = [
    ("keys", "mtime", "ALTER TABLE keys ADD COLUMN mtime INTEGER NOT NULL DEFAULT 0"),
    ("entries", "uuid", "ALTER TABLE entries ADD COLUMN uuid TEXT"),
    ("summaries", "mtime", "ALTER TABLE summaries ADD COLUMN mtime INTEGER NOT NULL DEFAULT 0"),
]

# Created after migrations so the uuid column is guaranteed to exist.
_POST_SCHEMA = """
CREATE UNIQUE INDEX IF NOT EXISTS entries_uuid_uq
ON entries (key_id, uuid) WHERE uuid IS NOT NULL;
"""


class SqliteSessionStore:
    """Implements the Claude Agent SDK ``SessionStore`` protocol on SQLite.

    * ``append`` / ``load`` (required)
    * ``list_sessions``, ``list_session_summaries``, ``delete``,
      ``list_subkeys`` (optional)

    A key is ``{"project_key", "session_id", "subpath"?}``. A missing or empty
    ``subpath`` is the main transcript and is stored as ``''``.

    The SDK's async methods wrap blocking sqlite3 calls in a worker thread; a
    single connection is shared and guarded by a lock.
    """

    def __init__(self, path: Union[str, Path] = DEFAULT_DB_PATH) -> None:
        self.path = str(path)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock, self._conn:
            self._conn.executescript(SCHEMA)
            for table, column, ddl in _MIGRATIONS:
                cols = {r[1] for r in self._conn.execute(f"PRAGMA table_info({table})")}
                if column not in cols:
                    self._conn.execute(ddl)
            self._conn.executescript(_POST_SCHEMA)

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def __enter__(self) -> "SqliteSessionStore":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ---- helpers ---------------------------------------------------------

    @staticmethod
    def _parts(key: dict) -> tuple[str, str, str]:
        return key["project_key"], key["session_id"], key.get("subpath") or ""

    def _find_key_id(self, project_key: str, session_id: str, sub: str) -> Optional[int]:
        row = self._conn.execute(
            "SELECT id FROM keys WHERE project_key = ? AND session_id = ? AND subpath = ?",
            (project_key, session_id, sub),
        ).fetchone()
        return row[0] if row else None

    # ---- required: append / load ----------------------------------------

    async def append(self, key: dict, entries: list[dict]) -> None:
        await asyncio.to_thread(self._append, key, entries)

    def _append(self, key: dict, entries: list[dict]) -> None:
        if not entries:
            return
        project_key, session_id, sub = self._parts(key)
        now_ms = int(time.time() * 1000)
        with self._lock, self._conn:  # one transaction: entries + summary
            self._conn.execute(
                "INSERT INTO keys (project_key, session_id, subpath, mtime) "
                "VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING",
                (project_key, session_id, sub, now_ms),
            )
            key_id = self._find_key_id(project_key, session_id, sub)
            self._conn.execute("UPDATE keys SET mtime = ? WHERE id = ?", (now_ms, key_id))

            # The SDK may re-deliver a batch after a retry, so entries that
            # carry a uuid are de-duplicated (INSERT OR IGNORE + unique index).
            inserted: list[dict] = []
            for e in entries:
                uuid = e.get("uuid") if isinstance(e.get("uuid"), str) else None
                cur = self._conn.execute(
                    "INSERT OR IGNORE INTO entries (key_id, uuid, entry) VALUES (?, ?, ?)",
                    (key_id, uuid, json.dumps(e, ensure_ascii=False)),
                )
                if cur.rowcount:
                    inserted.append(e)

            # Subagent transcripts must not feed the main session's summary.
            if not sub and inserted:
                row = self._conn.execute(
                    "SELECT summary, mtime FROM summaries WHERE key_id = ?", (key_id,)
                ).fetchone()
                prev = (
                    {
                        "session_id": session_id,
                        "mtime": row[1],
                        "data": json.loads(row[0]),
                    }
                    if row
                    else None
                )
                folded = fold_session_summary(prev, key, inserted)
                self._conn.execute(
                    "INSERT INTO summaries (key_id, summary, mtime) VALUES (?, ?, ?) "
                    "ON CONFLICT(key_id) DO UPDATE SET summary = excluded.summary, "
                    "mtime = excluded.mtime, "
                    "updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')",
                    (key_id, json.dumps(folded["data"], ensure_ascii=False), now_ms),
                )

    async def load(self, key: dict) -> Optional[list[dict]]:
        return await asyncio.to_thread(self._load, key)

    def _load(self, key: dict) -> Optional[list[dict]]:
        project_key, session_id, sub = self._parts(key)
        with self._lock:
            key_id = self._find_key_id(project_key, session_id, sub)
            if key_id is None:
                return None
            cur = self._conn.execute(
                "SELECT entry FROM entries WHERE key_id = ? ORDER BY id", (key_id,)
            )
            return [json.loads(r[0]) for r in cur]

    # ---- optional --------------------------------------------------------

    async def list_sessions(self, project_key: str) -> list[dict]:
        return await asyncio.to_thread(self._list_sessions, project_key)

    def _list_sessions(self, project_key: str) -> list[dict]:
        with self._lock:
            cur = self._conn.execute(
                "SELECT session_id, mtime FROM keys "
                "WHERE project_key = ? AND subpath = '' ORDER BY mtime DESC",
                (project_key,),
            )
            return [{"session_id": sid, "mtime": mtime} for sid, mtime in cur]

    async def list_session_summaries(self, project_key: str) -> list[dict]:
        return await asyncio.to_thread(self._list_summaries, project_key)

    def _list_summaries(self, project_key: str) -> list[dict]:
        with self._lock:
            cur = self._conn.execute(
                "SELECT k.session_id, s.mtime, s.summary "
                "FROM summaries s JOIN keys k ON k.id = s.key_id "
                "WHERE k.project_key = ? AND k.subpath = '' ORDER BY s.mtime DESC",
                (project_key,),
            )
            return [
                {"session_id": sid, "mtime": mtime, "data": json.loads(data)}
                for sid, mtime, data in cur
            ]

    async def delete(self, key: dict) -> None:
        await asyncio.to_thread(self._delete, key)

    def _delete(self, key: dict) -> None:
        project_key, session_id, sub = self._parts(key)
        with self._lock, self._conn:
            if sub:
                self._conn.execute(
                    "DELETE FROM keys WHERE project_key = ? AND session_id = ? AND subpath = ?",
                    (project_key, session_id, sub),
                )
            else:  # main key: cascade to every subkey and the summary
                self._conn.execute(
                    "DELETE FROM keys WHERE project_key = ? AND session_id = ?",
                    (project_key, session_id),
                )

    async def list_subkeys(self, key: dict) -> list[str]:
        return await asyncio.to_thread(self._list_subkeys, key)

    def _list_subkeys(self, key: dict) -> list[str]:
        with self._lock:
            cur = self._conn.execute(
                "SELECT subpath FROM keys "
                "WHERE project_key = ? AND session_id = ? AND subpath != '' "
                "ORDER BY subpath",
                (key["project_key"], key["session_id"]),
            )
            return [r[0] for r in cur]