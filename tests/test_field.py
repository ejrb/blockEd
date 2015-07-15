from field import Field


def test_from_str():
    assert str(Field.from_str('0,0;0,0')) == '0,0;0,0'
    assert str(Field.from_str('0,0,1;0,0,1')) == '0,0,1;0,0,1'


def test_row_completion():
    """update should delete any full rows and return the number removed"""
    field = Field.from_str('0,0;0,0')
    assert field.update() == 0
    assert str(field) == '0,0;0,0'

    field = Field.from_str('0,0,0;0,1,0;1,1,1')
    assert field.update() == 1
    assert str(field) == '0,0,0;0,0,0;0,1,0'

    field = Field.from_str('0,0,0,0,0;1,1,1,1,1;1,0,1,1,1;1,1,1,1,1;0,0,0,1,0')
    assert field.update() == 2
    assert str(field) == '0,0,0,0,0;0,0,0,0,0;0,0,0,0,0;1,0,1,1,1;0,0,0,1,0'
