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

            "type": "a-f-A",

            "time": iso_time(now),
            "start": iso_time(now),
            "stale": iso_time(stale),
            "how": "h-e"
        }
    )
    ET.SubElement(event, "point", 
                  {
                      "lat": str(drone.position.latitude),
                      "lon": str(drone.position.longitude),
                      "hae": str(drone.position.altitude_hae_m),
                      "ce": str(drone.position.ce_m),
                      "le": str(drone.position.le_m)
                  }
    )
    ET.SubElement(event, "track",
                  {
                      "course": str(drone.motion.course_deg),
                      "speed": str(drone.motion.speed_mps),
                      "climb_rate": str(drone.motion.climb_rate_mps)
                  }
    )
    detail = ET.SubElement(event, "detail")

    ET.SubElement(detail, "contact", {"callsign": drone.callsign})
    
    ET.SubElement(
    detail,
    "status",
    {
        "battery": str(drone.status.battery_percent)
        #"gps_fix": bool(drone.status.gps_fix)
    }
    )

    if drone.details.remarks:
        remarks = ET.SubElement(detail, "remarks")
        remarks.text = drone.details.remarks
        
    return ET.tostring(
        event, 
        encoding="unicode"
        )