import os
import time
from typing import Any

import mysql.connector
from mysql.connector import Error


MAX_RETRIES = int(os.getenv("DB_CONNECT_RETRIES", "15"))
RETRY_DELAY_SECONDS = float(os.getenv("DB_RETRY_DELAY_SECONDS", "2"))


def _db_config() -> dict[str, Any]:
    return {
        "host": os.getenv("DB_HOST", "db"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "database": os.getenv("DB_NAME", "appdb"),
        "user": os.getenv("DB_USER", "appuser"),
        "password": os.getenv("DB_PASSWORD", "apppassword"),
    }


def get_connection() -> Any:
    config = _db_config()
    last_error: Error | None = None

    for _ in range(MAX_RETRIES):
        try:
            return mysql.connector.connect(**config)
        except Error as exc:
            last_error = exc
            time.sleep(RETRY_DELAY_SECONDS)

    if last_error is None:
        raise RuntimeError("Failed to connect to MySQL for unknown reason.")

    raise RuntimeError(f"Could not connect to MySQL after retries: {last_error}")


def initialize_schema() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()
