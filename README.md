# pyrolld

A package to generate color sequences from videos and images

Its main use is to create a set of unique colors from an image and then
sort the colors according to the selected sorting method.

# Installation

You can simply pip install this package:

```bash
pip install pyrolld
```

# Usage

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
