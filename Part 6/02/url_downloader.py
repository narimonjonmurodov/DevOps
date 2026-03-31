import requests
from image import Image
from pathlib import Path
import asyncio

async def download(image: Image, path: Path, num: int) -> None:
    try:
        response = await asyncio.to_thread(requests.get, image.url)
        response.raise_for_status()

        with open(path / f"image{num}.jpg", "wb") as f:
            f.write(response.content)

        image.success()

    except requests.exceptions.RequestException:
        image.fail()

def check_path(path: str) -> bool:
    path = Path(path)

    if not path.is_dir():
        return False

    try:
        test_file = path / "test.tmp"
        test_file.touch(exist_ok=True)
        test_file.unlink()
        return True

    except (PermissionError, OSError):
        return False