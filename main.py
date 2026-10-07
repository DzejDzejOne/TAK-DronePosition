from fastapi import FastAPI
from pydantic import BaseModel, Field

from cot_build import build_cot
from send_to_tak import send_to_tak

app = FastAPI()

class Position(BaseModel):
   
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    altitude_hae_m: float = Field(ge=0)

    ce_m: float = Field(ge=0)
    le_m: float = Field(ge=0)

class Motion(BaseModel):

    course_deg: float = Field(ge=0, le=360)
    speed_mps: float = Field(ge=0)
    climb_rate_mps: float

class Status(BaseModel):

    battery_percent: float = Field(ge=0, le=100)
    gps_fix: bool

class Details(BaseModel):

    details: str | None = None

class DronePosition(BaseModel):

    # Identification
    uid: str
    callsign: str
    aircraft_type: str

    position: Position
    motion: Motion
    status: Status
    details: Details = Field(default_factory=Details)

@app.post("/api/v1/uav/position")
def update_position(drone: DronePosition):

    cot = build_cot(drone)

    send_to_tak(cot)

    return {
        "status": "sent",
        "uid": drone.uid
    }