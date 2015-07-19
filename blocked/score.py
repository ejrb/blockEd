class ScoreKeeper(object):
    def __init__(self, score=0, combo=0):
        self.score = score
        self.combo = combo

    def rows_removed(self, rows):
        if rows:
            self.score += self.combo + (rows if rows < 4 else 2 * rows)
            self.combo += 1
        else:
            self.combo = 0
