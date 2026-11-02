"""
Flask Backend
-------------
Receives form submissions from the Express frontend, validates and
processes the data, and returns a JSON response.
"""
import os
import re
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow browser requests from the frontend if ever called directly

# In-memory store (resets when the container restarts)
submissions = []

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate(data):
    """Return a list of validation error messages (empty list = valid)."""
    errors = []
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    age = str(data.get("age") or "").strip()
    course = (data.get("course") or "").strip()

    if len(name) < 2:
        errors.append("Name must be at least 2 characters long.")
    if not EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")
    if not age.isdigit() or not (1 <= int(age) <= 120):
        errors.append("Age must be a number between 1 and 120.")
    if not course:
        errors.append("Please select a course.")
    return errors


@app.route("/")
def home():
    return jsonify({"service": "flask-backend", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/submit", methods=["POST"])
def submit():
    # Accept both JSON and classic form-encoded bodies
    data = request.get_json(silent=True) or request.form.to_dict()

    errors = validate(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    record = {
        "id": len(submissions) + 1,
        "name": data["name"].strip().title(),
        "email": data["email"].strip().lower(),
        "age": int(str(data["age"]).strip()),
        "course": data["course"].strip(),
        "message": (data.get("message") or "").strip(),
        "received_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    submissions.append(record)
    app.logger.info("New submission #%s from %s", record["id"], record["email"])

    return jsonify({
        "success": True,
        "message": f"Hello {record['name']}! Your registration for {record['course']} was received successfully.",
        "data": record,
    }), 201


@app.route("/submissions", methods=["GET"])
def list_submissions():
    return jsonify({"count": len(submissions), "submissions": submissions})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
