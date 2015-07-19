class BlockEdException(Exception):
    """base exception for blockEd"""


class BlockException(BlockEdException):
    """block problems"""


class InvalidBlockPosition(BlockException):
    """cannot place block here"""


class InvalidBlockRotation(BlockException):
    """cannot rotate block here"""


class CannotMoveBlock(BlockException):
    """cannot move block"""


class GameOver(BlockEdException):
    pass


class FirstPlayerWin(GameOver):
    """game ends with p1 victory"""


class SecondPlayerWin(GameOver):
    """game ends with p2 victory"""


class Tie(GameOver):
    """game ends in a tie"""
