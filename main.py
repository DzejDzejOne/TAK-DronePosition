from fastapi import FastAPI
from pydantic import BaseModel, Field

from cot_build import build_cot
from send_to_tak import send_to_tak

app = FastAPI()

class DronePosition(BaseModel):

    uid: str
    callsign: str

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    altitude_hae_m: float

    aircraft_type: str

@app.post("/api/v1/uav/position")
def update_position(drone: DronePosition):

    cot = build_cot(drone)

    send_to_tak(cot)

    return {
        "status": "sent",
        "uid": drone.uid
    }