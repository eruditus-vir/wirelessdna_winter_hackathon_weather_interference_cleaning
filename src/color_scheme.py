from PIL.Image import Image
import numpy as np
from src.utils import rgb2hex


class AemetColorScheme:
    def __init__(self,
                 color_hexes_set):
        self.color_hexes_set = color_hexes_set

    @classmethod
    def from_cropped_image(cls,
                           img: Image):
        img = img.convert('RGB')
        imgarray = np.array(img)
        color_hexes_set = set()
        print(img.size)
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = imgarray[y, x]
                color_hexes_set.add(rgb2hex(r, g, b))
        return AemetColorScheme(color_hexes_set)

    @classmethod
    def from_file_path(cls,
                       file_path: str):
        img = Image.open(file_path)
        return cls.from_cropped_image(img)
