============
Installation
============

.. currentmodule:: chafa.loader

Here are some installation instructions for getting going. It is preferred to install from `PyPI`_, however, you are welcome to build from source if you so desire.

Currently every major 64-bit OS is supported except Windows on ARM.

For all methods, if you want to use the included :py:class:`Loader` class to load images, you will also need the `MagickWand <https://imagemagick.org/script/magick-wand.php>`_ C-library. The installation of MagickWand is fairly straight forward.

.. note::

   For a substantial performance increase when importing :py:class:`Loader`, you can set the ``MAGICK_HOME`` environment variable to where the ImageMagick library lives on your computer (i.e. for brew users, something like ``/usr/local/Cellar/imagemagick/``).

From PyPI
=========

Chafa.py is available on `PyPI`_. You can install it by running

::

    pip install chafa.py

If you are using MacOS, make sure to set your ``MAGICK_HOME`` environment variable appropriately or the :py:class:`Loader` might not find the ImageMagick.

From source
===========

When building from source, make sure you have installed the following:

- `Chafa <https://hpjansson.org/chafa/download/>`_, specifically that you have ``libchafa`` somewhere on your path
- `Hatchling <https://pypi.org/project/hatchling/>`_
- ``glib-2.0``

To install from source, clone `chafa.py repository`_ and run

::

    hatchling build -t wheel

When the build is finished (you might see some warnings, they are safe to ignore), there should be a ``.whl`` file in a new ``dist/`` folder. To install that, run

::
    
    pip install dist/{filename}.whl

replacing ``{filename}`` with the appropriate file name.

.. note::
    
    When installing from source, you have to make sure ``libchafa`` and ``libglib-2.0`` are somewhere on your path so chafa.py can find and use them.

Dependencies
============

- `Chafa <https://hpjansson.org/chafa/download/>`_
- `Hatchling <https://pypi.org/project/hatchling/>`_ (for building) 
- Python 3.8 or later

.. _`PyPI`: https://pypi.org/project/chafa.py/
.. _`chafa.py repository`: https://github.com/guardkenzie/chafa.py