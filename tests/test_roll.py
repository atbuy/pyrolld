import io
from unittest import TestCase

import pytest
from PIL import Image
from PIL.Image import Image as TImage

from rolld import Roller

RED = Image.new("RGB", (100, 100), (255, 0, 0))
GREEN = Image.new("RGB", (100, 100), (0, 255, 0))
BLUE = Image.new("RGB", (100, 100), (0, 0, 255))

# Stack images horizontally to create a 3x100 image
STACKED = Image.new("RGB", (300, 100))
STACKED.paste(RED, (0, 0))
STACKED.paste(GREEN, (100, 0))
STACKED.paste(BLUE, (200, 0))


def mock_image(image: TImage):
    """Create a mock image object"""

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    return image_bytes


class RollTest(TestCase):
    def test_roll(self):
        """Test size of output image"""

        mock = mock_image(STACKED)
        image = Roller(mock).roll()

        self.assertEqual(image.size, (9, 100))

        pixel_blue = image.getpixel((0, 50))
        pixel_red = image.getpixel((2, 50))
        pixel_green = image.getpixel((8, 50))

        self.assertEqual(pixel_red, (255, 0, 0))
        self.assertEqual(pixel_green, (0, 255, 0))
        self.assertEqual(pixel_blue, (0, 0, 255))

    def test_sorter_hsv(self):
        """Test HSV sorter"""

        mock = mock_image(STACKED)
        image = Roller(mock).roll(sorter="HSV")

        pixel_red = image.getpixel((0, 50))
        pixel_green = image.getpixel((4, 50))
        pixel_blue = image.getpixel((8, 50))

        self.assertEqual(pixel_red, (255, 0, 0))
        self.assertEqual(pixel_green, (0, 255, 0))
        self.assertEqual(pixel_blue, (0, 0, 255))

    def test_sorter_hsl(self):
        """Test HSL sorter"""

        mock = mock_image(STACKED)
        image = Roller(mock).roll(sorter="HSL")

        pixel_red = image.getpixel((0, 50))
        pixel_green = image.getpixel((4, 50))
        pixel_blue = image.getpixel((8, 50))

        self.assertEqual(pixel_red, (255, 0, 0))
        self.assertEqual(pixel_green, (0, 255, 0))
        self.assertEqual(pixel_blue, (0, 0, 255))

    def test_sorter_yiq(self):
        """Test YIQ sorter"""

        mock = mock_image(STACKED)
        image = Roller(mock).roll(sorter="YIQ")

        pixel_blue = image.getpixel((0, 50))
        pixel_red = image.getpixel((2, 50))
        pixel_green = image.getpixel((8, 50))

        self.assertEqual(pixel_red, (255, 0, 0))
        self.assertEqual(pixel_green, (0, 255, 0))
        self.assertEqual(pixel_blue, (0, 0, 255))

    def test_sorter_lum(self):
        """Test luminosity sorter"""

        mock = mock_image(STACKED)
        image = Roller(mock).roll(sorter="LUM")

        pixel_blue = image.getpixel((0, 50))
        pixel_red = image.getpixel((2, 50))
        pixel_green = image.getpixel((8, 50))

        self.assertEqual(pixel_red, (255, 0, 0))
        self.assertEqual(pixel_green, (0, 255, 0))
        self.assertEqual(pixel_blue, (0, 0, 255))

    def test_no_sorter(self):
        """Test no sorter"""

        mock = mock_image(STACKED)
        with pytest.raises(ValueError) as excinfo:
            Roller(mock).roll(sorter="")
            self.assertIn("Invalid sorter type", str(excinfo.value))
