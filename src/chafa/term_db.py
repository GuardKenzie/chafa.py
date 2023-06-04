from __future__ import annotations
import ctypes

from .libraries import _Chafa, _lib_glib
from .term_info import TermInfo

class TermDb():
    def __init__(self, no_defaults: bool=False):
        no_defaults = bool(no_defaults)

        # Init term db
        if no_defaults:
            _Chafa.chafa_term_db_new.restype = ctypes.c_void_p
            self._term_db = _Chafa.chafa_term_db_new()
        else:
            _Chafa.chafa_term_db_get_default.restype = ctypes.c_void_p
            self._term_db = _Chafa.chafa_term_db_get_default()

    def detect(self):
        """
        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with capabilities implied by 
        the system environment variables (principally the ``TERM`` 
        variable, but also others).
        """
        # Init glib
        glib = ctypes.CDLL(_lib_glib)
        glib.g_get_environ.restype = ctypes.c_void_p

        # Get environment
        environment = glib.g_get_environ()

        _Chafa.chafa_term_db_detect.restype  = ctypes.c_void_p
        _Chafa.chafa_term_db_detect.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        new_term_info = _Chafa.chafa_term_db_detect(
            self._term_db,
            environment
        )

        term_info = TermInfo()
        term_info._term_info = new_term_info

        return term_info


    def get_fallback_info(self) -> TermInfo:
        """
        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with fallback control 
        sequences. This can be used with unknown but presumably 
        modern terminals, or to supplement missing capabilities 
        in a detected terminal.
        """

        # Define types
        _Chafa.chafa_term_db_get_fallback_info.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_db_get_fallback_info.restype = ctypes.c_void_p

        # Get pointer to fallback info
        fallback_info_pointer = _Chafa.chafa_term_db_get_fallback_info(self._term_db)

        # Init fallback info
        fallback_info = TermInfo()
        fallback_info._term_info = fallback_info_pointer

        return fallback_info


    def copy(self) -> TermDb:
        """
        :rtype: TermDb

        Returns a new :py:class:`TermDb` which is a copy of this one.
        """

        # Argtypes
        _Chafa.chafa_term_db_copy.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_term_db_copy.restype = ctypes.c_void_p

        # Grab new pointer
        new_pointer = _Chafa.chafa_term_db_copy(self._term_db)

        # Init new term_db
        term_db = TermDb()
        term_db._term_db = new_pointer

        return term_db
