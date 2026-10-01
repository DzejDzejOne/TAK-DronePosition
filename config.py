import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR/".env"

load_dotenv(ENV_FILE)

def get_required_env(name: str) -> str:

    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Missing required variable: {name}"
        )

    return value

# Server variable

TAK_HOST = get_required_env("TAK_HOST")

TAK_PORT = os.getenv("TAK_PORT", "8089")

# CERTIFICATES

CA_FILE = Path(
    get_required_env("CA_FILE")
).expanduser()

CERT_FILE = Path(
    get_required_env("CERT_FILE")
).expanduser()

KEY_FILE = Path(
    get_required_env("KEY_FILE")
).expanduser()

# CERTIFICATES VALIDATION

def validate_config():

    files = {
        "CA_FILE": CA_FILE,
        "CERT_FILE": CERT_FILE,
        "KEY_FILE": KEY_FILE,
    }

    for name, path in files.items():

        if not path.is_file():

            raise FileNotFoundError(
                f"{name}: FILE NOT FIND: {path}"
            )