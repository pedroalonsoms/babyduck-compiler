from enum import Enum, auto

class OperandType(Enum):
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    NOT_EQUALS = auto()
