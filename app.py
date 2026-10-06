import os
import logging

from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from flask import Flask, request


load_dotenv()

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

def get_db_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row
    )


@app.get("/")
def home():
    return {"message": "Student API is running"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}

@app.get("/api/v1/students")
def get_students():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students ORDER BY id")
            students = cursor.fetchall()

    return students
import os
import logging

from dotenv import load_dotenv

import psycopg
from psycopg.rows import dict_row
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row
    )


@app.get("/")
def home():
    return {"message": "Student API is running"}


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


@app.get("/api/v1/students")
def get_students():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students ORDER BY id")
            students = cursor.fetchall()

    return students


@app.get("/api/v1/students/<int:student_id>")
def get_student(student_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM students WHERE id = %s",
                (student_id,)
            )
            student = cursor.fetchone()

    if student is None:
        logger.warning("Student not found: id=%s", student_id)
        return {"error": "Student not found"}, 404

    return student


@app.post("/api/v1/students")
def create_student():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("course"):
        return {"error": "name and course are required"}, 400

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO students (name, course)
                VALUES (%s, %s)
                RETURNING *
                """,
                (data["name"], data["course"])
            )
            new_student = cursor.fetchone()

    logger.info(
        "Student created: id=%s name=%s course=%s",
        new_student["id"],
        new_student["name"],
        new_student["course"]
    )

    return new_student, 201


@app.put("/api/v1/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json()

    if not data or not data.get("name") or not data.get("course"):
        return {"error": "name and course are required"}, 400

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE students
                SET name = %s, course = %s
                WHERE id = %s
                RETURNING *
                """,
                (data["name"], data["course"], student_id)
            )
            updated_student = cursor.fetchone()

    if updated_student is None:
        logger.warning("Student not found for update: id=%s", student_id)
        return {"error": "Student not found"}, 404

    logger.info(
        "Student updated: id=%s name=%s course=%s",
        updated_student["id"],
        updated_student["name"],
        updated_student["course"]
    )

    return updated_student


@app.patch("/api/v1/students/<int:student_id>")
def patch_student(student_id):
    data = request.get_json()

    if not data:
        return {"error": "Request body is required"}, 400

    allowed_fields = {"name", "course"}

    if not data.keys() & allowed_fields:
        return {
            "error": "At least one field (name or course) is required"
        }, 400

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM students WHERE id = %s",
                (student_id,)
            )
            student = cursor.fetchone()

            if student is None:
                logger.warning(
                    "Student not found for patch: id=%s",
                    student_id
                )
                return {"error": "Student not found"}, 404

            name = data.get("name", student["name"])
            course = data.get("course", student["course"])

            if not name or not course:
                return {
                    "error": "name and course cannot be empty"
                }, 400

            cursor.execute(
                """
                UPDATE students
                SET name = %s, course = %s
                WHERE id = %s
                RETURNING *
                """,
                (name, course, student_id)
            )
            updated_student = cursor.fetchone()

    logger.info(
        "Student patched: id=%s name=%s course=%s",
        updated_student["id"],
        updated_student["name"],
        updated_student["course"]
    )

    return updated_student


@app.delete("/api/v1/students/<int:student_id>")
def delete_student(student_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )
            deleted = cursor.rowcount

    if deleted == 0:
        logger.warning("Student not found for deletion: id=%s", student_id)
        return {"error": "Student not found"}, 404

    logger.info("Student deleted: id=%s", student_id)

    return {"message": "Student deleted successfully"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
