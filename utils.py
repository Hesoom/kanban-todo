from pathlib import Path

ASSETS_PATH = Path(__file__).parent / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)