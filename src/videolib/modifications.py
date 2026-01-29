from __future__ import annotations

import datetime as dt
import sqlite3
from typing import Iterable, Sequence


class ModificationService:
    """Create, update, and delete data in the video library."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add_person(self, full_name: str, birth_date: dt.date) -> int:
        sql = "INSERT INTO people (full_name, birth_date) VALUES (?, ?);"
        with self._connection:
            cursor = self._connection.execute(
                sql, (full_name, birth_date.isoformat())
            )
        return int(cursor.lastrowid)

    def add_film(self, title: str, release_date: dt.date, country: str) -> int:
        sql = "INSERT INTO films (title, release_date, country) VALUES (?, ?, ?);"
        with self._connection:
            cursor = self._connection.execute(
                sql, (title, release_date.isoformat(), country)
            )
        return int(cursor.lastrowid)

    def add_actors_to_film(self, film_id: int, actor_ids: Iterable[int]) -> None:
        sql = "INSERT OR IGNORE INTO film_actors (film_id, person_id) VALUES (?, ?);"
        with self._connection:
            self._connection.executemany(
                sql, [(film_id, actor_id) for actor_id in actor_ids]
            )

    def add_directors_to_film(
        self, film_id: int, director_ids: Sequence[int]
    ) -> None:
        sql = (
            "INSERT OR IGNORE INTO film_directors (film_id, person_id) "
            "VALUES (?, ?);"
        )
        with self._connection:
            self._connection.executemany(
                sql, [(film_id, director_id) for director_id in director_ids]
            )

    def delete_films_older_than(self, years: int) -> int:
        cutoff = dt.date.today() - dt.timedelta(days=years * 365)
        sql = "DELETE FROM films WHERE release_date < ?;"
        with self._connection:
            cursor = self._connection.execute(sql, (cutoff.isoformat(),))
        return cursor.rowcount
