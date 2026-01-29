from __future__ import annotations

from pathlib import Path

from videolib.db_connection import DatabaseConnection
from videolib.schema import initialize_schema


def initialize_database(db_path: str | Path) -> DatabaseConnection:
    connection_manager = DatabaseConnection(db_path)
    connection = connection_manager.get_connection()
    initialize_schema(connection)
    return connection_manager
