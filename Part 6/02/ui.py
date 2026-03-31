from prettytable import PrettyTable
from image import Image

def summary(images: list[Image]) -> None:
    table = PrettyTable()
    table.field_names = ["Link", "Status"]
    for image in images:
        table.add_row([image.url, image.status])
    print(table)


