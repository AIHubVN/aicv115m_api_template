from pathlib import Path


class AssetsConfig:

    ASSETS_PATH = Path("./assets")
    ASSETS_PATH.mkdir(parents=True, exist_ok=True)
    AUDIO_PATH = ASSETS_PATH / "audio"
    AUDIO_PATH.mkdir(parents=True, exist_ok=True)
    META_PATH = ASSETS_PATH / "metadata"
    META_PATH.mkdir(parents=True, exist_ok=True)
