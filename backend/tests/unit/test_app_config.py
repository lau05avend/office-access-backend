import os

import pytest
from sqlalchemy import inspect as sa_inspect

from app import create_app
from db import init_db
from models import db


@pytest.fixture(autouse=True)
def clear_database_url(monkeypatch):
    """Evita interferencias de variables de entorno reales entre pruebas."""
    for var in [
        "DATABASE_URL",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_NAME",
    ]:
        monkeypatch.delenv(var, raising=False)


def test_create_app_builds_mysql_uri_from_env(monkeypatch):
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASSWORD", "pass")
    monkeypatch.setenv("DB_HOST", "db")
    monkeypatch.setenv("DB_NAME", "office")

    app = create_app({"TESTING": True})

    assert (
        app.config["SQLALCHEMY_DATABASE_URI"]
        == "mysql+pymysql://user:pass@db:3306/office"
    )


def test_create_app_fallbacks_to_sqlite_default():
    app = create_app({"TESTING": True})

    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///visitantes.db"


def test_create_app_respects_explicit_test_config():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///custom.db",
            "SQLALCHEMY_ECHO": False,
        }
    )

    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///custom.db"
    assert app.config["SQLALCHEMY_ECHO"] is False


def test_init_db_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )

    init_db(app)

    with app.app_context():
        inspector = sa_inspect(db.engine)
        assert "visitantes" in inspector.get_table_names()
