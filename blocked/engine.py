from collections import OrderedDict

from .blocks import default_block_source
from .exceptions import GameOver, FirstPlayerWin, SecondPlayerWin, Tie

_DEFAULT_SETTINGS = OrderedDict([
    ('time_bank', 10000),
    ('time_per_move', 500),
    ('player_names', ('player1', 'player2')),
    ('your_bot', 'player1'),
    ('field_height', 20),
    ('field_width', 10)
])


class Reporter(object):
    def report_to(self, output):
        pass


def _report_repr(k, v):
    if isinstance(v, tuple):
        v = ','.join(map(str, v))
    return '{} {}'.format(k, v)


class SettingsReporter(Reporter):
    def __init__(self, settings):
        super(SettingsReporter, self).__init__()
        self._settings = settings

    def report_to(self, output):
        for k, v in self._settings.iteritems():
            output.write('settings {}\n'.format(_report_repr(k, v)))


class GameReporter(Reporter):
    def __init__(self, game_state):
        super(GameReporter, self).__init__()
        self._game_state = game_state

    def report_to(self, output):
        for k, v in self._game_state.iteritems():
            output.write('update game {}\n'.format(_report_repr(k, v)))


class PlayerReporter(Reporter):
    def __init__(self, name, field):
        self._name = name
        self._field = field

    def report_to(self, output):
        template = 'update {name} {{k}}{{v}}\n'.format(name=self._name)
        for k, v in (('row_points ', self._field.score),
                     ('combo ', self._field.combo),
                     ('field\n', self._field)):
            output.write(template.format(k=k, v=v))


class GameState(object):
    def __init__(self, block_source=default_block_source(), starting_round=1):
        self.round = starting_round
        self._block_source = block_source
        self.current_block = self._new_block()
        self.next_block = self._new_block()
        self.block_position = 4, -1

    def iteritems(self):
        yield 'round', self.round
        yield 'this_piece_type', self.current_block.type
        yield 'next_piece_type', self.next_block.type
        yield 'this_piece_position', self.block_position

    def _new_block(self):
        return next(self._block_source)

    def next_round(self):
        self.round += 1
        self.current_block, self.next_block = self.next_block, self._new_block()


class Engine(Reporter):
    def __init__(self, fields, player_names, settings=None, game_state=None):
        self.field1, self.field2 = fields
        self._game_state = game_state or GameState()
        self._settings = settings or _DEFAULT_SETTINGS

        self._settings_reporter = SettingsReporter(settings)
        self._game_reporter = GameReporter(game_state)
        self._p1_reporter = PlayerReporter(player_names[0], self.field1)
        self._p2_reporter = PlayerReporter(player_names[1], self.field2)

    def report_to(self, output):
        if self._game_state.round == 1:
            self._settings_reporter.report_to(output)
        self._game_reporter.report_to(output)
        self._p1_reporter.report_to(output)
        self._p2_reporter.report_to(output)

    def _determine_winner(self, go1, go2):
        if go1 and go2:
            p1, p2 = self.field1.score, self.field2.score
            if p1 == p2:
                return Tie()
            return FirstPlayerWin() if p1 > p2 else SecondPlayerWin()
        return FirstPlayerWin() if go2 else SecondPlayerWin()

    def complete_round(self):
        self._game_state.next_round()
        p1_score, p2_score = self.field1.score, self.field2.score

        self.field1.remove_completed_rows()
        self.field2.remove_completed_rows()

        to_add1 = self.field1.score / 4 - p1_score / 4
        to_add2 = self.field2.score / 4 - p2_score / 4

        game_over1 = game_over2 = False
        while to_add1 > 0 or to_add2 > 0:

            if to_add1:
                try:
                    self.field2.raise_base()
                except GameOver:
                    game_over2 = True
                to_add1 -= 1
            if to_add2:
                try:
                    self.field1.raise_base()
                except GameOver:
                    game_over1 = True
                to_add2 -= 1

            if game_over1 or game_over2:
                raise self._determine_winner(game_over1, game_over2)
