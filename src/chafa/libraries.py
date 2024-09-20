import os
from pathlib import Path
import ctypes
import ctypes.util
import platform

#  CHAFA LETS GOOOOOOO!!!
_root_dir = Path(os.path.dirname(__file__)) 

def find_chafa():
    search_names = ["chafa", "libchafa", "libchafa-0"]
    for name in search_names:
        chafa = ctypes.util.find_library(name)
        if chafa:
            break
    
    return chafa

def find_glib():
    search_names  = ["glib", "glib-2.0", "libglib", "libglib-2.0", "libglib-2.0-0"]
    for name in search_names:
        glib = ctypes.util.find_library(name)
        if glib:
            break
    
    return glib

# Figure out which libraries we need to import
if platform.system() == "Linux":
    _lib_glib = "libglib-2.0.so"
    _lib      = _root_dir / "libs" / "libchafa.so"

    try:
        ctypes.CDLL(_lib_glib)
    except OSError:
        _lib_glib = find_glib()

    if not _lib.exists():
        _lib = find_chafa()

elif platform.system() == "Windows":
    os.add_dll_directory(os.path.dirname(__file__))

    _lib_glib = _root_dir / "libs" / "libglib-2.0-0.dll"
    _lib      = _root_dir / "libs" / "libchafa.dll"

    if not _lib_glib.exists():
        _lib_glib = find_glib()

    if not _lib.exists():
        _lib = find_chafa()


elif platform.system() == "Darwin":
    _lib_glib = _root_dir / ".dylibs" / "libglib-2.0.0.dylib"
    _lib      = _root_dir / "libs"    / "libchafa.dylib"

    if not _lib_glib.exists():
        _lib_glib = find_glib()

    if not _lib.exists():
        _lib = find_chafa()

else:
    raise ImportError("You appear to be running on an unsupported system.")


if _lib is None:
    raise ImportError("libchafa was not found on your system.")

if _lib_glib is None:
    raise ImportError("libglib-2.0 was not found on your system.")

_lib      = str(_lib)
_lib_glib = str(_lib_glib)

_Chafa = ctypes.CDLL(_lib)