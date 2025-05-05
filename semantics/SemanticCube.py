from semantics.OperandType import OperandType
from semantics.VariableType import VariableType

# This is a 3D semantic cube that will be indexed as follows:
# sematic_cube[(left_variable_type, right_variable_type, operand_type)] = result_variable_type
# Note: if the variable/operand combination is not in this table, then that means it's not
# supported and therefore we must throw an error.
SEMANTIC_CUBE = {
    # INT - INT
    (VariableType.INT, VariableType.INT, OperandType.PLUS): VariableType.INT,
    (VariableType.INT, VariableType.INT, OperandType.MINUS): VariableType.INT,
    (VariableType.INT, VariableType.INT, OperandType.TIMES): VariableType.INT,
    (VariableType.INT, VariableType.INT, OperandType.DIVIDE): VariableType.FLOAT,
    (VariableType.INT, VariableType.INT, OperandType.GREATER_THAN): VariableType.BOOLEAN,
    (VariableType.INT, VariableType.INT, OperandType.LESS_THAN): VariableType.BOOLEAN,
    (VariableType.INT, VariableType.INT, OperandType.NOT_EQUALS): VariableType.BOOLEAN,
    # INT - FLOAT
    (VariableType.INT, VariableType.FLOAT, OperandType.PLUS): VariableType.FLOAT,
    (VariableType.INT, VariableType.FLOAT, OperandType.MINUS): VariableType.FLOAT,
    (VariableType.INT, VariableType.FLOAT, OperandType.TIMES): VariableType.FLOAT,
    (VariableType.INT, VariableType.FLOAT, OperandType.DIVIDE): VariableType.FLOAT,
    (VariableType.INT, VariableType.FLOAT, OperandType.GREATER_THAN): VariableType.BOOLEAN,
    (VariableType.INT, VariableType.FLOAT, OperandType.LESS_THAN): VariableType.BOOLEAN,
    (VariableType.INT, VariableType.FLOAT, OperandType.NOT_EQUALS): VariableType.BOOLEAN,
    # FLOAT - INT
    (VariableType.FLOAT, VariableType.INT, OperandType.PLUS): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.INT, OperandType.MINUS): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.INT, OperandType.TIMES): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.INT, OperandType.DIVIDE): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.INT, OperandType.GREATER_THAN): VariableType.BOOLEAN,
    (VariableType.FLOAT, VariableType.INT, OperandType.LESS_THAN): VariableType.BOOLEAN,
    (VariableType.FLOAT, VariableType.INT, OperandType.NOT_EQUALS): VariableType.BOOLEAN,
    # FLOAT - FLOAT
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.PLUS): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.MINUS): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.TIMES): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.DIVIDE): VariableType.FLOAT,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.GREATER_THAN): VariableType.BOOLEAN,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.LESS_THAN): VariableType.BOOLEAN,
    (VariableType.FLOAT, VariableType.FLOAT, OperandType.NOT_EQUALS): VariableType.BOOLEAN,
    # BOOLEAN - BOOLEAN
    (VariableType.BOOLEAN, VariableType.BOOLEAN, OperandType.NOT_EQUALS): VariableType.BOOLEAN,
}
