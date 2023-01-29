import colorsys
from typing import IO

from PIL import Image
from PIL.Image import Image as TImage

from ._types import Pixel, PixelList


class SortMethod:
    HSV = "HSV"
    HSL = "HSL"


class Roller:
    def __init__(self, filepath: IO) -> None:
        self.filepath = filepath

    def _get_image(self) -> TImage:
        """Open filepath and return Image object."""

        return Image.open(self.filepath).convert("RGB")

    def _get_all_colors(self) -> PixelList:
        """Parse pixels and return a set of all colors."""

        maxsize = (256, 256)
        image = self._get_image()

        # Resize image to skip some colors
        if max(image.size) > max(maxsize):
            image.thumbnail(maxsize, Image.LANCZOS)

        colors = set()
        for x in range(image.width):
            for y in range(image.height):
                colors.add(image.getpixel((x, y)))

        return list(colors)

    def luminosity(self, color: Pixel) -> float:
        """Calculate luminosity of a color."""

        return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

    def _sort_colors(self, colors: PixelList, sorter: str = "HSV") -> PixelList:
        """Sort colors by hue, saturation, and value."""

        if sorter == "HSV":
            return sorted(colors, key=lambda color: colorsys.rgb_to_hsv(*color))

        if sorter == "HSL":
            return sorted(colors, key=lambda color: colorsys.rgb_to_hls(*color))

        if sorter == "LUM":
            return sorted(colors, key=lambda color: self.luminosity(color))

        raise ValueError(f"Invalid sorter type {repr(sorter)}")

    def roll(self, sorter="HSV") -> TImage:
        """Create image of all unique colors in the image passed."""

        colors = self._get_all_colors()
        sorted_colors = self._sort_colors(colors, sorter=sorter)

        height = 100
        image = Image.new("RGB", (len(sorted_colors), height))

        for index, color in enumerate(sorted_colors):
            line = Image.new("RGB", (1, height), color)
            image.paste(line, (index, 0))

        return image
