from __future__ import annotations
import ctypes
import os
import platform
import warnings

from typing import Iterable

from .libraries import _Chafa
from .chafa import get_device_attributes
from .enums import *


class PixelPassthroughNeeded():
    """
    TODO: Documentation
    """
    def __init__(self, term_info: TermInfo):
        self.term_info = term_info


    def __iter__(self):
        self.passthrough_index = 1 # Skip CHAFA_PIXEL_PASSTHROUGH_NONE
        return self

    def __next__(self):
        if self.passthrough_index < Passthrough.CHAFA_PASSTHROUGH_MAX:
            out = (
                Passthrough(self.passthrough_index), 
                self[self.passthrough_index]
            )

            self.passthrough_index += 1
            return out
        
        else:
            raise StopIteration


    def __repr__(self):
        return str(dict(self))


    def __getitem__(self, pixel_passthrough: Passthrough):
        pixel_passthrough = Passthrough(pixel_passthrough)
        
        return self._get_is_pixel_passthrough_needed(pixel_passthrough)
    

    def __setitem__(self, pixel_passthrough: Passthrough, value: bool):
        pixel_passthrough = Passthrough(pixel_passthrough)
        value = bool(value)

        self._set_is_pixel_passthrough_needed(pixel_passthrough, value)


    def _get_is_pixel_passthrough_needed(self, pixel_passthrough: Passthrough):
        """
        wrapper for chafa_term_info_get_is_pixel_passthrough_needed
        """

        _Chafa.chafa_term_info_get_is_pixel_passthrough_needed.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_get_is_pixel_passthrough_needed.restype = ctypes.c_bool

        return _Chafa.chafa_term_info_get_is_pixel_passthrough_needed(
            self.term_info._term_info, 
            pixel_passthrough
        )
    

    def _set_is_pixel_passthrough_needed(self, passthrough: Passthrough, value: bool):
        """
        wrapper for chafa_term_info_set_is_pixel_passthrough_needed
        """

        _Chafa.chafa_term_info_set_is_pixel_passthrough_needed.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_bool
        ]

        _Chafa.chafa_term_info_set_is_pixel_passthrough_needed(
            self.term_info._term_info,
            passthrough,
            value
        )


class InheritedSequences():
    """
    TODO: Documentation
    """
    def __init__(self, term_info: TermInfo):
        self.term_info = term_info


    def __iter__(self):
        self.seq = 0
        return self

    def __next__(self):
        if self.seq < TermSeq.CHAFA_TERM_SEQ_MAX:
            out = [TermSeq(self.seq).name, self[self.seq]]
            self.seq += 1
            return out
        
        else:
            raise StopIteration


    def __repr__(self):
        return str(dict(self))


    def __getitem__(self, sequence: TermSeq):
        sequence = TermSeq(sequence)
        
        return self._get_inherit_seq(sequence)
    

    def __setitem__(self, sequence: TermSeq, value: bool):
        sequence = TermSeq(sequence)
        value = bool(value)

        self._set_inherit_seq(sequence, value)
    

    def _get_inherit_seq(self, sequence: TermSeq):
        """
        wrapper for chafa_term_info_get_inherit_seq
        """

        _Chafa.chafa_term_info_get_inherit_seq.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_get_inherit_seq.restype = ctypes.c_bool

        return _Chafa.chafa_term_info_get_inherit_seq(
            self.term_info._term_info, 
            sequence
        )
    

    def _set_inherit_seq(self, sequence: TermSeq, value: bool):
        """
        wrapper for chafa_term_info_set_inherit_seq
        """

        _Chafa.chafa_term_info_set_inherit_seq.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_bool
        ]

        _Chafa.chafa_term_info_set_inherit_seq(
            self.term_info._term_info,
            sequence,
            value
        )


class TermInfo():
    def __init__(self):
        # Init term_info
        _Chafa.chafa_term_info_new.restype = ctypes.c_void_p

        self._term_info = _Chafa.chafa_term_info_new()
        self._inherited_sequences = InheritedSequences(self)
        self._pixel_passthrough_needed = PixelPassthroughNeeded(self)


    class TerminalCapabilities:
        def __init__(self, canvas_mode, pixel_mode):
            self.canvas_mode = canvas_mode
            self.pixel_mode = pixel_mode

        def __repr__(self):
            return f"TerminalCapabilities(canvas_mode={self.canvas_mode.name}, pixel_mode={self.pixel_mode.name})"

        def __eq__(self, other):
            return self.canvas_mode == other.canvas_mode and self.pixel_mode == other.pixel_mode


    # == Inherited_sequences property ==
    @property
    def inherited_sequences(self) -> Iterable:
        """
        TODO: docs
        """
        return self._inherited_sequences


    # == Pixel_passthrough_needed property ==
    @property
    def pixel_passthrough_needed(self) -> Iterable:
        """
        TODO: docs
        """
        return self._pixel_passthrough_needed
    

    @property
    def name(self) -> str:
        """
        TODO: docs
        """
        return self._get_name().decode()
    
    @name.setter
    def name(self, name: str):
        self._set_name(name)
    

    def _get_name(self):
        """
        wrapper for chafa_term_info_get_name
        """

        _Chafa.chafa_term_info_get_name.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_get_name.restype = ctypes.c_char_p

        res = _Chafa.chafa_term_info_get_name(self._term_info)

        return res

    
    def _set_name(self, name: str):
        """
        wrapper for chafa_term_info_set_name
        """

        _Chafa.chafa_term_info_set_name.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p
        ]

        _Chafa.chafa_term_info_set_name(self._term_info, name.encode())


    # === Quirks property ===

    @property
    def quirks(self) -> tuple[quirks]:
        """
        TODO: docs
        """
        enabled_quirks = self._get_quirks()
        out = []

        for quirk in Quirks:
            if quirk & enabled_quirks == quirk:
                enabled_quirks ^= quirk
                out.append(quirk)
        
        return tuple(out)

    @quirks.setter
    def quirks(self, new_quirks: Iterable[Quirks]):
        quirk_bits = 0

        for quirk in new_quirks:
            quirk = Quirks(quirk)
            quirk_bits |= quirk
        
        self._set_quirks(quirk_bits)
    

    def _get_quirks(self):
        """
        wrapper for chafa_term_info_get_quirks
        """

        _Chafa.chafa_term_info_get_quirks.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_get_quirks.restype = ctypes.c_int

        return _Chafa.chafa_term_info_get_quirks(self._term_info)


    def _set_quirks(self, quirks):
        """
        wrapper for chafa_term_info_set_quirks
        """

        _Chafa.chafa_term_info_set_quirks.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_set_quirks(self._term_info, quirks)


    # === Safe symbol tags ===

    @property
    def safe_symbol_tags(self) -> tuple[SymbolTags]:
        """
        TODO: docs
        """

        safe_tags = self._get_safe_symbol_tags()
        out = []

        compound_tags = [
            SymbolTags.CHAFA_SYMBOL_TAG_ALL,
            SymbolTags.CHAFA_SYMBOL_TAG_HALF,
            SymbolTags.CHAFA_SYMBOL_TAG_ALNUM,
            SymbolTags.CHAFA_SYMBOL_TAG_BAD
        ]

        for tag in [*compound_tags, *SymbolTags]:
            if tag == SymbolTags.CHAFA_SYMBOL_TAG_NONE:
                continue

            if tag & safe_tags == tag:
                safe_tags ^= tag
                out.append(tag)
        
        return tuple(out)

    @safe_symbol_tags.setter
    def safe_symbol_tags(self, new_symbol_tags: Iterable[SymbolTags]):
        symbol_tag_bits = 0

        for tag in new_symbol_tags:
            tag = SymbolTags(tag)
            symbol_tag_bits |= tag
        
        self._set_safe_symbol_tags(symbol_tag_bits)
    

    def _get_safe_symbol_tags(self):
        """
        wrapper for chafa_term_info_get_safe_symbol_tags
        """

        _Chafa.chafa_term_info_get_safe_symbol_tags.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_get_safe_symbol_tags.restype = ctypes.c_int

        return _Chafa.chafa_term_info_get_safe_symbol_tags(self._term_info)


    def _set_safe_symbol_tags(self, safe_symbol_tags):
        """
        wrapper for chafa_term_info_set_safe_symbol_tags
        """

        _Chafa.chafa_term_info_set_safe_symbol_tags.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_set_safe_symbol_tags(self._term_info, safe_symbol_tags)


    def copy(self) -> TermInfo:
        """
        Returns a new :py:class:`TermInfo` that is a copy of this one.

        :rtype: TermInfo
        """

        # Argtypes
        _Chafa.chafa_term_info_copy.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_copy.restype = ctypes.c_void_p

        # Grab new pointer
        new_pointer = _Chafa.chafa_term_info_copy(self._term_info)

        # Init new term_info
        term_info = TermInfo()
        term_info._term_info = new_pointer

        return term_info

    
    def supplement(self, source: 'TermInfo'):
        """
        Supplements missing sequences in this 
        :py:class:`TermInfo` with ones copied 
        from source.

        :param TermInfo source: The :py:class:`TermInfo` to copy sequences from.
        """

        if not isinstance(source, TermInfo):
            raise TypeError(f"source must be of type TermInfo, not {type(source)}")

        self._supplement(source._term_info)


    def _supplement(self, source: ctypes.c_void_p):
        """
        Wrapper for chafa_term_info_supplement
        """

        _Chafa.chafa_term_info_supplement.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_supplement(self._term_info, source)


    def have_seq(self, seq: TermSeq) -> bool:
        """
        Checks if :py:class:`TermInfo` can emit seq.
        
        :param TermSeq seq: A :py:class:`TermSeq` to query for.

        :rtype: bool
        """

        seq = TermSeq(seq)

        # Set types
        _Chafa.chafa_term_info_have_seq.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_int
        ]
        
        _Chafa.chafa_term_info_have_seq.restype = ctypes.c_bool

        # Check for sequence
        return _Chafa.chafa_term_info_have_seq(self._term_info, seq)


    def detect_capabilities(self) -> TerminalCapabilities:
        """
        A function that tries to detect the capabilities of the
        terminal and return the appropriate canvas and pixel modes
        """

        warnings.warn(
            "TermInfo.detect_capabilities is deprecated. \
            Developers should use TermInfo.best_pixel_mode and TermInfo.best_canvas_mode instead", 
            DeprecationWarning
        )

        # === Canvas mode ===

        color_direct = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_DIRECT) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_DIRECT) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_DIRECT)

        color_256    = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_256) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_256) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_256)

        color_16     = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_16) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_16) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_16)

        color_2      = self.have_seq(TermSeq.CHAFA_TERM_SEQ_INVERT_COLORS) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_RESET_ATTRIBUTES)

        if color_direct:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_TRUECOLOR

        elif color_256:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_240

        elif color_16:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_16

        elif color_2:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_FGBG_BGFG

        else:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_FGBG

        # === Pixel mode ===

        # Also check device attributes if we are on xterm
        terminal = os.environ.get("TERM", "")
        xterm_sixels = False

        if "xterm" in terminal and platform.system() == "Linux":
            attributes = get_device_attributes()

            xterm_sixels = 4 in attributes

        # Check for sixels
        sixel_capable = self.have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_SIXELS) \
            and         self.have_seq(TermSeq.CHAFA_TERM_SEQ_END_SIXELS) \

        sixel_capable = sixel_capable or xterm_sixels

        # Check for kitty
        kitty_capable = self.have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_KITTY_IMMEDIATE_IMAGE_V1)

        # Check for ITERM2
        iterm2_capable = self.have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_ITERM2_IMAGE)

        if kitty_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_KITTY

        elif sixel_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SIXELS
        
        elif iterm2_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_ITERM2

        else:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SYMBOLS


        # Init capabilities
        terminal_capabilities = self.TerminalCapabilities(canvas_mode, pixel_mode)

        return terminal_capabilities


    def emit(self, sequence: TermSeq, *args) -> bytes:
        """
        Returns the asked for terminal sequences as bytes.

        :param TermSeq *args: The sequences to emit

        :rtype: bytes
        """
        # Make sure we have a terminal sequence
        sequence = TermSeq(sequence)

        # Check if the terminal has the sequence
        if not self.have_seq(sequence):
            raise ValueError(f"Your terminal does not appear the sequence {sequence.name}")
        
        # Terminate the args
        args = (*args, -1)

        # Grab the sequence
        out = self._emit_seq(sequence, *args)

        # Check if we actually got anything
        if out is None:
            raise TypeError(f"Wrong number of arguments passed for sequence {sequence.name}")


        return out


    def _emit_seq(self, seq: TermSeq, *args):
        """
        wrapper for chafa_term_info_emit_seq
        """

        _Chafa.chafa_term_info_emit_seq.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int
        ]

        _Chafa.chafa_term_info_emit_seq.restype  = ctypes.c_char_p

        res = _Chafa.chafa_term_info_emit_seq(self._term_info, seq, *args)

        return res
    

    def chain(self, inner: TermInfo) -> TermInfo:
        """
        TODO: docs
        """

        # Construct placeholder term info
        chained_info = TermInfo()

        # Chain the infos together and assign the new one to the placeholder
        chained_pointer = self._chain(inner)
        chained_info._term_info = chained_pointer

        return chained_info


    def _chain(self, inner: TermInfo):
        """
        wrapper for chafa_term_info_chain
        """

        _Chafa.chafa_term_info_chain.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_chain.restype = ctypes.c_void_p

        res = _Chafa.chafa_term_info_chain(self._term_info, inner._term_info)

        return res
    

    def best_canvas_mode(self) -> CanvasMode:
        """
        TODO: Docs
        """

        return CanvasMode(self._best_canvas_mode())


    def _best_canvas_mode(self):
        """
        wrapper for chafa_term_info_get_best_canvas_mode
        """

        _Chafa.chafa_term_info_get_best_canvas_mode.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_get_best_canvas_mode.restype = ctypes.c_uint

        res = _Chafa.chafa_term_info_get_best_canvas_mode(self._term_info)

        return res


    def best_pixel_mode(self) -> PixelMode:
        """
        TODO: Docs
        """

        return PixelMode(self._best_pixel_mode())


    def _best_pixel_mode(self):
        """
        wrapper for chafa_term_info_get_best_pixel_mode
        """

        _Chafa.chafa_term_info_get_best_pixel_mode.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_info_get_best_pixel_mode.restype = ctypes.c_uint

        res = _Chafa.chafa_term_info_get_best_pixel_mode(self._term_info)

        return res


    def supports(self, mode: CanvasMode|PixelMode):
        """
        TODO: docs
        """

        if type(mode) == CanvasMode:
            supported = bool(self._is_canvas_mode_supported(mode))

        elif type(mode) == PixelMode:
            supported = bool(self._is_pixel_mode_supported(mode))

        else:
            raise TypeError("Provided 'mode' is neither PixelMode or CanvasMode")
        
        return supported


    def _is_canvas_mode_supported(self, canvas_mode: CanvasMode):
        """
        wrapper for chafa_term_info_is_canvas_mode_supported
        """

        _Chafa.chafa_term_info_is_canvas_mode_supported.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_is_canvas_mode_supported.restype = ctypes.c_bool

        res = _Chafa.chafa_term_info_is_canvas_mode_supported(self._term_info, canvas_mode)

        return res


    def _is_pixel_mode_supported(self, pixel_mode: PixelMode):
        """
        wrapper for chafa_term_info_is_pixel_mode_supported
        """

        _Chafa.chafa_term_info_is_pixel_mode_supported.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_term_info_is_pixel_mode_supported.restype = ctypes.c_bool

        res = _Chafa.chafa_term_info_is_pixel_mode_supported(self._term_info, pixel_mode)

        return res
    
