from .score import ScoreKeeper
from .exceptions import GameOver


class _OutOfBoundsElem(object):
    """Can be retrieved but not assigned to"""

    def __getitem__(self, _):
        return None

    def __setitem__(self, key, value):
        raise IndexError('Cannot place block outside bounds')


OutOfBoundsElem = _OutOfBoundsElem()


class Row(object):
    """Squares outside bounds can be selected but not assigned to"""

    def __init__(self, w, value=0):
        self.w = w
        self._row = [value] * w

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

    def is_complete(self):
        return all(self._row)

    def is_empty(self):
        return not any(self._row)


class OutOfBoundsBottomRow(Row):
    """All elements are out of bounds"""

    def __getitem__(self, item):
        return OutOfBoundsElem


class OutOfBoundsTopRow(Row):
    """Blocks can be placed in the area above the field without breaking"""

    def __setitem__(self, key, value):
        if value > 1:
            raise GameOver('Block landing above field ended the game')
        super(OutOfBoundsTopRow, self).__setitem__(key, value)


class SolidRow(Row):
    def __init__(self, w):
        super(SolidRow, self).__init__(w, 3)

    def is_complete(self):
        return False


class Field(object):
    def __init__(self, height, width, score_keeper=None):
        self.h, self.w = height, width
        self._field = [Row(width) for _ in xrange(height)]
        self._score_keeper = score_keeper or ScoreKeeper()

    def __str__(self):
        return ';'.join(map(str, self._field))

    def __getitem__(self, item):
        if item < 0:
            return OutOfBoundsTopRow(self.w)
        if item >= self.h:
            return OutOfBoundsBottomRow(self.w)
        return self._field[item]

    def remove_completed_rows(self):
        completed = [
            i for i, row in enumerate(self._field) if row.is_complete()
        ]

        for i in reversed(completed):
            del self._field[i]

        for _ in completed:
            self._field.insert(0, Row(self.w))

        if self._score_keeper is not None:
            self._score_keeper.rows_removed(len(completed))

    def raise_base(self):
        if self._field[0].is_empty():
            del self._field[0]
            self._field.append(SolidRow(self.w))
        else:
            raise GameOver('Raising base has ended the game: {}'.format(self))

    @classmethod
    def from_str(cls, s, score_keeper=None):
        array = [map(int, r.split(',')) for r in s.split(';')]
        h, w = len(array), len(array[0])
        field = cls(h, w, score_keeper=score_keeper)
        for j, row in enumerate(array[::-1]):
            if row == [3] * w:
                field.raise_base()
            else:
                for i, v in enumerate(row):
                    field[h - j - 1][i] = v
        return field

    @property
    def score(self):
        return self._score_keeper.score

    @property
    def combo(self):
        return self._score_keeper.combo
