from dynaconf import Dynaconf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to src/myapp

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        BASE_DIR / "settings.yaml",
        BASE_DIR / "settings.local.yaml",  # Optional
    ],
)
