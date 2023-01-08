============
Installation
============

First things first
------------------

First, you will need to `install chafa <https://hpjansson.org/chafa/download/>`_. This should be fairly straight forward since chafa packages are available for most linux distributions.

.. currentmodule:: chafa.loader

If you want to use the included :py:class:`Loader` class to load images for using with chafa.py, you will also need the `MagickWand <https://imagemagick.org/script/magick-wand.php>`_ C-library.


From PyPi
---------

Chafa.py is available on PyPi. You can install it by running

::

    pip install chafa.py

From source
-----------

If you want, you can install and play around with this package by cloning the repo and building it yourself

::

    python -m build


in the root of the repository. This will build a distribution file in a new folder: ``dist/`` called something like ``chafa_py-[version].gz``. You can then install this file with pip by running

::

    pip install ./dist/chafa_py-[version].tar.gz


Dependencies
------------

- `Chafa <https://hpjansson.org/chafa/download/>`_
- `MagickWand <https://imagemagick.org/script/magick-wand.php>`_
- `Hatchling <https://pypi.org/project/hatchling/>`_ (for building) 
- Python 3.5 or later
