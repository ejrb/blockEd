import pytest

from blocked.exceptions import GameOver
from blocked.field import Field


def test_field_str_repr():
    """required string repr for outputting"""
    field = Field(6, 3)
    assert str(field) == '0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0'


def test_from_str():
    """instantiate a field from its string representation"""
    assert str(Field.from_str('0,0;0,0')) == '0,0;0,0'
    assert str(Field.from_str('0,0,2;0,0,2')) == '0,0,2;0,0,2'


def test_row_completion():
    """update should delete any full rows and return the number removed"""
    field = Field.from_str('0,0;0,0')
    assert field.update() == 0
    assert str(field) == '0,0;0,0'

    field = Field.from_str('0,0,0;0,2,0;2,2,2')
    assert field.update() == 1
    assert str(field) == '0,0,0;0,0,0;0,2,0'

    field = Field.from_str('0,0,0,0,0;2,2,2,2,2;2,0,2,2,2;2,2,2,2,2;0,0,0,2,0')
    assert field.update() == 2
    assert str(field) == '0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;2,0,2,2,2;0,0,0,2,0'


def test_raising():
    """raising the base should add a solid row (3s) which cannot be removed.
    if blocks are pushed above the upper bound, the game ends """
    field = Field.from_str('0,0,0,0;0,0,2,2;2,2,2,0')

    field.raise_base()
    assert str(field) == '0,0,2,2;2,2,2,0;3,3,3,3'
    assert field.update() == 0
    assert str(field) == '0,0,2,2;2,2,2,0;3,3,3,3'

    with pytest.raises(GameOver):
        field.raise_base()
