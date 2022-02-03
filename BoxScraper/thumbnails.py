from PIL.Image import LANCZOS, Image
from pdf2image import convert_from_bytes


def get_thumbnail(file: bytes, max_size: int = 160) -> Image:
    thumb: Image = convert_from_bytes(file, dpi=160)[0]
    width, height = thumb.size

    def scalar(w, h, m):
        ratio = lambda n: round(n / (max(w, h) / m))
        return ratio(w), ratio(h)

    return thumb.resize(size=scalar(width, height, max_size), resample=LANCZOS)
