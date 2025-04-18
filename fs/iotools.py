"""Compatibility tools between Python 2 and Python 3 I/O interfaces."""

import typing

import io

if typing.TYPE_CHECKING:
    from typing import IO, Any, Iterator, Optional, Text


@typing.no_type_check
def make_stream(
    name,  # type: Text
    bin_file,  # type: io.RawIOBase
    mode="r",  # type: Text
    buffering=-1,  # type: int
    encoding=None,  # type: Optional[Text]
    errors=None,  # type: Optional[Text]
    newline="",  # type: Optional[Text]
    line_buffering=False,  # type: bool
    **kwargs  # type: Any
):
    # type: (...) -> IO
    """Take a Python 2.x binary file and return an IO Stream."""
    reading = "r" in mode
    writing = "w" in mode
    appending = "a" in mode
    binary = "b" in mode
    if "+" in mode:
        reading = True
        writing = True

    encoding = None if binary else (encoding or "utf-8")

    io_object = bin_file

    if buffering >= 0:
        if reading and writing:
            io_object = io.BufferedRandom(
                typing.cast(io.RawIOBase, io_object),
                buffering or io.DEFAULT_BUFFER_SIZE,
            )
        elif reading:
            io_object = io.BufferedReader(
                typing.cast(io.RawIOBase, io_object),
                buffering or io.DEFAULT_BUFFER_SIZE,
            )
        elif writing or appending:
            io_object = io.BufferedWriter(
                typing.cast(io.RawIOBase, io_object),
                buffering or io.DEFAULT_BUFFER_SIZE,
            )

    if not binary:
        io_object = io.TextIOWrapper(
            io_object,
            encoding=encoding,
            errors=errors,
            newline=newline,
            line_buffering=line_buffering,
        )

    return io_object


def line_iterator(readable_file, size=None):
    # type: (IO[bytes], Optional[int]) -> Iterator[bytes]
    """Iterate over the lines of a file.

    Implementation reads each char individually, which is not very
    efficient.

    Yields:
        str: a single line in the file.

    """
    read = readable_file.read
    line = []
    byte = b"1"
    if size is None or size < 0:
        while byte:
            byte = read(1)
            line.append(byte)
            if byte in b"\n":
                yield b"".join(line)
                del line[:]

    else:
        while byte and size:
            byte = read(1)
            size -= len(byte)
            line.append(byte)
            if byte in b"\n" or not size:
                yield b"".join(line)
                del line[:]
