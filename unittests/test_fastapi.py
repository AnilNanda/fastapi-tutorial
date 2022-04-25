from xmlrpc import client

from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_path():
    resp = client.get("/")
    print(resp.json().get('message'))
    assert resp.json().get('message') == 'Hello World!'
    assert resp.status_code == 200

def test_create_user():
    res = client.post("/users/",json={"email": "hello123@west.com","password": "pass1234"})
    print(res.json())
    assert res.json().get("email") == "hello123@west.com"
    assert res.status_code == 200