from datetime import datetime, timezone
from types import SimpleNamespace
import xml.etree.ElementTree as ET

from cot_build import build_cot, iso_time

def test_iso_time():
    dt = datetime(
        2026,
        9,
        30,
        12,
        49,
        50,
        123000,
        tzinfo=timezone.utc
    )

    assert iso_time(dt) == "2026-09-30T12:49:50.123Z"

def test_build_cot_return_valid_xml():
    
    drone = SimpleNamespace(
        uid="uav-01",
        callable="Matylda",
        latitude=52.2297,
        longitude=21.0122,
        altitude_hae_m=120.0
        )

    cot = build_cot(drone)

    xml = ET.fromstring(str)

    assert xml.tag == "event"
    assert xml.attrib["version"] == "2.0"
    assert xml.attrib["uid"] == "uav-01"
    assert xml.attrib["callable"] == "Matylda"
    assert xml.attrib["how"] == "h-e"

def test_build_cot_create_correct_point():

    drone = SimpleNamespace(
            uid="uav-01",
            callable="Matylda",
            latitude=52.2297,
            longitude=21.0122,
            altitude_hae_m=120.0
            )

    cot = cot_build(drone)

    xml = ET.fromstring(cot)

    point = xml.find("point")

    assert point is not None

    assert point.attrib["lat"] == "52.2297"
    assert point.attrib["hae"] == "21.0122"
    assert point.attrib["hae"] == "120.0"
    assert point.attrib["ce"] == "1"
    assert point.attrib["le"] == "1"

def test_build_cot_has_correct_callsign():

    drone = SimpleNamespace(
        uid="uav-001",
        callsign="Matylda",
        latitude=52.2297,
        longitude=21.0122,
        altitude_hae_m=120.0
    )

    cot = build_cot(drone)

    xml = ET.fromstring(cot)

    contact = xml.find("./detail/contact")

    assert contact is not None
    assert contact.attrib["callsign"] == "Matylda"