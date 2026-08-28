from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# Create the Flask application.
app = Flask(__name__)

# Store the SQLite database beside this Python file.
DATABASE = Path(__file__).with_name("visitors.db")


def get_db():
    # Open a connection to the local SQLite database.
    connection = sqlite3.connect(DATABASE)

    # Return rows as dictionary-like objects when needed.
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    # Create the visitors table if it does not already exist.
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visited_at TEXT NOT NULL,
                user_agent TEXT,
                language TEXT,
                platform TEXT,
                screen_width INTEGER,
                screen_height INTEGER,
                timezone TEXT,
                referrer TEXT
            )
            """
        )

        # Save the schema changes.
        db.commit()


@app.post("/api/visit")
def record_visit():
    # Accept only JSON telemetry from the consent dialog on the website.
    data = request.get_json(silent=True) or {}

    # Read only the fields that the frontend explicitly sends.
    user_agent = str(data.get("user_agent", ""))[:1000]
    language = str(data.get("language", ""))[:100]
    platform = str(data.get("platform", ""))[:100]
    timezone_name = str(data.get("timezone", ""))[:100]
    referrer = str(data.get("referrer", ""))[:2000]

    # Validate screen dimensions so arbitrary data is not stored.
    try:
        screen_width = int(data.get("screen_width", 0))
        screen_height = int(data.get("screen_height", 0))
    except (TypeError, ValueError):
        screen_width = 0
        screen_height = 0

    # Clamp the values to reasonable browser-screen ranges.
    screen_width = max(0, min(screen_width, 10000))
    screen_height = max(0, min(screen_height, 10000))

    # Record the current server-side UTC timestamp.
    visited_at = datetime.now(timezone.utc).isoformat()

    # Insert the consented telemetry into SQLite.
    with get_db() as db:
        db.execute(
            """
            INSERT INTO visitors (
                visited_at,
                user_agent,
                language,
                platform,
                screen_width,
                screen_height,
                timezone,
                referrer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                visited_at,
                user_agent,
                language,
                platform,
                screen_width,
                screen_height,
                timezone_name,
                referrer,
            ),
        )

        # Commit the new visitor record.
        db.commit()

    # Return a small success response.
    return jsonify({"ok": True})


@app.get("/api/visitors")
def list_visitors():
    # Return recent records so the site owner can inspect the database.
    with get_db() as db:
        rows = db.execute(
            """
            SELECT *
            FROM visitors
            ORDER BY id DESC
            LIMIT 100
            """
        ).fetchall()

    # Convert SQLite rows into ordinary JSON-compatible dictionaries.
    return jsonify([dict(row) for row in rows])


# Initialize the database when the application starts.
init_db()


if __name__ == "__main__":
    # Run the development server locally.
    app.run(host="127.0.0.1", port=5000, debug=True)
