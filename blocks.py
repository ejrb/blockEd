import functools
import itertools


class BlockException(Exception):
    """block problems"""


class InvalidBlockPosition(BlockException):
    """cannot place block"""


class CannotMoveBlock(BlockException):
    """cannot move block"""


def movement(meth):
    @functools.wraps(meth)
    def do_move_if_possible(block, *args, **kwargs):
        if block.movable:
            return meth(block, *args, **kwargs)
        else:
            raise CannotMoveBlock()
    return do_move_if_possible


class Block(object):
    type = ''
    shape = ()

    def __init__(self, field):
        self._field = field
        self._position = None, None
        self._movable = True

    def __str__(self):
        return self.type

    def _iter_location(self, x, y):
        for j, row in enumerate(self.shape):
            for i, check in enumerate(row):
                if check:
                    yield x + i, y + j

    def _can_place(self, x, y):
        for i, j in self._iter_location(x, y):
            if self._field[j][i]:
                return False
        return True

    def _update_field(self, x, y, v):
        for i, j in self._iter_location(x, y):
            self._field[j][i] = v

    def _place(self, x, y):
        self._update_field(x, y, 1)

    def _remove(self):
        x, y = self._position
        if x is not None and y is not None:
            self._update_field(x, y, 0)

    def _is_floating(self):
        return self._position == (None, None)

    @property
    def movable(self):
        return self._movable

    @movable.setter
    def movable(self, value):
        if value is False:
            x, y = self._position
            self._update_field(x, y, 2)
            self._movable = value

    @property
    def position(self):
        return self._position

    @position.setter
    @movement
    def position(self, value):
        if self._can_place(*value):
            self._remove()
            self._place(*value)
            self._position = value
        else:
            raise InvalidBlockPosition(
                "cannot place {} block at {}. \n{}"
                .format(self.type, value, str(self._field))
            )

    def _rotate(self, forward, back):
        self._remove()
        self.shape = forward(self.shape)
        if not self._is_floating():
            if not self._can_place(*self._position):
                self.shape = back(self.shape)
                self.position = self._position
                raise InvalidBlockPosition('Cannot rotate block')
            self.position = self._position

    @movement
    def rotate_cw(self):
        """Try to rotate the block clockwise by a quarter turn"""
        self._rotate(rotate_cw, rotate_ccw)
        return self

    @movement
    def rotate_ccw(self):
        """Try to rotate the block counter-clockwise by a quarter turn"""
        self._rotate(rotate_ccw, rotate_cw)
        return self

    @movement
    def drop(self):
        """Drop the block directly downwards to the bottom of the field.
        This is the block's final position and it cannot be moved further"""
        self._remove()
        x, y = self.position
        for i in itertools.count():
            if not self._can_place(x, y + i):
                self.position = x, y + i - 1
                break
        self.movable = False
        return self


def _build_block_cls(letter, shape):
    return type(
        '{}Block'.format(letter), (Block,), {'type': letter, 'shape': shape}
    )


OBlock = _build_block_cls('O', ((1, 1),
                                (1, 1)))
IBlock = _build_block_cls('I', ((0, 0, 0, 0),
                                (1, 1, 1, 1),
                                (0, 0, 0, 0),
                                (0, 0, 0, 0)))
JBlock = _build_block_cls('J', ((1, 0, 0),
                                (1, 1, 1),
                                (0, 0, 0)))
LBlock = _build_block_cls('L', ((0, 0, 1),
                                (1, 1, 1),
                                (0, 0, 0)))
SBlock = _build_block_cls('S', ((0, 1, 1),
                                (1, 1, 0),
                                (0, 0, 0)))
TBlock = _build_block_cls('T', ((0, 1, 0),
                                (1, 1, 1),
                                (0, 0, 0)))
ZBlock = _build_block_cls('Z', ((1, 1, 0),
                                (0, 1, 1),
                                (0, 0, 0)))
BLOCKS = {
    b.type: b for b in (
        OBlock, IBlock, JBlock, LBlock, SBlock, TBlock, ZBlock
    )
}
rotate_ccw = lambda m: tuple(map(tuple, reversed(zip(*m))))
rotate_cw = lambda m: tuple(map(tuple, zip(*reversed(m))))
