import ctypes.util
import ctypes
from pathlib import Path
from chafa import PixelType

def _get_library_name():
    """
    Function that tries to find the MagickWand Library
    by iterating over various versions
    """
    libwand = None

    versions = [
        "",
        "-7",
        "-7.Q8",
        "-7.Q16",
        "-6",
        "-Q16",
        "-Q8",
        "-6.Q16"
    ]

    i = 0

    while i < len(versions) and not libwand:
        libwand = ctypes.util.find_library(f"MagickWand{versions[i]}")
        i += 1

    return libwand

# Try to find library and raise ImportError if it isn't found
_lib = _get_library_name()

if _lib is None:
    raise ImportError("MagickWand library not found.")

_MagickWand = ctypes.CDLL(_lib)


class Loader:
    """
    The :py:class:`Loader` is a reasonably fast way 
    to load the pixel data of an image for use 
    with chafa.py. In addition to loading the pixel 
    data, the :py:class:`Loader` will also provide 
    useful information such as the width and height 
    of the image to further simplify drawing to the 
    :py:class:`chafa.Canvas`.

    :param str path: The path to the image to load. 
        This will not resolve special characters such as ``~``.

    :raises FileNotFoundError: if the image does not exist.
    """

    def __init__(self, path: str):
        
        # check if path exists
        path = Path(path).resolve()

        if not path.exists():
            raise FileNotFoundError()

        self.path = str(path)

        # === Argtypes ===

        _MagickWand.PixelSetColor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p
        ]

        _MagickWand.MagickSetBackgroundColor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _MagickWand.MagickReadImage.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p
        ]

        _MagickWand.DestroyPixelWand.argtypes = [ctypes.c_void_p]

        _MagickWand.MagickGetImageWidth. argtypes = [ctypes.c_void_p]
        _MagickWand.MagickGetImageHeight.argtypes = [ctypes.c_void_p]

        _MagickWand.MagickExportImagePixels.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_uint8)
        ]


        # === Restypes ===

        _MagickWand.NewMagickWand.restype = ctypes.c_void_p
        _MagickWand.NewPixelWand.restype  = ctypes.c_void_p

        _MagickWand.MagickGetImageWidth. restype = ctypes.c_int;
        _MagickWand.MagickGetImageHeight.restype = ctypes.c_int;

        # === Load necessary image information ===

        # Enum for uint8 pixel values
        CharPixel = 1

        # Init wand
        _MagickWand.MagickWandGenesis()

        magick_wand = _MagickWand.NewMagickWand()
        
        # Grab image
        image_path = ctypes.c_char_p(bytes(self.path, "utf8"))

        _MagickWand.MagickReadImage(magick_wand, image_path)

        # Get image information
        width  = _MagickWand.MagickGetImageWidth (magick_wand)
        height = _MagickWand.MagickGetImageHeight(magick_wand)

        # We will have 4 channels because we are outputting RGBA
        rowstride = width * 4

        # Get pixels
        pixels = (ctypes.c_uint8 * (height * rowstride))()

        _MagickWand.MagickExportImagePixels(
            magick_wand,
            0, 0,
            width, height,
            ctypes.c_char_p(bytes("RGBA", "utf8")),
            CharPixel,
            pixels
        )

        self._height        = height
        self._width         = width
        self._rowstride     = rowstride
        self._channels      = 4
        self._pixel_type    = PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED
        self._pixels        = pixels

    @property
    def width(self) -> int:
        """
        :type: int

        The width of the image.
        """
        return self._width

    @property
    def height(self) -> int:
        """
        :type: int

        The height of the image.
        """
        return self._height

    @property
    def channels(self) -> int:
        """
        :type: int

        The number of output of :py:meth:`get_pixels`.
        """
        return self._channels

    @property
    def pixel_type(self) -> PixelType:
        """
        :type: chafa.PixelType

        The :py:class:`chafa.PixelType` of the output 
        of :py:meth:`get_pixels`.
        """
        return self._pixel_type

    @property
    def rowstride(self) -> int:
        """
        :type: int

        The rowstride of the image.
        """
        return self._rowstride

    def get_pixels(self) -> ctypes.Array:
        """
        :rtype: ctypes.Array

        Returns the pixel data of the image.
        """
        return self._pixels
