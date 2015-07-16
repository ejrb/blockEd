from cStringIO import StringIO
from collections import OrderedDict

from blocked.engine import SettingsReporter, UpdateReporter, Engine
from blocked.blocks import OBlock, IBlock
from blocked.field import Field

_test_settings = OrderedDict([
    ('time_bank', 1),
    ('time_per_move', 2),
    ('player_names', ('p1', 'p2')),
    ('your_bot', 'p1'),
    ('field_height', 20),
    ('field_width', 10)
])


def test_settings_reporter():
    buf = StringIO()
    settings_reporter = SettingsReporter(_test_settings)
    settings_reporter.report_to(buf)
    buf.seek(0)
    assert buf.read() == (
        'settings time_bank 1\n'
        'settings time_per_move 2\n'
        'settings player_names p1,p2\n'
        'settings your_bot p1\n'
        'settings field_height 20\n'
        'settings field_width 10\n'
    )


def test_game_engine_initial_game():
    f = Field(4, 4)
    blocks = [OBlock(f), IBlock(f)]
    mock_block_source = iter(blocks)
    engine = Engine(block_source=mock_block_source)
    assert dict(engine.game) == {
        'round': 1, 'this_piece_type': blocks[0],
        'next_piece_type': blocks[1], 'this_piece_position': (4, -1),
    }


def test_update_reporter_initial():
    f = Field(4, 4)
    mock_block_source = iter([OBlock(f), IBlock(f)])
    engine = Engine(block_source=mock_block_source)
    buf = StringIO()
    updater = UpdateReporter(engine)
    updater.report_to(buf)
    buf.seek(0)
    assert buf.read() == (
        'update game round 1\n'
        'update game this_piece_type O\n'
        'update game next_piece_type I\n'
        'update game this_piece_position 4,-1\n'
    )


def test_field_str_repr():
    field = Field(6, 3)
    assert str(field) == '0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0'
