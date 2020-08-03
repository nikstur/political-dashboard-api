from configparser import ConfigParser
from pathlib import Path

import typer


def ensure_config() -> ConfigParser:
    config: ConfigParser = ConfigParser()
    config_path: Path = ensure_config_path()
    config.read(config_path)
    return config


def ensure_config_path() -> Path:
    app_dir: Path = Path(typer.get_app_dir("pdactl"))
    app_dir.mkdir(parents=True, exist_ok=True)
    config_path: Path = app_dir / "config"
    return config_path


def write_config(config: ConfigParser) -> None:
    config_path: Path = ensure_config_path()
    with open(config_path, "w") as f:
        config.write(f)
