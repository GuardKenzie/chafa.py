.. currentmodule:: chafa

==========================
Frame, Image and Placement
==========================

These three objects are useful for animations or for image alignment within the :py:class:`Canvas`.
The most important thing to remember is:

   :py:class:`Frame` < :py:class:`Image` < :py:class:`Placement` < :py:class:`Canvas`

That is, a :py:class:`Placement` contains a :py:class:`Image` which contains a :py:class:`Frame`. Once that's all done, the :py:class:`Placement` can be placed on the :py:class:`Canvas`.

Frame
-----

.. py:class:: Frame(src_pixel_type: PixelType, src_pixels, src_width: int, src_height: int, src_rowstride: int)

    This defines a frame of an image. This has to be added to an :py:class:`Image`. The inputs are the same as in :py:meth:`Canvas.draw_all_pixels`.

    .. note::
        Best performance is achieved by passing a :py:class:`ctypes.Array` for src_pixels. A fast way to do this is to use `Pillow <https://pillow.readthedocs.io/en/stable/>`_; specifically the `Image.tobytes <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.tobytes>`_ method.

    :param PixelType src_pixel_type: The pixel type of src_pixels. This will determine what order the color channels will be read in and whether there is an alpha channel.
    :param list|tuple|array.array|ctypes.Array src_pixels: The source pixel data. This is a one dimensional array where every block of 3 (or 4 depending on the :py:class:`PixelType`) values represents one pixel of the image. The order of the channels is determined by src_pixel_type.

    :param int src_width:  The width of the source image.
    :param int src_height: The width of the source image.
    :param int src_rowstride: The number of values in src_image that represents one line pixels in the source image. Typically this will be the number of channels in the source image multiplied by src_width, e.g. for an image with no alpha channel and a width of 300 pixels, this will be ``3*300``.

    :raises ValueError: if src_width, src_height or src_rowstride are less than or equal to 0.

    .. versionadded:: 1.2.0

Image
-----

.. py:class:: Image

    A container for a :py:class:`Frame`. To be placed on a :py:class:`Placement`.

    .. versionadded:: 1.2.0

    .. py:property:: frame

        :type: Frame

        The :py:class:`Frame` for the image
    

Placement
---------
After assigning a :py:class:`Placement` to a :py:class:`Canvas` with :py:attr:`Canvas.placement`, you can print the :py:class:`Canvas` using :py:meth:`Canvas.print`.


.. py:class:: Placement(image: Image, id: int = 0)

    This class defines the placement of an :py:class:`Image` on a :py:class:`Canvas`. 

    .. note::
        None of placement's properties have any effect if the :py:class:`Canvas`'s pixel mode is set to :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.

    :param image: The :py:class:`Image` to be placed.
    :param id: An id to assign to the image. Leave as ``0`` to assign one automatically.

    .. versionadded:: 1.2.0

    .. py:property:: tuck

        :type: Tuck

        This describes how the :py:class:`Image` is resized to fit on the :py:class:`Canvas`, and defaults to :py:attr:`Tuck.CHAFA_TUCK_STRETCH`.

    
    .. py:property:: halign

        :type: Align

        Describes the horizontal alignment of the :py:class:`Image` on the :py:class:`Canvas`.

    
    .. py:property:: valign

        :type: Align

        Describes the horizontal alignment of the :py:class:`Image` on the :py:class:`Canvas`.