from enum import Enum, auto
from semantics.QuadruplePrintMode import QuadruplePrintMode

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
    GOTO = auto()
    GOTO_F = auto()

    def print(self, quadruple_print_mode: QuadruplePrintMode) -> str:
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
            OperandType.PRINT: "PRINT",
            OperandType.GOTO: "GOTO",
            OperandType.GOTO_F: "GOTO_F",
        }

        operation_code_map = {
            OperandType.PLUS: "1",
            OperandType.MINUS: "2",
            OperandType.TIMES: "3",
            OperandType.DIVIDE: "4",
            OperandType.GREATER_THAN: "5",
            OperandType.LESS_THAN: "6",
            OperandType.NOT_EQUALS: "7",
            OperandType.ASSIGN: "8",
            OperandType.LEFT_PARENTHESIS: "9",
            OperandType.RIGHT_PARENTHESIS: "10",
            OperandType.PRINT: "11",
            OperandType.GOTO: "12",
            OperandType.GOTO_F: "12",
        }

        if quadruple_print_mode == QuadruplePrintMode.USE_VARIABLE_NAME:
            return symbol_map[self]
        elif quadruple_print_mode == QuadruplePrintMode.USE_VIRTUAL_DIRECTION:
            return operation_code_map[self]
        else:
            raise ValueError(f"Unknown quadruple print mode: {quadruple_print_mode}")