.. currentmodule:: chafa

================
Useful functions
================

This page has documentation for the functions belonging to chafa.py that don't relate to any specific class.


Device attributes
-----------------

Device attributes are a concept in Xterm terminals that indicate what the terminal is capable of. This is used to detect sixels graphics capabilities in :py:meth:`TermInfo.detect_capabilities`. See `Xterm Control Sequences on invisible-island.net <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>`_ for details.

.. py:method:: get_device_attributes()

    A function that returns an tuple containing the current
    terminal's device attributes, fetched by reading the string
    provided by emitting the ``\e[c`` control sequence.

    This function will return an empty tuple if it is executed on a system that is not Linux.

    .. attention::
        Using this function in a terminal that does not reply to ``\e[c`` by putting a string ending in ``c`` on STDIN will cause the program to hang until it receives a lower case ``c`` on STDIN.

    :rtype: (int, ...)

    .. versionadded:: 1.1.0
