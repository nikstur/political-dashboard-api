import pytest
from api.database import DataBase
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@pytest.mark.parametrize("setenv", [("true"), ("false")])
def test_init(monkeypatch, setenv):
    if setenv:
        monkeypatch.setenv("DB_HOSTNAME", "db")
    else:
        monkeypatch.delenv("DB_HOSTNAME", raising=False)
    database = DataBase()
    assert database.hostname == "db"


def test_connect(monkeypatch):
    monkeypatch.setenv("DB_HOSTNAME", "db")
    database = DataBase()
    database.connect()
    assert isinstance(database.client, AsyncIOMotorClient)
    assert isinstance(database.db, AsyncIOMotorDatabase)


def test__get_client(monkeypatch):
    monkeypatch.setenv("DB_HOSTNAME", "db")
    database = DataBase()
    database._get_client()
    assert isinstance(database.client, AsyncIOMotorClient)


def test__get_db(monkeypatch):
    monkeypatch.setenv("DB_HOSTNAME", "db")
    database = DataBase()
    database._get_client()
    database._get_db()
    assert isinstance(database.db, AsyncIOMotorDatabase)
    assert database.db.name == "database"
