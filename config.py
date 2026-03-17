import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


class Configs(BaseSettings, extra="allow"):  # type: ignore
    model_bundle: Path = Path("models/research_center_pipeline.pkl")
    logger: logging.Logger = logging.getLogger(__name__)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Configs()
