import math
import time
import requests


API_URL = "http://127.0.0.1:8000/api/v1/uav/position"

CENTER_LAT = 52.37177
CENTER_LON = 20.65703

RADIUS_M = 150.0
ALTITUDE_M = 120.0

UPDATE_INTERVAL_S = 1.0
ANGULAR_SPEED_DEG = 10.0   # ile stopni na sekundę


def meters_to_lat_lon(center_lat, east_m, north_m):
    lat_deg_per_m = 1 / 111320
    lon_deg_per_m = 1 / (111320 * math.cos(math.radians(center_lat)))

    dlat = north_m * lat_deg_per_m
    dlon = east_m * lon_deg_per_m

    return center_lat + dlat, CENTER_LON + dlon


def build_drone_payload(uid, callsign, lat, lon, altitude, course_deg):
    return {
        "uid": uid,
        "callsign": callsign,
        "latitude": lat,
        "longitude": lon,
        "altitude_hae_m": altitude,
        "aircraft_type": "quadcopter",
        "speed_mps": 12.0,
        "course_deg": course_deg,
        "battery_percent": 90
    }


def send_drone(payload):
    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def main():
    angle_deg = 0.0

    drones = [
        {"uid": "uav-001", "callsign": "DRONE-ALFA", "phase_deg": 0.0},
        {"uid": "uav-002", "callsign": "DRONE-BRAVO", "phase_deg": 120.0},
        {"uid": "uav-003", "callsign": "DRONE-CHARLIE", "phase_deg": 240.0},
    ]

    print("Start generatora 3 dronów. Ctrl+C aby zatrzymać.")

    while True:
        for drone in drones:
            current_angle_deg = angle_deg + drone["phase_deg"]
            current_angle_rad = math.radians(current_angle_deg)

            east_m = RADIUS_M * math.cos(current_angle_rad)
            north_m = RADIUS_M * math.sin(current_angle_rad)

            lat, lon = meters_to_lat_lon(
                CENTER_LAT,
                east_m,
                north_m
            )

            # Kurs styczny do okręgu
            course_deg = (current_angle_deg + 90.0) % 360.0

            payload = build_drone_payload(
                uid=drone["uid"],
                callsign=drone["callsign"],
                lat=lat,
                lon=lon,
                altitude=ALTITUDE_M,
                course_deg=course_deg
            )

            try:
                result = send_drone(payload)
                print(
                    f"{drone['callsign']} -> "
                    f"lat={lat:.6f}, lon={lon:.6f}, "
                    f"response={result}"
                )
            except Exception as error:
                print(f"Błąd dla {drone['callsign']}: {error}")

        angle_deg = (angle_deg + ANGULAR_SPEED_DEG) % 360.0
        time.sleep(UPDATE_INTERVAL_S)


if __name__ == "__main__":
    main()