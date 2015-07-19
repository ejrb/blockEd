from collections import namedtuple, OrderedDict

Settings = namedtuple(
    'Settings', ('time_bank', 'time_per_move', 'player_names', 'your_bot',
                 'field_height', 'field_width')
)

player1_settings = Settings(11111, 511, 'player1,player2', 'player1', 21, 11)


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
    def __init__(self, engine):
        super(GameReporter, self).__init__()
        self._engine = engine

    def report_to(self, output):
        for k, v in self._engine.game.iteritems():
            output.write('update game {}\n'.format(_report_repr(k, v)))


class PlayerReporter(Reporter):
    def __init__(self, name, field, score_keeper):
        self._name = name
        self._field = field
        self._score_keeper = score_keeper

    def report_to(self, output):
        template = 'update {name} {{k}}{{v}}\n'.format(name=self._name)
        for k, v in (('row_points ', self._score_keeper.score),
                     ('combo ', self._score_keeper.combo),
                     ('field\n', self._field)):
            output.write(template.format(k=k, v=v))


class Engine(object):
    def __init__(self, block_source):
        self._block_source = block_source
        self.game = OrderedDict([
            ('round', 1),
            ('this_piece_type', self._next_block()),
            ('next_piece_type', self._next_block()),
            ('this_piece_position', (4, -1))
        ])

    def _next_block(self):
        return next(self._block_source)
