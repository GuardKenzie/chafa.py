============
Installation
============

.. currentmodule:: chafa.loader

Here are some installation instructions for getting going. It is preferred to install from `PyPi`_, however, you are welcome to build from source if you so desire.

Currently only Linux, Windows 64-bit and Intel MacOS systems are supported.

For all methods, if you want to use the included :py:class:`Loader` class to load images, you will also need the `MagickWand <https://imagemagick.org/script/magick-wand.php>`_ C-library. The installation of MagickWand is fairly straight forward.

.. note::

   For a substantial performance increase when importing :py:class:`Loader`, you can set the ``MAGICK_HOME`` environment variable to where the ImageMagick library lives on your computer (i.e. for brew users, something like ``/usr/local/Cellar/imagemagick/``).

From PyPi
=========

Chafa.py is available on `PyPi`_. You can install it by running

::

    pip install chafa.py

If you are using MacOS, make sure to set your ``MAGICK_HOME`` environment variable appropriately or the :py:class:`Loader` might not find the ImageMagick.

From source
===========

Building from source requires the `hatchling <https://pypi.org/project/hatchling/>`_ build tool. To build chafa.py from source on Linux or Windows, do the following:

Linux
-----

#. Navigate to the root of the `chafa.py repository`_ and run

   ::

        git clone https://github.com/hpjansson/chafa libs/libchafa_src


#. Navigate to the newly cloned chafa source and run

   ::

        ./autogen.sh --without-tools
        make

#. Navigate back to the root of the chafa.py repository and run

   ::

        cp libs/libchafa_src/chafa/.libs/libchafa.so libs/linux


#. You are now all set to build! Run

   ::

        hatchling build -t wheel


#. There should now be a new ``.whl`` file in ``./dist``. Install that with
   
   ::
    
        pip install dist/chafa.py-[version]-[tags].whl

   replacing the ``[version]`` and ``[tags]`` with the appropriate values.



Windows
-------

#. Navigate to the root of the `chafa.py repository`_ and run
   ::

        hatchling build -t wheel

#. There should now be a new ``.whl`` file in ``./dist``. Install that with
   
   ::
    
        pip install dist/chafa.py-[version]-[tags].whl

   replacing the ``[version]`` and ``[tags]`` with the appropriate values.


Dependencies
============

- `Chafa <https://hpjansson.org/chafa/download/>`_
- `MagickWand <https://imagemagick.org/script/magick-wand.php>`_
- `Hatchling <https://pypi.org/project/hatchling/>`_ (for building) 
- Python 3.8 or later

.. _`PyPi`: https://pypi.org/project/chafa.py/
.. _`chafa.py repository`: https://github.com/guardkenzie/chafa.py