from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from .db import get_connection, initialize_schema


main_bp = Blueprint("main", __name__)


@main_bp.route("/health", methods=["GET"])
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@main_bp.route("/", methods=["GET"])
def index() -> str:
    initialize_schema()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC")
        messages = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template("index.html", messages=messages)


@main_bp.route("/messages", methods=["POST"])
def create_message():
    content = (request.form.get("content") or "").strip()

    if not content:
        return jsonify({"error": "Message content cannot be empty."}), 400

    initialize_schema()

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.index"))
