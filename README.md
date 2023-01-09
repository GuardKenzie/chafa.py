<div align="center" >
  <img width=500 alt="chafa.py" src="https://github.com/GuardKenzie/chafa.py/blob/main/img/logo.svg?raw=true">
  <p>
    <em>The snakes don't bite! (I think...)</em>
  </p>
  <p>
      <a href="https://chafapy.mage.black/">Docs</a> | <a href="https://chafapy.mage.black/usage/tutorial.html">Tutorial</a> | <a href="https://chafapy.mage.black/usage/examples.html">Examples</a>
  </p>
</div>

# What is this?

[Chafa](https://hpjansson.org/chafa/) is a wonderful command-line utility, 
created by [Hans Petter Jansson](https://hpjansson.org/), for visualizing 
images in the terminal. In Jansson's own words:
  
> **The future is (still) now!**
>
>  The premier UX of the 21st century just got a little better: 
> With `chafa`, you can now view very, very reasonable approximations 
> of pictures and animations in the comfort of your favorite terminal 
> emulator. The power of ANSI X3.64 compels you!

chafa.py is a python wrapper for the chafa library so you can use rad graphics in your (undoubtedly pretty cool) Python applications!

chafa.py tries to be very *pythonian* (I think that's a word) in the sense that most getter and setter functions are simply made to be attributes of Python objects.

# Example

Here is a [picture of a cute snake](https://chafapy.mage.black/_images/snake.jpg) rendered to text using chafa.py:

<div align="center">
  <img src="https://github.com/GuardKenzie/chafa.py/blob/main/img/readme_snake.png?raw=true"></img>
</div>

And here is the code that printed this image. For more examples, head on over to the docs at [chafapy.mage.black](https://chafapy.mage.black).

```python
from chafa import *
from chafa.loader import Loader

# The font ratio of JetBrains Mono (width/height)
FONT_RATIO = 11/24

# Create a canvas config
config = CanvasConfig()

# Configure the canvas geometry
config.width  = 40
config.height = 40

# Load the snake
image = Loader("./snake.jpg")

# Configure the ideal canvas geometry based on our FONT_RATIO
config.calc_canvas_geometry(
   image.width,
   image.height,
   FONT_RATIO
)

# Init the canvas
canvas = Canvas(config)

# Draw to the canvs
canvas.draw_all_pixels(
   image.pixel_type,
   image.get_pixels(),
   image.width, image.height,
   image.rowstride
)

# Print the output
output = canvas.print()

print(output.decode())
```


# How do I get it?

First, you will need to [install chafa](https://hpjansson.org/chafa/download/). This should be fairly straight forward since chafa packages are available for most linux distributions.

If you want to use the included Loader class to load images for using with chafa.py, you will also need the [MagickWand](https://imagemagick.org/script/magick-wand.php) C-library.


### From PyPi

Chafa.py is available on PyPi. You can install it by running

```
pip install chafa.py
```

### From source

If you want, you can install and play around with this package by cloning the repo and building it yourself

```
python -m build
```

in the root of the repository. This will build a distribution file in a new folder: `dist/` called something like `chafa_py-[version].gz`. You can then install this file with pip by running

```
pip install ./dist/chafa_py-[version].tar.gz
```

### Dependencies

- [Chafa](https://hpjansson.org/chafa/download/)
- [MagickWand](https://imagemagick.org/script/magick-wand.php)
- [Hatchling](https://pypi.org/project/hatchling/) (for building) 
- Python 3.5 or later
