import pytest

from blocked.blocks import rotate_cw, rotate_ccw, OBlock, IBlock
from blocked.exceptions import InvalidBlockPosition, CannotMoveBlock,\
    GameOver, InvalidBlockRotation
from blocked.field import Field


def test_matrix_rotation():
    """used to rotate blocks"""
    s = ((1, 2, 3),
         (4, 5, 6))
    tr, tl = rotate_cw, rotate_ccw
    assert tr(s) == ((4, 1), (5, 2), (6, 3)) == tl(tl(tl(s)))
    assert tr(tr(s)) == ((6, 5, 4), (3, 2, 1)) == tl(tl(s))
    assert tr(tr(tr(s))) == ((3, 6), (2, 5), (1, 4)) == tl(s)
    assert tr(tr(tr(tr(s)))) == s == tl(tl(tl(tl(s))))


def test_o_block():
    field = Field(6, 4)
    block = OBlock(field)
    block.position = 1, -1
    assert str(field) == '0,1,1,0;0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0'

    block.position = 0, 4
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;1,1,0,0;1,1,0,0'

    block.rotate_ccw().rotate_ccw()
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;1,1,0,0;1,1,0,0'


def test_invalid_block_placement():
    """cannot place blocks on top of each other or outside field bounds"""
    exp_str = '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,2,0,0;2,2,0,0'
    field = Field.from_str(exp_str)
    block = OBlock(field)

    # Place outside the field
    with pytest.raises(InvalidBlockPosition):
        block.position = -1, 4

    # Overlapping blocks
    with pytest.raises(InvalidBlockPosition):
        block.position = 0, 4

    assert str(field) == exp_str


def test_i_block():
    field = Field(6, 4)
    block = IBlock(field)

    block.position = 0, -1
    assert str(field) == '1,1,1,1;0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0'

    block.rotate_ccw()
    assert str(field) == '0,1,0,0;0,1,0,0;0,1,0,0;0,0,0,0;0,0,0,0;0,0,0,0'

    block.rotate_cw().rotate_cw()
    assert str(field) == '0,0,1,0;0,0,1,0;0,0,1,0;0,0,0,0;0,0,0,0;0,0,0,0'
    block.position = 1, 2
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,1;0,0,0,1;0,0,0,1;0,0,0,1'


def test_invalid_rotations():
    """cannot rotate blocks if they will collide with another"""
    field = Field.from_str('0,0,0,0;0,0,0,0;0,0,0,2;0,0,0,2;0,0,0,2;0,0,0,2')
    # Vertical I blocks placed next to each other
    block = IBlock(field).rotate_cw()
    block.position = 0, 2
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,1,2;0,0,1,2;0,0,1,2;0,0,1,2'

    # Block unable to rotate from this position
    with pytest.raises(InvalidBlockRotation):
        block.rotate_ccw()
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,1,2;0,0,1,2;0,0,1,2;0,0,1,2'


def test_drop():
    """blocks can be dropped downwards to their final position"""
    field = Field(6, 4)
    oblock1, oblock2, iblock = OBlock(field), OBlock(field), IBlock(field)

    # Drop first O into bottom right corner
    oblock1.position = 0, 0
    oblock1.drop()
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,2,0,0;2,2,0,0'

    # Move second O next to it and drop it (stays in place)
    oblock2.position = 2, 4
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,2,1,1;2,2,1,1'
    oblock2.drop()
    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,2,2,2;2,2,2,2'

    # Drop I on top of O
    iblock.position = 0, -1
    iblock.drop()

    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;2,2,2,2;2,2,2,2;2,2,2,2'

    with pytest.raises(CannotMoveBlock):
        oblock1.position = 0, 0

    with pytest.raises(CannotMoveBlock):
        oblock1.rotate_ccw()


def test_ending_game_with_drop():
    field = Field.from_str('0,0,0,0;3,3,3,3')

    oblock = OBlock(field)
    oblock.position = 1, -1

    with pytest.raises(GameOver):
        oblock.drop()
