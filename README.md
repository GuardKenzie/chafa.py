<div align="center" >
  <img width=500 alt="Chafa.py" src="docs/_static/img/logo.svg">
  <p>
    <em>The snakes don't bite! (I think...)</em>
  </p>
  <p>
      <a href="https://chafapy.mage.black/">Docs</a> | <a href="https://chafapy.mage.black/usage/tutorial.html">Tutorial</a> | <a href="https://chafapy.mage.black/usage/examples.html">Examples</a>
  </p>
</div>

# THIS MODULE IS STILL IN PRE-RELEASE! THERE MIGHT BE BREAKING CHANGES TO THE API!
Please refrain from using in production code until a stable version 1.0 is released.

# What is this?

[Chafa](https://hpjansson.org/chafa/) is a wonderful command-line utility, 
created by [Hans Petter Jansson](https://hpjansson.org/), for visualizing 
images in the terminal. In Jansson's own words:
  
> **The future is (still) now!**
>
>  The premier UX of the 21st century just got a little better: 
> With ``chafa``, you can now view very, very reasonable approximations 
> of pictures and animations in the comfort of your favorite terminal 
> emulator. The power of ANSI X3.64 compels you!

chafa.py is a python wrapper for the chafa library so you can use rad graphics in your (undoubtedly pretty cool) Python applications!

chafa.py tries to be very *pythonian* (I think that's a word) in the sense that most getter and setter functions are simply made to be attributes of Python objects.

# How do I get it?

First, you will need to [install chafa](https://hpjansson.org/chafa/download/). This should be fairly straight forward since chafa packages are available for most linux distributions.

If you want to use the included loader class to load images for using with chafa.py, you will also need the [MagickWand](https://imagemagick.org/script/magick-wand.php) C-library.

Chafa.py is not available on PyPi yet but it will be soon! You can still install and play around with this package by cloning this repo and running

```
python -m build
```

in the root of the repository. This will build a distribution file in a new folder: `dist/` called something like `chafa-0.0.1.tar.gz`. You can then install this file with pip by running
```
pip install ./dist/chafa-0.0.1.tar.gz
```

## Dependencies
- [Chafa](https://hpjansson.org/chafa/download/)
- [MagickWand](https://imagemagick.org/script/magick-wand.php)
- Python 3.5 or later

# Example

Here is [the example program](https://hpjansson.org/chafa/ref/chafa-using.html) from the Chafa C API docs written in chafa.py. Take a look at the [examples](https://chafapy.mage.black/usage/examples.html) page in the docs for more cool examples.

```python  	
from chafa import *
from array import array

PIX_WIDTH  = 3
PIX_HEIGHT = 3
N_CHANNELS = 4

# Initiate pixels array ('B') for 8 bit values
pixels = array("B", [
    0xff, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff,
    0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0xff,
    0xff, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff
])

# Specify which symbols we want
symbol_map = SymbolMap()
symbol_map.add_by_tags(SymbolTags.CHAFA_SYMBOL_TAG_ALL)

# Set up a configuration with the symbols and the canvas size in characters
config = CanvasConfig()

config.width  = 23
config.height = 12

config.set_symbol_map(symbol_map)

# Create the canvas
canvas = Canvas(config)

# Draw pixels and build string
canvas.draw_all_pixels(
    PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED,
    pixels,
    PIX_WIDTH,
    PIX_HEIGHT,
    N_CHANNELS * PIX_WIDTH
)

output = canvas.print()

print(output)
```
