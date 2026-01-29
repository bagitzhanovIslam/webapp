from __future__ import annotations

import datetime as dt
import sqlite3
from typing import Iterable


class QueryService:
    """Run compiled (parameterized) read-only queries."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def films_from_current_and_previous_year(self) -> list[sqlite3.Row]:
        current_year = dt.date.today().year
        previous_year = current_year - 1
        sql = (
            "SELECT id, title, release_date, country "
            "FROM films "
            "WHERE strftime('%Y', release_date) IN (?, ?) "
            "ORDER BY release_date DESC;"
        )
        return list(
            self._connection.execute(
                sql, (str(current_year), str(previous_year))
            ).fetchall()
        )

    def actors_for_film(self, film_title: str) -> list[sqlite3.Row]:
        sql = (
            "SELECT p.id, p.full_name, p.birth_date "
            "FROM people AS p "
            "JOIN film_actors AS fa ON fa.person_id = p.id "
            "JOIN films AS f ON f.id = fa.film_id "
            "WHERE f.title = ? "
            "ORDER BY p.full_name;"
        )
        return list(self._connection.execute(sql, (film_title,)).fetchall())

    def actors_in_at_least_n_films(self, minimum_films: int) -> list[sqlite3.Row]:
        sql = (
            "SELECT p.id, p.full_name, p.birth_date, COUNT(*) AS film_count "
            "FROM people AS p "
            "JOIN film_actors AS fa ON fa.person_id = p.id "
            "GROUP BY p.id, p.full_name, p.birth_date "
            "HAVING COUNT(*) >= ? "
            "ORDER BY film_count DESC, p.full_name;"
        )
        return list(self._connection.execute(sql, (minimum_films,)).fetchall())

    def actors_who_are_directors(self) -> list[sqlite3.Row]:
        sql = (
            "SELECT DISTINCT p.id, p.full_name, p.birth_date "
            "FROM people AS p "
            "WHERE EXISTS (SELECT 1 FROM film_actors fa WHERE fa.person_id = p.id) "
            "AND EXISTS (SELECT 1 FROM film_directors fd WHERE fd.person_id = p.id) "
            "ORDER BY p.full_name;"
        )
        return list(self._connection.execute(sql).fetchall())

    def iter_rows(self, rows: Iterable[sqlite3.Row]) -> list[dict[str, str]]:
        return [dict(row) for row in rows]
