from antlr.BabyDuckListener import BabyDuckListener
from semantics.Function import Function
from semantics.FunctionType import FunctionType
from semantics.VariableType import VariableType
from semantics.Variable import Variable
from antlr4 import *

class BabyDuckSemanticListener(BabyDuckListener):
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