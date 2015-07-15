class _OutOfBoundsElem(object):
    """Can be retrieved but not assigned to"""
    def __getitem__(self, _):
        return None

    def __setitem__(self, key, value):
        raise IndexError('Cannot place block outside bounds')

OutOfBoundsElem = _OutOfBoundsElem()


class Row(object):
    """Squares outside bounds can be selected but not assigned to"""
    def __init__(self, w):
        self.w = w
        self._row = [0] * w

    def __getitem__(self, item):
        try:
            # Prevent negative index wrap around
            if item < 0:
                raise IndexError
            return self._row[item]
        except IndexError:
            # Blocks cannot exist beyond the horizontal bounds of the field
            return OutOfBoundsElem

    def __setitem__(self, key, value):
        self._row[key] = value

    def __str__(self):
        return ','.join(map(str, self._row))


class OutOfBoundsBottomRow(Row):
    """All elements are out of bounds"""
    def __getitem__(self, item):
        return OutOfBoundsElem


class OutOfBoundsTopRow(Row):
    """Blocks can be placed in the area above the field without breaking"""


class Field(object):
    def __init__(self, height, width):
        self.h, self.w = height, width
        self._field = [Row(width) for _ in xrange(height)]

    def __str__(self):
        return ';'.join(map(str, self._field))

    def __getitem__(self, item):
        if item < 0:
            return OutOfBoundsTopRow(self.w)
        if item >= self.h:
            return OutOfBoundsBottomRow(self.w)
        return self._field[item]
