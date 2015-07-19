class ScoreKeeper(object):
    def __init__(self):
        self.score = 0
        self.combo = 0

    def rows_removed(self, rows):
        if rows:
            self.score += self.combo + (rows if rows < 4 else 2 * rows)
            self.combo += 1
        else:
            self.combo = 0
