from cStringIO import StringIO
from collections import OrderedDict

from blocked.engine import SettingsReporter, GameReporter, Engine, \
    PlayerReporter, GameState
from blocked.blocks import OBlock, IBlock, TBlock
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


def _read_report(reporter):
    buf = StringIO()
    reporter.report_to(buf)
    buf.seek(0)
    return buf.read()


def test_game_reporter_initial():
    mock_block_source = iter([OBlock, IBlock])
    reporter = GameReporter(GameState(mock_block_source))
    assert _read_report(reporter) == (
        'update game round 1\n'
        'update game this_piece_type O\n'
        'update game next_piece_type I\n'
        'update game this_piece_position 4,-1\n'
    )


def test_player_reporter():
    """reporting player status"""
    sk = ScoreKeeper(15, 2)
    f = Field.from_str('0,0,0,0;0,0,2,2;0,2,2,2;3,3,3,3', sk)

    reporter = PlayerReporter('first_player', f)

    assert _read_report(reporter) == (
        'update first_player row_points 15\n'
        'update first_player combo 2\n'
        'update first_player field\n'
        '0,0,0,0;0,0,2,2;0,2,2,2;3,3,3,3\n'
    )


def test_engine_initial():
    field = Field(4, 4)
    mock_block_source = iter([OBlock, IBlock])
    
    engine = Engine((field, field), ('p1', 'p2'), settings=_test_settings,
                    game_state=GameState(mock_block_source))
    
    assert _read_report(engine) == (
        'settings time_bank 1\n'
        'settings time_per_move 2\n'
        'settings player_names p1,p2\n'
        'settings your_bot p1\n'
        'settings field_height 20\n'
        'settings field_width 10\n'
        'update game round 1\n'
        'update game this_piece_type O\n'
        'update game next_piece_type I\n'
        'update game this_piece_position 4,-1\n'
        'update p1 row_points 0\n'
        'update p1 combo 0\n'
        'update p1 field\n'
        '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0\n'
        'update p2 row_points 0\n'
        'update p2 combo 0\n'
        'update p2 field\n'
        '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0\n'
    )


def test_engine_round_complete():
    p1_field_str = '0,0,0,0;0,0,0,0;2,0,0,2;2,2,0,2;2,2,2,2;2,2,2,2;3,3,3,3'
    p2_field_str = '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,0,0,2;2,0,2,2;2,2,2,0'

    field1 = Field.from_str(p1_field_str, score_keeper=ScoreKeeper(11, 2))
    field2 = Field.from_str(p2_field_str, score_keeper=ScoreKeeper(3, 1))

    mock_block_source = iter([OBlock, IBlock, TBlock])

    engine = Engine((field1, field2),
                    ('p1', 'p2'),
                    game_state=GameState(mock_block_source, starting_round=3),
                    settings=_test_settings)

    assert _read_report(engine) == (
        'update game round 3\n'
        'update game this_piece_type O\n'
        'update game next_piece_type I\n'
        'update game this_piece_position 4,-1\n'
        'update p1 row_points 11\n'
        'update p1 combo 2\n'
        'update p1 field\n'
        '{p1_field}\n'
        'update p2 row_points 3\n'
        'update p2 combo 1\n'
        'update p2 field\n'
        '{p2_field}\n'
    ).format(p1_field=p1_field_str, p2_field=p2_field_str)

    engine.complete_round()

    # Player 1 completes 2 rows, winning 2 (+2) points.  A solid row is
    # added to player 2's field.  Player 1's combo continues, player 2's is
    # lost.  New blocks are selected.  The round number is now
    assert _read_report(engine) == (
        'update game round 4\n'
        'update game this_piece_type I\n'
        'update game next_piece_type T\n'
        'update game this_piece_position 4,-1\n'
        'update p1 row_points 15\n'
        'update p1 combo 3\n'
        'update p1 field\n'
        '0,0,0,0;0,0,0,0;0,0,0,0;0,0,0,0;2,0,0,2;2,2,0,2;3,3,3,3\n'
        'update p2 row_points 3\n'
        'update p2 combo 0\n'
        'update p2 field\n'
        '0,0,0,0;0,0,0,0;0,0,0,0;2,0,0,2;2,0,2,2;2,2,2,0;3,3,3,3\n'
    )
