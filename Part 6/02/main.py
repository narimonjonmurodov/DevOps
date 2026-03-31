from image import Image, load_image
from url_downloader import check_path, download
from pathlib import Path
from ui import summary
import asyncio

async def main():
    images: list[Image] = []
    path = input("Enter path :").strip()

    while True:
        if path == "":
            return
        elif not check_path(path):
            print("Path is not valid, Try again.")
            path = input("Enter path :").strip()
        else:
            break

    tasks = []
    num = 0
    while True:
        url = input("url:").strip()
        if url == "":
            break
        image = load_image(url, images)
        task = asyncio.create_task(download(image, Path(path), num))
        tasks.append(task)
        num += 1

    if tasks:
        print("Waiting for downloads to complete...")
        await asyncio.gather(*tasks)

    summary(images)

if __name__ == "__main__":
    asyncio.run(main())