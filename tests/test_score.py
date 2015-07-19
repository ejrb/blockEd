from blocked.score import ScoreKeeper


def test_update_score():
    """if fewer than 4 rows, 1 point per row else 2 points per row, plus the
    current combo which increments for each round with at least 1 row
    removal """
    score_keeper = ScoreKeeper()
    assert score_keeper.score == 0
    assert score_keeper.combo == 0

    score_keeper.rows_removed(1)
    assert score_keeper.score == 1
    assert score_keeper.combo == 1

    score_keeper.rows_removed(0)
    assert score_keeper.score == 1
    assert score_keeper.combo == 0

    score_keeper.rows_removed(4)
    assert score_keeper.score == 9
    assert score_keeper.combo == 1

    score_keeper.rows_removed(2)
    assert score_keeper.score == 12
    assert score_keeper.combo == 2

    score_keeper.rows_removed(1)
    assert score_keeper.score == 15
    assert score_keeper.combo == 3

    score_keeper.rows_removed(0)
    assert score_keeper.score == 15
    assert score_keeper.combo == 0
