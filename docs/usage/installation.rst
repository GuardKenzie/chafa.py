Installation
============

First, you will need to `install chafa <https://hpjansson.org/chafa/download/>`_. This should be fairly straight forward since chafa packages are available for most linux distributions.

.. currentmodule:: chafa.loader

If you want to use the included :py:class:`Loader` class to load images for using with chafa.py, you will also need the `MagickWand <https://imagemagick.org/script/magick-wand.php>`_ C-library.

Chafa.py is not available on PyPi yet but it will be soon! You can still install and play around with this package by cloning this repo and running

::

    python -m build


in the root of the repository. This will build a distribution file in a new folder: ``dist/`` called something like ``chafa-0.0.1.tar.gz``. You can then install this file with pip by running

::

    pip install ./dist/chafa-0.0.1.tar.gz


Dependencies
------------

- `Chafa <https://hpjansson.org/chafa/download/>`_
- `MagickWand <https://imagemagick.org/script/magick-wand.php>`_
- Python 3.5 or later