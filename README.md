# Video Library Database

This project implements a normalized SQLite schema and Python services for a
home video library (films, actors, directors). It separates database
connections, schema initialization, read-only compiled queries, and
modification operations.

## Quick start

```bash
python -m videolib_example
```

## Example usage

```python
from pathlib import Path
import datetime as dt

from videolib.app import initialize_database
from videolib.modifications import ModificationService
from videolib.queries import QueryService

connection_manager = initialize_database(Path("videolib.sqlite3"))
connection = connection_manager.get_connection()

modifications = ModificationService(connection)
queries = QueryService(connection)

actor_id = modifications.add_person("Keanu Reeves", dt.date(1964, 9, 2))
film_id = modifications.add_film("John Wick", dt.date(2014, 10, 24), "USA")
modifications.add_actors_to_film(film_id, [actor_id])

recent_films = queries.films_from_current_and_previous_year()
print(queries.iter_rows(recent_films))
```
