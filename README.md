<div align="center" >
  <p>&nbsp;</p>
  <img width=500 alt="chafa.py" src="https://github.com/GuardKenzie/chafa.py/blob/main/img/logo.svg?raw=true">
  <p>&nbsp;</p>
  <p>
    <em>Terminal graphics with Python!</em>
  </p>
  <p>
      <a href="https://chafapy.mage.black/">📙 Docs</a>&nbsp;&nbsp;-&nbsp;&nbsp;<a href="https://chafapy.mage.black/usage/tutorial.html">🌱 Tutorial</a>&nbsp;&nbsp;-&nbsp;&nbsp;<a href="https://chafapy.mage.black/usage/examples.html">💾 Examples</a>
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

chafa.py is a python wrapper for the chafa library so you can use rad graphics in your (undoubtedly pretty cool) Python applications! The chafa.py library also tries to be very *pythonian* (I think that's a word) in the sense that most getter and setter functions are simply made to be attributes of Python objects.

### Features include:

- ⚡ Modern and intuitive Python API
- 📖 Extensive [documentation](https://chafapy.mage.black) and a [tutorial](https://chafapy.mage.black/usage/tutorial.html)
- 📟 Support for (almost) any terminal emulator
- [6️⃣ Sixels](https://www.arewesixelyet.com/), [😸 Kitty](https://sw.kovidgoyal.net/kitty/graphics-protocol/) and [🍎 ITerm2](https://iterm2.com/documentation-images.html) image protocols support
- 🐧 Linux, 🍎 MacOS (x86 and ARM), 🪟 Windows support

# Example

Here is a [picture of a cute snake](https://chafapy.mage.black/_images/snake.jpg) rendered to text using chafa.py:

<div align="center">
  <img src="https://github.com/GuardKenzie/chafa.py/blob/main/img/readme_snake.jpg?raw=true"></img>
</div>
<p></p>
<details>
  <summary>✏️ Code</summary>

  For more examples, head on over to the docs at [chafapy.mage.black](https://chafapy.mage.black).
  
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
</details>


# Where can I get it?

Chafa.py is available on [PyPi](https://pypi.org/project/chafa.py/). You can install it by running

```
pip install chafa.py
```

If you want to use the included Loader class to load images, you will also need to install [MagickWand](https://imagemagick.org/script/magick-wand.php).

### From source

There are instructions on building chafa.py from source on Windows or Linux in [the docs](https://chafapy.mage.black/usage/installation.html#from-source)

### Dependencies

- [Chafa](https://hpjansson.org/chafa/download/)
- [MagickWand](https://imagemagick.org/script/magick-wand.php)
- [Hatchling](https://pypi.org/project/hatchling/) (for building) 
- Python 3.8 or later


<details>
<summary>📬 P.S. The snakes don't bite <em>(I think...)</em></summary>
    🐍🐍🐍🐍🐍
</details> 
