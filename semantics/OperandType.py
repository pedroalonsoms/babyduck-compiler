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
        }
        return symbol_map[self]