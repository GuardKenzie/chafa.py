.. raw:: html

   <h1 class="blocked-header">
      <span class="break-block">Chafa, </span>
      <span class="break-block">now with 20% more 🐍!</span>
   </h1>

=====
Index
=====


`Chafa <https://hpjansson.org/chafa/>`_ is a wonderful command-line utility, created by `Hans Petter Jansson`_, for visualizing images in the terminal. In Jansson's own words:
   
   **The future is (still) now!**

   The premier UX of the 21st century just got a little better: With ``chafa``, you can now view very, very reasonable approximations of pictures and animations in the comfort of your favorite terminal emulator. The power of ANSI X3.64 compels you!

chafa.py is a python wrapper for the chafa library so you can use rad graphics in your (undoubtedly pretty cool) Python applications! Not convinced? Here's a picture of a cute snake rendered to text using chafa.py and beamed into your visual cortex through the power of html and css:

.. raw:: html
   :file: _chafa_img/snake.html


chafa.py tries to be very *pythonian* (I think that's a word) in the sense that most getter and setter functions are simply made to be attributes of Python objects.

Here is the program used to output the :download:`image <usage/snake.jpg>` you see above::

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


That doesn't look that complicated! Take a look at the :ref:`examples` page for more cool examples or the :ref:`tutorial` to learn how chafa.py works. Also, here is a table of contents for these entire docs so you can sort of get a picture of what they cover and where to go:

Getting started
---------------
.. toctree::
   :maxdepth: 2
   :caption: Here are some links to get you going:

   usage/installation
   usage/tutorial
   usage/examples

API Reference
---------------
.. toctree::
   :maxdepth: 2
   :caption: If you are looking for a specific class or function, look no further:

   api/Canvas
   api/CanvasConfig
   api/SymbolMap
   api/TermDb
   api/TermInfo
   api/Loader
   api/enums

.. sidebar-links::
   :caption: External links:
   :github:
   :pypi: chafa.py
   
   Discussions <https://github.com/GuardKenzie/chafa.py/discussions>

.. _`Hans Petter Jansson`: https://hpjansson.org/
.. _`the example program`: https://hpjansson.org/chafa/ref/chafa-using.html
