# Student API

A simple REST API built with Flask and PostgreSQL for managing student records.

## Features

- Create a student
- Get all students
- Get a student by ID
- Update a student
- Partially update a student
- Delete a student
- Healthcheck endpoint
- Database migrations
- API request and response logging
- Automated tests
- OpenAPI specification

## Tech Stack

- Python 3
- Flask
- PostgreSQL
- Psycopg
- Pytest
- PyYAML

## Project Structure

```text
student-api/
├── app.py
├── migrate.py
├── requirements.txt
├── Makefile
├── openapi.yaml
├── migrations/
│   └── 001_create_students.sql
├── tests/
│   └── test_students.py
└── .gitignore
