.. currentmodule:: chafa

=================
Terminal Database
=================

::

    import chafa

    database  = chafa.TermDb()
    term_info = database.detect()


TermDb
------

A :py:class:`TermDb` contains information on terminals, and can be used to obtain a suitable :py:class:`TermInfo` for a terminal environment.

.. py:class:: TermDb(no_defaults: bool=False)

    :param bool no_defaults: If ``True``, the class will be initialised blank instead of with the default global database.

    .. py:method:: copy()

        :rtype: TermDb

        Returns a new :py:class:`TermDb` which is a copy of this one.

    .. py:method:: detect()

        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with capabilities implied by the system environment variables (principally the ``TERM`` variable, but also others).

    .. py:method:: get_fallback_info()

        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with fallback control sequences. This can be used with unknown but presumably modern terminals, or to supplement missing capabilities in a detected terminal.
