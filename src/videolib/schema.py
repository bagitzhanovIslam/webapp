from __future__ import annotations

import sqlite3


SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_date DATE NOT NULL,
        country TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date DATE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS film_actors (
        film_id INTEGER NOT NULL,
        person_id INTEGER NOT NULL,
        PRIMARY KEY (film_id, person_id),
        FOREIGN KEY (film_id) REFERENCES films (id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS film_directors (
        film_id INTEGER NOT NULL,
        person_id INTEGER NOT NULL,
        PRIMARY KEY (film_id, person_id),
        FOREIGN KEY (film_id) REFERENCES films (id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people (id) ON DELETE CASCADE
    );
    """,
)


def initialize_schema(connection: sqlite3.Connection) -> None:
    """Create normalized schema for films, people, and relations."""
    with connection:
        for statement in SCHEMA_STATEMENTS:
            connection.execute(statement)
