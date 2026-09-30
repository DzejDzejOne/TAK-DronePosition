from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

def iso_time(dt):
    return (
        dt.isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

def build_cot(drone):

    now = datetime.now(timezone.utc)
    stale = now + timedelta(seconds=2)

    event = ET.Element(
        "event", 
        {
            "version": "2.0",
            "uid": drone.uid,

            "type": "COT_TYPE",

            "time": iso_time(now),
            "start": iso_time(now),
            "stale": iso_time(stale),
            "how": "h-e"
        }
    )
    ET.SubElement(event, "point", 
                  {
                      "lat": str(drone.latitude),
                      "lon": str(drone.longitude),
                      "hae": str(drone.altitude_hae_m),
                      "ce": "1",
                      "le": "1"
                  }
    )

    detail = ET.SubElement(event, "detail")

    ET.SubElement(detail, "contact", {"callsign": drone.callsign})

    return ET.tostring(
        event, 
        encoding="unicode"
        )