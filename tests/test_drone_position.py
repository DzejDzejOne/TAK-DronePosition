import pytest
from pydantic import ValidationError

from main import DronePosition

def test_valid_drone_position():

    drone_data = {
        "uid": "uav_01",
        "callsign": "Drone Alpha",
        "latitude": 45.0,
        "longitude": -75.0,
        "altitude_hae_m": 100.0,
        "aircraft_type": "quadcopter"
    }

    drone = DronePosition(**drone_data)
    assert drone.uid == "uav_01"
    assert drone.callsign == "Drone Alpha"
    assert drone.latitude == 45.0
    assert drone.longitude == -75.0
    assert drone.altitude_hae_m == 100.0
    assert drone.aircraft_type == "quadcopter"

def test_latitiude_cannot_be_greater_than_90():

    drone_data = {
        "uid": "uav_02",
        "callsign": "Drone Beta",
        "latitude": 91.0,
        "longitude": -75.0,
        "altitude_hae_m": 100.0,
        "aircraft_type": "quadcopter"
    }

    with pytest.raises(ValidationError):
        DronePosition(**drone_data)

def test_latitude_cannot_be_less_than_minus_90():

    drone_data = {
        "uid": "uav_02",
        "callsign": "Drone Beta",
        "latitude": 91.0,
        "longitude": -75.0,
        "altitude_hae_m": 100.0,
        "aircraft_type": "quadcopter"
    }
    
    with pytest.raises(ValidationError):
        DronePosition(**drone_data)

def test_longitude_cannot_be_greater_than_180():

    drone_data = {
        "uid": "uav_03",
        "callsign": "Drone Gamma",
        "latitude": 45.0,
        "longitude": 181.0,
        "altitude_hae_m": 100.0,
        "aircraft_type": "quadcopter"
    }

    with pytest.raises(ValidationError):
        DronePosition(**drone_data)

def test_longitude_cannot_be_less_than_minus_180():

    drone_data = {
        "uid": "uav_03",
        "callsign": "Drone Gamma",
        "latitude": 45.0,
        "longitude": -181.0,
        "altitude_hae_m": 100.0,
        "aircraft_type": "quadcopter"
    }

    with pytest.raises(ValidationError):
        DronePosition(**drone_data)

