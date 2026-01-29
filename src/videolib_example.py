from __future__ import annotations

import datetime as dt
from pathlib import Path

from videolib.app import initialize_database
from videolib.modifications import ModificationService
from videolib.queries import QueryService


def main() -> None:
    connection_manager = initialize_database(Path("videolib.sqlite3"))
    connection = connection_manager.get_connection()

    modifications = ModificationService(connection)
    queries = QueryService(connection)

    actor_id = modifications.add_person("Keanu Reeves", dt.date(1964, 9, 2))
    director_id = modifications.add_person("Chad Stahelski", dt.date(1968, 9, 20))
    film_id = modifications.add_film("John Wick", dt.date(2014, 10, 24), "USA")
    modifications.add_actors_to_film(film_id, [actor_id])
    modifications.add_directors_to_film(film_id, [director_id])

    recent_films = queries.films_from_current_and_previous_year()
    print("Recent films:", queries.iter_rows(recent_films))
    print("Actors for John Wick:", queries.iter_rows(queries.actors_for_film("John Wick")))
    print(
        "Actors in at least 1 film:",
        queries.iter_rows(queries.actors_in_at_least_n_films(1)),
    )
    print("Actors who are directors:", queries.iter_rows(queries.actors_who_are_directors()))


if __name__ == "__main__":
    main()
