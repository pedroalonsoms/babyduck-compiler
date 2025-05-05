from antlr.BabyDuckListener import BabyDuckListener
from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from antlr4 import *
from enum import Enum, auto
from dataclasses import dataclass, field

input_stream = FileStream("tests/semantic/test_cases/test_02.txt")  # or use InputStream for strings
lexer = BabyDuckLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = BabyDuckParser(token_stream)

tree = parser.programa()  # Replace `startRule` with your grammar's entry point

class VariableType(Enum):
    INT = auto()
    FLOAT = auto()
    BOOLEAN = auto()

class OperandType(Enum):
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    NOT_EQUALS = auto()

@dataclass
class Variable:
    name: str
    type: VariableType

class FunctionType(Enum):
    VOID = auto()

@dataclass
class Function:
    name: str
    type: FunctionType
    vars: dict[str, Variable] = field(default_factory=dict) # gpt fixed me this

# This is a 3D semantic cube that will be indexed as follows:
# sematic_cube[(left_variable_type, right_variable_type, operand_type)] = result_variable_type
# Note: if the variable/operand combination is not in this table, then that means it's not
# supported and therefore we must throw an error.
semantic_cube = {
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

class BabyDuckCustomListener(BabyDuckListener):
    def __init__(self):
        super().__init__()
        self.dirfuncs: dict[str, Function] = {}
        self.program_id = ""
        self.last_seen_var_ids = [] # this is a stack
        self.last_seen_func_id = ""

    def enterProgram_id(self, ctx):
        self.program_id = str(ctx.ID().getText())
        self.dirfuncs[self.program_id] = Function(name=self.program_id, type=FunctionType.VOID)

        # save last seen function id
        self.last_seen_func_id = self.program_id

    def enterMain(self, ctx):
        # whenever we enter the main function, we need to update this variable
        # so that we add to the variables table correctly
        self.last_seen_func_id = self.program_id

    def enterFunc_id(self, ctx):
        func_id = str(ctx.ID().getText())

        if func_id in self.dirfuncs:
            raise Exception(f"ERROR: Function '{func_id}' was already declared")
        self.dirfuncs[func_id] = Function(name=func_id, type=FunctionType.VOID)

        # save last seen function id
        self.last_seen_func_id = func_id

    def enterVar_id(self, ctx):
        var_id = str(ctx.ID().getText())

        # We need to add them to our stack so that when the type arrives,
        # we can finally add them to our table
        self.last_seen_var_ids.append(var_id)

    def enterVar_type(self, ctx):
        raw_var_type = str(ctx.type_().getText())

        # Detect the variable type
        var_type = None
        if raw_var_type == "int":
            var_type = VariableType.INT
        elif raw_var_type == "float":
            var_type = VariableType.FLOAT
        else:
            raise Exception(f"ERROR: Unexpected variable type {raw_var_type}")

        # Pop all the seen vars and add them to our var table
        function_directory = self.dirfuncs[self.last_seen_func_id]
        while self.last_seen_var_ids:
            last_seen_var_id = self.last_seen_var_ids.pop()

            # check if variable is already present
            if last_seen_var_id in function_directory.vars:
                raise Exception(f"ERROR: Variable '{last_seen_var_id}' was already declared on function directory '{function_directory.name}'")
            
            # We create the new variable
            function_directory.vars[last_seen_var_id] = Variable(name=last_seen_var_id, type=var_type)

walker = ParseTreeWalker()
listener = BabyDuckCustomListener()
walker.walk(listener, tree)

print(listener.dirfuncs)