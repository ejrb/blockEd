import logging
import pytest
from blocks import rotate_cw, rotate_ccw, OBlock, InvalidBlockPosition, IBlock
from field import Field

log = logging.getLogger(__name__)


def test_matrix_rotation():
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
    field = Field(6, 4)
    block1, block2 = OBlock(field), OBlock(field)

    # Place outside the field
    with pytest.raises(InvalidBlockPosition):
        block1.position = -1, 4

    # Overlapping blocks
    block1.position = 0, 4
    with pytest.raises(InvalidBlockPosition):
        block2.position = 0, 4

    assert str(field) == '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;1,1,0,0;1,1,0,0'


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
    field = Field(6, 4)
    # Vertical I blocks placed next to each other
    block1, block2 = IBlock(field).rotate_cw(), IBlock(field).rotate_cw()
    block1.position = 1, 2
    block2.position = 0, 2
    exp_field = '0,0,0,0;0,0,0,0;0,0,1,1;0,0,1,1;0,0,1,1;0,0,1,1'
    assert str(field) == exp_field

    # Neither block able to rotate from this position
    for block in block1, block2:
        with pytest.raises(InvalidBlockPosition):
            block.rotate_ccw()
        assert str(field) == exp_field

        with pytest.raises(InvalidBlockPosition):
            block.rotate_cw()
        assert str(field) == exp_field
