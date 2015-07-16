class BlockEdException(Exception):
    """base exception for blockEd"""


class GameOver(BlockEdException):
    pass


class BlockException(BlockEdException):
    """block problems"""


class InvalidBlockPosition(BlockException):
    """cannot place block"""


class CannotMoveBlock(BlockException):
    """cannot move block"""
