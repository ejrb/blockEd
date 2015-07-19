from cStringIO import StringIO
from collections import OrderedDict

from blocked.engine import SettingsReporter, GameReporter, Engine, \
    PlayerReporter
from blocked.blocks import OBlock, IBlock
from blocked.field import Field
from blocked.score import ScoreKeeper

_test_settings = OrderedDict([
    ('time_bank', 1),
    ('time_per_move', 2),
    ('player_names', ('p1', 'p2')),
    ('your_bot', 'p1'),
    ('field_height', 20),
    ('field_width', 10)
])


def test_settings_reporter():
    reporter = SettingsReporter(_test_settings)
    assert _read_report(reporter) == (
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


def _read_report(reporter):
    buf = StringIO()
    reporter.report_to(buf)
    buf.seek(0)
    return buf.read()


def test_game_reporter_initial():
    f = Field(4, 4)
    mock_block_source = iter([OBlock(f), IBlock(f)])
    engine = Engine(block_source=mock_block_source)
    reporter = GameReporter(engine)
    assert _read_report(reporter) == (
        'update game round 1\n'
        'update game this_piece_type O\n'
        'update game next_piece_type I\n'
        'update game this_piece_position 4,-1\n'
    )


def test_player_reporter():
    """reporting player status"""
    sk = ScoreKeeper(15, 2)
    f = Field.from_str('0,0,0,0;0,0,2,2;0,2,2,2;3,3,3,3')

    reporter = PlayerReporter('first_player', f, sk)

    assert _read_report(reporter) == (
        'update first_player row_points 15\n'
        'update first_player combo 2\n'
        'update first_player field\n'
        '0,0,0,0;0,0,2,2;0,2,2,2;3,3,3,3\n'
    )
