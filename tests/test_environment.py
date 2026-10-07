import importlib

REQUIRED_MODULES = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pytest",
    "httpx",
    "dotenv"
    "requests"
]

def test_reqired_modules():

    missing_modules = []

    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)

    assert not missing_modules, f"Missing required modules: {', '.join(missing_modules)}"