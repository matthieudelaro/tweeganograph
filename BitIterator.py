# This file describs the Cipher class and provides some tests.
# It has been designed for Python 3.X. Please upgrade if you
# are using Python 2.X version.

# Sources:
# - examples about bytes and bytearray: http://www.dotnetperls.com/bytes
# - bit manipulation: https://wiki.python.org/moin/BitManipulation
# - unit tests: https://docs.python.org/3.5/library/unittest.html
import unittest


class Bit:
    """This class works directly on bits of a bytearray.
    It considers each item of the bytearray as a 8 bits, represented from
    left to right as
    most significant bit to least significant bit.
    For example, iterating over [1, 2] will return the following list:
    [0, 0, 0, 0,   0, 0, 0, 1,            0, 0, 0, 0,   0, 0, 1, 0]"""

    @staticmethod
    def len(data):
        """Returns the quantity of bits in data."""
        return len(data)*8

    @staticmethod
    def get(data, iterator):
        """Returns the value of the bit pointed by the iterator in data."""
        byte = iterator / 8
        offset = 7 - (iterator % 8)
        mask = 1 << offset
        if data[byte] & mask:
            return 1
        else:
            return 0

    @staticmethod
    def set(data, iterator, value):
        """Sets the value of the bit pointed by the iterator in data."""
        byte = iterator / 8
        offset = 7 - (iterator % 8)
        if value:
            mask = 1 << offset
            data[byte] = data[byte] | mask
        else:
            mask = ~(1 << offset)
            data[byte] = data[byte] & mask

    @staticmethod
    def equal(data1, start1, data2, start2, lengthToCompare):
        """Compares lengthToCompare bits of data1 (from bit at position start1)
        and data2 (from bit at position start2).
        Returns True if all of the bits are equal, False otherwise."""
        # print("compare ", start1, Bit.len(data1), start2, Bit.len(data2))
        for i in range(lengthToCompare):
            # print("\tcompare ", i, Bit.get(data1, start1 + i), Bit.get(data2, start2 + i))
            if Bit.get(data1, start1 + i) != Bit.get(data2, start2 + i):
                return False
        return True


class BitOver:
    """This class works directly on bits of the bytearray provided.
    to the constructor. It does the same as Bit class, except
    that the data on which it works is provided only once,
    to the constructor."""
    # todo : improve by providing __getitem__ and __setitem__ operators: http://stackoverflow.com/questions/2936863/python-implementing-slicing-in-getitem

    def __init__(self, data):
        self._data = data

    def len(self):
        return Bit.len(self._data)

    def get(self, iterator):
        return Bit.get(self._data, iterator)

    def set(self, iterator, value):
        Bit.set(self._data, iterator, value)

    def getData(self):
        return self._data


class TestBitMethods(unittest.TestCase):
    def setUp(self):
        self.elements = [0, 1, 2, 4, 8, 16]
        self.values = bytearray(self.elements)

    def test_len(self):
        self.assertEqual(len(self.elements)*8, Bit.len(self.elements))
        self.assertEqual(len(self.values)*8, Bit.len(self.values))

    def test_get(self):
        self.assertFalse(Bit.get(self.values, 7))
        self.assertFalse(Bit.get(self.elements, 7))
        self.assertTrue(Bit.get(self.values, 15))
        self.assertTrue(Bit.get(self.elements, 15))
        self.assertFalse(Bit.get(self.values, 23))
        self.assertFalse(Bit.get(self.elements, 23))

    def test_set_values(self):
        for counter in range(0, Bit.len(self.values)):
            Bit.set(self.values, counter, True)
            self.assertTrue(Bit.get(self.values, counter))
            Bit.set(self.values, counter, False)
            self.assertFalse(Bit.get(self.values, counter))

    def test_set_elements(self):
        for counter in range(0, Bit.len(self.elements)):
            Bit.set(self.elements, counter, True)
            self.assertTrue(Bit.get(self.elements, counter))
            Bit.set(self.elements, counter, False)
            self.assertFalse(Bit.get(self.elements, counter))

    def test_equal(self):
        elements2 = [17]
        values2 = bytearray(elements2)
        # for i in range(len(self.values)):
        #     str = ""
        #     for j in range(8):
        #         str += repr(Bit.get(self.values, i*8+j))
        #     print(str)
        self.assertFalse(Bit.equal(self.values, 40, values2, 0, 8))
        self.assertFalse(Bit.equal(self.values, 47, values2, 7, 1))


class TestBitOverMethods(unittest.TestCase):
    def setUp(self):
        self.elements = [0, 1, 2, 4, 8, 16]
        self.values = bytearray(self.elements)
        self.bElements = BitOver(self.elements)
        self.bValues = BitOver(self.values)

    def test_len(self):
        self.assertEqual(len(self.elements)*8, self.bElements.len())
        self.assertEqual(len(self.values)*8, self.bValues.len())

    def test_get(self):
        self.assertFalse(self.bValues.get(7))
        self.assertFalse(self.bElements.get(7))
        self.assertTrue(self.bValues.get(15))
        self.assertTrue(self.bElements.get(15))
        self.assertFalse(self.bValues.get(23))
        self.assertFalse(self.bElements.get(23))

    def test_set_values(self):
        for counter in range(0, Bit.len(self.values)):
            self.bValues.set(counter, True)
            self.assertTrue(self.bValues.get(counter))
            self.bValues.set(counter, False)
            self.assertFalse(self.bValues.get(counter))

    def test_set_elements(self):
        for counter in range(0, Bit.len(self.values)):
            self.bElements.set(counter, True)
            self.assertTrue(self.bElements.get(counter))
            self.bElements.set(counter, False)
            self.assertFalse(self.bElements.get(counter))


if __name__ == '__main__':
    unittest.main()
