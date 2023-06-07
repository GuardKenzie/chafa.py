from __future__ import annotations
import ctypes
import os
import platform

from .libraries import _Chafa
from .chafa import get_device_attributes
from .enums import *

class TermInfo():
    def __init__(self):
        # Init term_info
        _Chafa.chafa_term_info_new.restype = ctypes.c_void_p

        self._term_info = _Chafa.chafa_term_info_new()


    class TerminalCapabilities:
        def __init__(self, canvas_mode, pixel_mode):
            self.canvas_mode = canvas_mode
            self.pixel_mode = pixel_mode

        def __repr__(self):
            return f"TerminalCapabilities(canvas_mode={self.canvas_mode.name}, pixel_mode={self.pixel_mode.name})"

        def __eq__(self, other):
            return self.canvas_mode == other.canvas_mode and self.pixel_mode == other.pixel_mode


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

        if kitty_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_KITTY

        elif sixel_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SIXELS

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
    
