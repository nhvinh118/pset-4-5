# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):

    """Write a file atomically
    :param file: str or :class:`os.PathLike` target to write
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string
    :param kwargs: anything else needed to open the file
    :raises: FileExistsError if target exists
    Example::
        with atomic_write("hello.txt") as f:
           f.write("world!")

    """
    dirname, fname = os.path.split(file)

    try:
        basename, ext = fname.split('.', 1)
    except ValueError:
        ext = ''

    with NamedTemporaryFile(
        mode=mode,
        dir=dirname, 
        suffix='.' + ext,
    ) as f:
         if as_file:
              yield f.name
         else:
              yield f
         #yield f
         os.link(f.name, file)
