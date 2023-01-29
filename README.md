# pyrolld

A package to generate color sequences from videos and images

Its main use is to create a set of unique colors from an image and then
sort the colors according to the selected sorting method.

## Installation

You can simply pip install this package:

```bash
pip install pyrolld
```

## Usage

Here is an example:

```python
from rolld import Roller


filepath = "image.png"
image = Roller(filepath)
rolled = image.roll()

rolled.show()
```

You can also chose between 3 different sorting methods `["HSV", "HSL", "LUM"]`:

```python
from rolld import Roller


filepath = "image.png"
image = Roller(filepath)
rolled = image.roll(sorter="LUM")

rolled.show()
```


## Example

Here is an example. We are going to use the image `lena.png`:

<img src="./assets/images/lena.png" width="250" height="250">

And with this code we will "roll" the image:

```python
from rolld import Roller


filepath = "lena.png"
roller = Roller(filepath)

sorters = ["HSV", "HSL", "YIQ", "LUM"]
for sorter in sorters:
    image = roller.roll(sorter=sorter)
    image.show()

```

Here is the output of all the sorting methods:

### Luminance

<img src="./assets/images/lena_lum.png">

### YIQ

<img src="./assets/images/lena_yiq.png">

### HSV

<img src="./assets/images/lena_hsv.png">

### HSL

<img src="./assets/images/lena_hsl.png">
