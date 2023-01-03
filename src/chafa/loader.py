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

class Loader:

    def __init__(self, path: str):
        self._wand = ctypes.CDLL(_lib)
        
        # check if path exists
        path = Path(path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError()

        self.path = str(path)

        # === Argtypes ===

        self._wand.PixelSetColor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p
        ]

        self._wand.MagickSetBackgroundColor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self._wand.MagickReadImage.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p
        ]

        self._wand.DestroyPixelWand.argtypes = [ctypes.c_void_p]

        self._wand.MagickGetImageWidth. argtypes = [ctypes.c_void_p]
        self._wand.MagickGetImageHeight.argtypes = [ctypes.c_void_p]

        self._wand.MagickExportImagePixels.argtypes = [
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

        self._wand.NewMagickWand.restype = ctypes.c_void_p
        self._wand.NewPixelWand.restype  = ctypes.c_void_p

        self._wand.MagickGetImageWidth. restype = ctypes.c_int;
        self._wand.MagickGetImageHeight.restype = ctypes.c_int;

        # === Load necessary image information ===

        # Enum for uint8 pixel values
        CharPixel = 1

        # Init wand
        self._wand.MagickWandGenesis()

        # Do background color magicks
        magick_wand = self._wand.NewMagickWand()
        color       = self._wand.NewPixelWand()

        s = ctypes.c_char_p(bytes("none", "utf8"))

        self._wand.PixelSetColor(color, s)
        self._wand.MagickSetBackgroundColor(magick_wand, color)

        self._wand.DestroyPixelWand(color)

        # Grab image
        image_path = ctypes.c_char_p(bytes(self.path, "utf8"))

        self._wand.MagickReadImage(magick_wand, image_path)

        # Get image information
        width  = self._wand.MagickGetImageWidth (magick_wand)
        height = self._wand.MagickGetImageHeight(magick_wand)

        # We will have 4 channels because we are outputting RGBA
        rowstride = width * 4

        # Get pixels
        pixels = (ctypes.c_uint8 * (height * rowstride))()

        self._wand.MagickExportImagePixels(
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
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def channels(self):
        return self._channels

    @property
    def pixel_type(self):
        return self._pixel_type

    @property
    def rowstride(self):
        return self._rowstride

    def get_pixels(self):
        return self._pixels
