class Image:
    def __init__(self, url: str):
        self.url: str = url
        self.status: str | None = None

    def success(self):
        self.status: str = "success"

    def fail(self):
        self.status: str = "Error"

    def __str__(self):
        return self.url

def load_image(url: str, images: list[Image]) -> Image:
    image = Image(url)
    images.append(image)
    return image