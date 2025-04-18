import io
import unittest

from fs import iotools, tempfs


class TestIOTools(unittest.TestCase):
    def setUp(self):
        self.fs = tempfs.TempFS("iotoolstest")

    def tearDown(self):
        self.fs.close()
        del self.fs

    def test_line_iterator(self):
        f = io.BytesIO(b"Hello\nWorld\n\nfoo")
        self.assertEqual(
            list(iotools.line_iterator(f)), [b"Hello\n", b"World\n", b"\n", b"foo"]
        )

        f = io.BytesIO(b"Hello\nWorld\n\nfoo")
        self.assertEqual(list(iotools.line_iterator(f, 10)), [b"Hello\n", b"Worl"])
