from faker import Faker
from time import perf_counter
import sys
import os

# Добавляем src в путь для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def load():
    from error import Duplicate
    from data.explorer import create
    from model.explorer import Explorer

    f = Faker()
    NUM = 100_000
    DUPLICATE_NUM = 0
    t1 = perf_counter()
    for row in range(NUM):
        try:
            create(
                Explorer(name=f.name(), country=f.country(), description=f.text()[:100])
            )
        except Duplicate:
            DUPLICATE_NUM += 1
    t2 = perf_counter()
    print(NUM - DUPLICATE_NUM, "rows")
    print("write time:", t2 - t1)


def read_db():
    from data.explorer import get_all

    t1 = perf_counter()
    _ = get_all()
    t2 = perf_counter()
    print("db read time:", t2 - t1)


def read_api():
    from fastapi.testclient import TestClient
    from main import app

    t1 = perf_counter()
    client = TestClient(app)
    _ = client.get("/explorer/")
    t2 = perf_counter()
    print("api read time:", t2 - t1)


load()
read_db()
read_db()
read_api()
