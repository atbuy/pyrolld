import colorsys
from typing import IO

from PIL import Image
from PIL.Image import Image as TImage

from ._types import Pixel, PixelList, Size2D


class SortMethod:
    HSV = "HSV"
    HSL = "HSL"
    YIQ = "YIQ"
    LUM = "LUM"


class Roller:
    def __init__(self, filepath: IO) -> None:
        self.filepath = filepath

    def _get_image(self) -> TImage:
        """Open filepath and return Image object."""

        return Image.open(self.filepath).convert("RGB")

    def _get_all_colors(
        self,
        keep_size: bool = False,
        maxsize: Size2D = (100, 100),
    ) -> PixelList:
        """Parse pixels and return a set of all colors.

        Arguments
        ---------
        keep_size: bool
            Whether to keep the original image size or not.
            Best to keep this False for large images.
        maxsize: Tuple[int, int]
            The size to resize the image to.
            This seems to work best for small sizes e.g. (100, 100).
        """

        image = self._get_image()

        # Resize image to skip some colors
        if not keep_size and max(image.size) > max(maxsize):
            image.thumbnail(maxsize, Image.LANCZOS)

        colors = set()
        for x in range(image.width):
            for y in range(image.height):
                colors.add(image.getpixel((x, y)))

        return list(colors)

    def _luminance(self, color: Pixel) -> float:
        """Calculate luminosity of a color."""

        return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

    def _sort_colors(self, colors: PixelList, sorter: str) -> PixelList:
        """Sort colors by hue, saturation, and value.

        Arguments
        ---------
        colors: list
            List of colors to sort.
        sorter: str
            Type of sorting to use. Can be "HSV", "HSL", "YIQ", "LUM".
        """

        sorter = sorter.upper()

        if sorter == "HSV":
            return sorted(colors, key=lambda color: colorsys.rgb_to_hsv(*color))

        if sorter == "HSL":
            return sorted(colors, key=lambda color: colorsys.rgb_to_hls(*color))

        if sorter == "YIQ":
            return sorted(colors, key=lambda color: colorsys.rgb_to_yiq(*color))

        if sorter == "LUM":
            return sorted(colors, key=lambda color: self._luminance(color))

        raise ValueError(f"Invalid sorter type {repr(sorter)}")

    def roll(
        self,
        sorter="LUM",
        keep_size: bool = False,
        maxsize: Size2D = (100, 100),
    ) -> TImage:
        """Create image of all unique colors in the image passed.

        Arguments
        ---------
        sorter: str
            Type of sorting to use. Can be "HSV", "HSL", "YIQ", "LUM".
        keep_size: bool
            Whether to keep the original image size or not.
            Best to keep this False for large images.
        size: Tuple[int, int]
            The size to resize the image to.
            This seems to work best for small sizes e.g. (100, 100).
        """

        colors = self._get_all_colors(keep_size=keep_size, maxsize=maxsize)
        sorted_colors = self._sort_colors(colors, sorter=sorter)

        height = 100
        image = Image.new("RGB", (len(sorted_colors), height))

        for index, color in enumerate(sorted_colors):
            line = Image.new("RGB", (1, height), color)
            image.paste(line, (index, 0))

        return image
