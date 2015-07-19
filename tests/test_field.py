import pytest

from blocked.exceptions import GameOver
from blocked.field import Field
from blocked.score import ScoreKeeper


def test_field_str_repr():
    """required string repr for outputting"""
    field = Field(6, 3)
    assert str(field) == '0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0'


def test_from_str():
    """instantiate a field from its string representation"""
    assert str(Field.from_str('0,0;0,0')) == '0,0;0,0'
    assert str(Field.from_str('0,0,2;0,0,2')) == '0,0,2;0,0,2'
    with_solid_row = Field.from_str('0,0,2;3,3,3')
    assert str(with_solid_row) == '0,0,2;3,3,3'


def test_row_completion():
    """update should delete any full rows and return the number removed"""
    score_keeper = ScoreKeeper()
    field = Field.from_str('0,0;0,0', score_keeper)
    field.remove_completed_rows()
    assert score_keeper.score == 0
    assert score_keeper.combo == 0
    assert str(field) == '0,0;0,0'

    field = Field.from_str('0,0,0;0,2,0;2,2,2', score_keeper)
    field.remove_completed_rows()
    assert score_keeper.score == 1
    assert score_keeper.combo == 1
    assert str(field) == '0,0,0;0,0,0;0,2,0'

    field = Field.from_str('0,0,0,0,0;2,2,2,2,2;2,0,2,2,2;2,2,2,2,2;0,0,0,2,0',
                           score_keeper)
    field.remove_completed_rows()
    assert score_keeper.score == 4
    assert score_keeper.combo == 2
    assert str(field) == '0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;2,0,2,2,2;0,0,0,2,0'


def test_raising():
    """raising the base should add a solid row (3s) which cannot be removed.
    if blocks are pushed above the upper bound, the game ends """
    score_keeper = ScoreKeeper()
    field = Field.from_str('0,0,0,0;0,0,2,2;2,2,2,0', score_keeper)

    field.raise_base()
    assert str(field) == '0,0,2,2;2,2,2,0;3,3,3,3'
    field.remove_completed_rows()
    assert str(field) == '0,0,2,2;2,2,2,0;3,3,3,3'

    with pytest.raises(GameOver):
        field.raise_base()

    assert score_keeper.score == 0
    assert score_keeper.combo == 0
