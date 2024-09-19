from __future__ import annotations
import ctypes

from .libraries import _Chafa
from .enums import Tuck, Align
from .image import Image


class Placement:
    def __init__(self, image: Image, id: int = 0):
        _Chafa.chafa_placement_new.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int
        ]

        _Chafa.chafa_placement_new.restype = ctypes.c_void_p

        self._placement = _Chafa.chafa_placement_new(image._image, id)
        self._image = image


    # === Tuck property ===
    
    @property
    def tuck(self) -> Tuck:
        return self._get_tuck()


    @tuck.setter
    def tuck(self, new_tuck: Tuck):
        new_tuck = Tuck(new_tuck)

        self._set_tuck(new_tuck)


    # === Halign property === 

    @property
    def halign(self) -> Align:
        return self._get_halign()


    @halign.setter
    def halign(self, new_halign: Align):
        new_halign = Align(new_halign)

        self._set_halign(new_halign)


    # === Valign property ===

    @property
    def valign(self) -> Align:
        return self._get_valign()


    @valign.setter
    def valign(self, new_valign: Align):
        new_valign = Align(new_valign)

        self._set_valign(new_valign)
    

    def _get_tuck(self) -> Tuck:
        _Chafa.chafa_placement_get_tuck.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_tuck.restype  = ctypes.c_uint

        tuck =_Chafa.chafa_placement_get_tuck(self._placement)
        return Tuck(tuck)
    

    def _set_tuck(self, new_tuck: Tuck):
        _Chafa.chafa_placement_set_tuck.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_tuck(self._placement, new_tuck)


    def _get_halign(self) -> Align:
        _Chafa.chafa_placement_get_halign.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_halign.restype  = ctypes.c_uint

        halign =_Chafa.chafa_placement_get_halign()
        return Align(halign)
    

    def _set_halign(self, new_halign: Align):
        _Chafa.chafa_placement_set_halign.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_halign(self._placement, new_halign)


    def _get_valign(self) -> Align:
        _Chafa.chafa_placement_get_valign.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_valign.restype  = ctypes.c_uint

        valign =_Chafa.chafa_placement_get_valign()
        return Align(valign)
    

    def _set_valign(self, new_valign: Align):
        _Chafa.chafa_placement_set_valign.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_valign(self._placement, new_valign)