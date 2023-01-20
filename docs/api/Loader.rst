.. currentmodule:: chafa.loader

=================
The loader module
=================

The loader module depends on the `MagickWand`_ C-library. Make sure it is installed before using this module.

On Linux and MacOS, the loader module will try to search for `MagickWand`_ in the folder set by the environment variable ``MAGICK_HOME``. This is substantially faster than the alternate method so it is recommended to set this environment variable before importing :py:class:`Loader`.
 
::
    
    from chafa.loader import Loader
    import chafa

    config = chafa.CanvasConfig()
    canvas = chafa.Canvas(config)

    loader = Loader("./example.jpg")

    canvas.draw_all_pixels(
        loader.pixel_type,
        loader.get_pixels(),
        loader.width,
        loader.height,
        loader.rowstride
    )

    print(canvas.print().decode())

Loader
------

The :py:class:`Loader` is a reasonably fast way to load the pixel data of an image for use with chafa.py. In addition to loading the pixel data, the :py:class:`Loader` will also provide useful information such as the width and height of the image to further simplify drawing to the :py:class:`chafa.Canvas`.

.. py:class:: Loader(path: str)

    :param str path: The path to the image to load. This will not resolve special characters such as ``~``.

    :raises FileNotFoundError: if the image does not exist.

    .. py:property:: width

        :type: int

        The width of the image.

    .. py:property:: height

        :type: int

        The height of the image.

    .. py:property:: channels

        :type: int

        The number of output of :py:meth:`get_pixels`.

    .. py:property:: pixel_type

        :type: chafa.PixelType

        The :py:class:`chafa.PixelType` of the output of :py:meth:`get_pixels`.

    .. py:property:: rowstride

        :type: int

        The rowstride of the image.

    .. py:method:: get_pixels()

        :rtype: ctypes.Array

        Returns the pixel data of the image.


.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
