from antlr.BabyDuckListener import BabyDuckListener
from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from antlr4 import *
from enum import Enum, auto
from dataclasses import dataclass, field

input_stream = FileStream("tests/semantic/test_cases/test_01.txt")  # or use InputStream for strings
lexer = BabyDuckLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = BabyDuckParser(token_stream)

tree = parser.programa()  # Replace `startRule` with your grammar's entry point

class VariableType(Enum):
    INT = auto()
    FLOAT = auto()

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
            raise f"ERROR: Unexpected variable type {raw_var_type}"

        # Pop all the seen vars and add them to our var table
        function_directory = self.dirfuncs[self.last_seen_func_id]
        while self.last_seen_var_ids:
            last_seen_var_id = self.last_seen_var_ids.pop()

            # check if variable is already present
            if last_seen_var_id in function_directory.vars:
                raise f"ERROR: Variable {last_seen_var_id} was already declared on function directory {function_directory.name}"
            
            # We create the new variable
            function_directory.vars[last_seen_var_id] = Variable(name=last_seen_var_id, type=var_type)

walker = ParseTreeWalker()
listener = BabyDuckCustomListener()
walker.walk(listener, tree)

print(listener.dirfuncs)