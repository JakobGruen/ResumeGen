from pathlib import Path
import json


def load_json(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        with open(path, "r") as f:
            user_data = json.load(f)
    else:
        raise ValueError(f"Invalid file: {path} \nInput file must be a JSON file.")
    return user_data


def save_html(content: str, path: str | None = None) -> Path:

    if path is None:
        # Default to the data directory
        path = Path(__file__).parent.parent / "data" / "content.html"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
