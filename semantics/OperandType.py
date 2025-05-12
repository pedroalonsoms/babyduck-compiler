from enum import Enum, auto

class OperandType(Enum):
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    NOT_EQUALS = auto()
    ASSIGN = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    PRINT = auto()

    def to_symbol(self) -> str:
        symbol_map = {
            OperandType.PLUS: "+",
            OperandType.MINUS: "-",
            OperandType.TIMES: "*",
            OperandType.DIVIDE: "/",
            OperandType.GREATER_THAN: ">",
            OperandType.LESS_THAN: "<",
            OperandType.NOT_EQUALS: "!=",
            OperandType.ASSIGN: "=",
            OperandType.LEFT_PARENTHESIS: "(",
            OperandType.RIGHT_PARENTHESIS: ")",
            OperandType.PRINT: "print",
        }
        return symbol_map[self]