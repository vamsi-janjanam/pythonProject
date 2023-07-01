import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from crud import create_aircraft, delete_aircraft
from models import Base, Aircraft
from schemas import AircraftCreate, AircraftUpdate


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Override the database dependency to use a test database
def override_get_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def test_create_aircraft():
    client = TestClient(app)
    aircraft_data = {
        "name": "Gulfstream G650",
        "performances": {
            "range": 7000,
            "speed": 956,
        },
        "cabins": {
            "total_interior_length": 53.7
        },
        "systems": {
            "engine": "Rolls-Royce BR725"
        }
    }
    response = client.post("/aircraft/", json=aircraft_data)
    assert response.status_code == 200
    assert response.json()["name"] == aircraft_data["name"]
    assert response.json()["performances"]["range"] == aircraft_data["performances"]["range"]
    assert response.json()["cabins"]["total_interior_length"] == aircraft_data["cabins"]["total_interior_length"]
    assert response.json()["systems"]["engine"] == aircraft_data["systems"]["engine"]
    created_aircraft_id = response.json()["id"]

    # Cleanup: Delete the created aircraft
    with override_get_db() as db:
        delete_aircraft(db, created_aircraft_id)


def test_get_aircraft():
    client = TestClient(app)
    # Create a test aircraft
    with override_get_db() as db:
        aircraft_data = {
            "name": "Gulfstream G650",
            "performances": {
                "range": 7000,
                "speed": 956,
            },
            "cabins": {
                "total_interior_length": 53.7
            },
            "systems": {
                "engine": "Rolls-Royce BR725"
            }
        }
        created_aircraft = create_aircraft(db, AircraftCreate(**aircraft_data))

    # Test retrieving the aircraft
    response = client.get(f"/aircraft/{created_aircraft.id}")
    assert response.status_code == 200
    assert response.json()["name"] == aircraft_data["name"]
    assert response.json()["performances"]["range"] == aircraft_data["performances"]["range"]
    assert response.json()["cabins"]["total_interior_length"] == aircraft_data["cabins"]["total_interior_length"]
    assert response.json()["systems"]["engine"] == aircraft_data["systems"]["engine"]

    # Cleanup: Delete the created aircraft
    with override_get_db() as db:
        delete_aircraft(db, created_aircraft.id)


def test_update_aircraft():
    client = TestClient(app)
    # Create a test aircraft
    with override_get_db() as db:
        aircraft_data = {
            "name": "Gulfstream G650",
            "performances": {
                "range": 7000,
                "speed": 956,
            },
            "cabins": {
                "total_interior_length": 53.7
            },
            "systems": {
                "engine": "Rolls-Royce BR725"
            }
        }
        created_aircraft = create_aircraft(db, AircraftCreate(**aircraft_data))

    # Update the aircraft
    updated_aircraft_data = {
        "name": "Gulfstream G700",
        "performances": {
            "range": 8000,
            "speed": 982,
        },
        "cabins": {
            "total_interior_length": 56.3
        },
        "systems": {
            "engine": "Rolls-Royce Pearl 700"
        }
    }
    response = client.put(f"/aircraft/{created_aircraft.id}", json=updated_aircraft_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_aircraft_data["name"]
    assert response.json()["performances"]["range"] == updated_aircraft_data["performances"]["range"]
    assert response.json()["cabins"]["total_interior_length"] == updated_aircraft_data["cabins"]["total_interior_length"]
    assert response.json()["systems"]["engine"] == updated_aircraft_data["systems"]["engine"]

    # Cleanup: Delete the created aircraft
    with override_get_db() as db:
        delete_aircraft(db, created_aircraft.id)


def test_delete_aircraft():
    client = TestClient(app)
    # Create a test aircraft
    with override_get_db() as db:
        aircraft_data = {
            "name": "Gulfstream G650",
            "performances": {
                "range": 7000,
                "speed": 956,
            },
            "cabins": {
                "total_interior_length": 53.7
            },
            "systems": {
                "engine": "Rolls-Royce BR725"
            }
        }
        created_aircraft = create_aircraft(db, AircraftCreate(**aircraft_data))

    # Delete the aircraft
    response = client.delete(f"/aircraft/{created_aircraft.id}")
    assert response.status_code == 200
    assert response.json()["name"] == aircraft_data["name"]
    assert response.json()["performances"]["range"] == aircraft_data["performances"]["range"]
    assert response.json()["cabins"]["total_interior_length"] == aircraft_data["cabins"]["total_interior_length"]
    assert response.json()["systems"]["engine"] == aircraft_data["systems"]["engine"]

    # Ensure the aircraft is deleted
    response = client.get(f"/aircraft/{created_aircraft.id}")
    assert response.status_code == 404

# Cleanup: Delete the test database file after running the tests
def test_cleanup():
    import os
    os.remove("test.db")

