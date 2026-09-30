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