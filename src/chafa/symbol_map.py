from __future__ import annotations
import ctypes

from .libraries import _Chafa
from .enums import *

class ReadOnlySymbolMap():
    def __init__(self):
        # Init map
        _Chafa.chafa_symbol_map_new.restype = ctypes.c_void_p
        self._symbol_map = _Chafa.chafa_symbol_map_new()

    
    def copy(self) -> SymbolMap:
        """
        Returns a new :py:class:`SymbolMap` that's a copy of this one.

        :rtype: SymbolMap
        """

        # Argtypes
        _Chafa.chafa_symbol_map_copy.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_symbol_map_copy.restype = ctypes.c_void_p

        # Get new pointer
        new_pointer = _Chafa.chafa_symbol_map_copy(self._symbol_map)

        # Init symbol map
        symbol_map = SymbolMap()
        symbol_map._symbol_map = new_pointer

        return symbol_map



class SymbolMap(ReadOnlySymbolMap):
    def add_by_tags(self, tags: SymbolTags):
        """
        Adds symbols matching the set of tags to the symbol map.

        :param SymbolTags tags: The set of tags to add to the map.
        """

        # Set types
        _Chafa.chafa_symbol_map_add_by_tags.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint
        ]

        _Chafa.chafa_symbol_map_add_by_tags(self._symbol_map, tags)

    
    def remove_by_tags(self, tags: SymbolTags):
        """
        Removes symbols matching the set of tags from the symbol map.

        :param SymbolTags tags: The set of tags to remove from the map.
        """

        # If we did not get passed a SymbolTags
        # try to convert to SymbolTags which will give
        # an appropriate error if invalid
        if not isinstance(tags, SymbolTags):
            tags = SymbolTags(SymbolTags)

        # Set types
        _Chafa.chafa_symbol_map_remove_by_tags.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint
        ]

        _Chafa.chafa_symbol_map_remove_by_tags(self._symbol_map, tags)

    
    def add_by_range(self, first: str, last: str):
        """
        Adds symbols in the code point range starting with the character first and ending with the character last to the symbol map.

        For example, if first is given as ``a`` and last is given as ``f``, all characters ``a, b, c, d, e, f`` will be added to the map.

        :param str first: First code point to add, inclusive.
        :param str last: Last code point to add, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.
        """

        # Check types
        if not isinstance(first, str):
            raise TypeError(f"code point 'first' must be of type str. Got {type(first)}")

        if not isinstance(last, str):
            raise TypeError(f"code point 'last' must be of type str. Got {type(last)}")

        # check for chars
        if len(first) != 1:
            raise ValueError("code point 'first' must be of length 1")

        if len(last) != 1:
            raise ValueError("code point 'last' must be of length 1")

        # Set types
        _Chafa.chafa_symbol_map_add_by_range.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar,
            ctypes.c_wchar
        ]

        # add tags
        _Chafa.chafa_symbol_map_add_by_range(
            self._symbol_map,
            first,
            last
        )


    def remove_by_range(self, first: str, last: str):
        """
        Removes symbols in the code point range starting with the character first and ending with the character last from the symbol map.

        :param str first: First code point to remove, inclusive.
        :param str last: Last code point to remove, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.
        """

        # Check types
        if not isinstance(first, str):
            raise TypeError(f"code point 'first' must be of type str. Got {type(first)}")

        if not isinstance(last, str):
            raise TypeError(f"code point 'last' must be of type str. Got {type(last)}")

        # check for chars
        if len(first) != 1:
            raise ValueError("code point 'first' must be of length 1")

        if len(last) != 1:
            raise ValueError("code point 'last' must be of length 1")

        # Set types
        _Chafa.chafa_symbol_map_remove_by_range.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar,
            ctypes.c_wchar
        ]

        # remove tags
        _Chafa.chafa_symbol_map_remove_by_range(
            self._symbol_map,
            first,
            last
        )

    
    def apply_selectors(self, selectors: str):
        """
        Parses a string consisting of symbol tags separated by ``+-,`` and applies the pattern to the symbol map. If the string begins with ``+`` or ``-``, it's understood to be relative to the current set in the symbol map, otherwise the map is cleared first.

        The symbol tags are string versions of :py:class:`SymbolTags`, i.e.

        ================================================  ===========
        :py:class:`SymbolTags`                            String
        ================================================  ===========
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_ALL`        all
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_NONE`       none
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_SPACE`      space
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_SOLID`      solid
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_STIPPLE`    stipple
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_BLOCK`      block
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_BORDER`     border
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_DIAGONAL`   diagonal
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_DOT`        dot
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_QUAD`       quad
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_HALF`       half
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_EXTRA`      extra
        ================================================  ===========

        other :py:class:`SymbolTags` follow the same format and are supported.

        For example: ``block,border`` sets map to contain symbols matching either of those tags. ``+block,border-dot,stipple`` adds block and border symbols then removes dot and stipple symbols.

        :param str selectors: The string of selectors to apply.

        :raises ValueError: if the selectors string is invalid.
        """

        # Check type
        if not isinstance(selectors, str):
            raise TypeError(f"selectors must be of type str. Got {type(selectors)}")

        class GError(ctypes.Structure):
            _fields_ = [('domain',   ctypes.c_uint32),
                        ('code',     ctypes.c_int),
                        ('message',  ctypes.c_char_p)]

        # Set types

        _Chafa.chafa_symbol_map_apply_selectors.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(GError))
        ]

        _Chafa.chafa_symbol_map_apply_selectors.restype = ctypes.c_bool

        selectors = ctypes.c_char_p(bytes(selectors, "utf8"))

        # Init error
        error = ctypes.POINTER(GError)()

        success = _Chafa.chafa_symbol_map_apply_selectors(
            self._symbol_map,
            selectors,
            ctypes.byref(error)
        )
        
        if not success:
            error = error.contents.message.decode()
            raise ValueError(error)

        return success
