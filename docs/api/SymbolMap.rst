.. currentmodule:: chafa

===========
Symbol Maps
===========

::

    import chafa

    symbol_map = chafa.SymbolMap()

    symbol_map.add_by_tags(chafa.SymbolTags.CHAFA_SYMBOL_TAG_BLOCK)

SymbolMap
---------

A :py:class:`SymbolMap` describes a selection of the supported textual symbols that can be used in building a printable output string from a :py:class:`Canvas`.

To create a new :py:class:`SymbolMap`, simply initialise the class. You can then add symbols to it using :py:meth:`SymbolMap.add_by_tags` before copying it into a :py:class:`CanvasConfig` using :py:meth:`CanvasConfig.set_symbol_map`.

Note that some symbols match multiple tags, so it makes sense to e.g. add symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_BORDER` and then removing symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_DIAGONAL`.

.. note:: 
    The number of available symbols is a significant factor in the speed of :py:class:`Canvas`. For the fastest possible operation you could use a single symbol. :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_VHALF` works well by itself.


.. py:class:: SymbolMap

    :bases: :py:class:`ReadOnlySymbolMap`

    .. py:method:: add_by_tags(tags: SymbolTags)

        Adds symbols matching the set of tags to the symbol map.

        :param SymbolTags tags: The set of tags to add to the map.

    .. py:method:: remove_by_tags(tags: SymbolTags)

        Removes symbols matching the set of tags from the symbol map.

        :param SymbolTags tags: The set of tags to remove from the map.

    .. py:method:: add_by_range(first: str, last: str)

        Adds symbols in the code point range starting with the character first and ending with the character last to the symbol map.

        For example, if first is given as ``a`` and last is given as ``f``, all characters ``a, b, c, d, e, f`` will be added to the map.

        :param str first: First code point to add, inclusive.
        :param str last: Last code point to add, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.

    .. py:method:: remove_by_range(first: str, last: str)

        Removes symbols in the code point range starting with the character first and ending with the character last from the symbol map.

        :param str first: First code point to remove, inclusive.
        :param str last: Last code point to remove, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.

    .. py:method:: apply_selectors(selectors: str)

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


ReadOnlySymbolMap
-----------------

A :py:class:`ReadOnlySymbolMap` is a read only version of a :py:class:`SymbolMap`.

.. py:class:: ReadOnlySymbolMap

    .. py:method:: copy()

        Returns a new :py:class:`SymbolMap` that's a copy of this one.

        :rtype: SymbolMap