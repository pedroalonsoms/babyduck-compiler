from antlr.BabyDuckListener import BabyDuckListener
from semantics.Function import Function
from semantics.FunctionType import FunctionType
from semantics.VariableType import VariableType
from semantics.Variable import Variable
from semantics.OperandType import OperandType
from semantics.SemanticCube import SEMANTIC_CUBE
from antlr4 import *

class BabyDuckSemanticListener(BabyDuckListener):
    def __init__(self):
        super().__init__()

        # Variables related with the declaration of functions and variables
        self.dirfuncs: dict[str, Function] = {}
        self.program_id = ""
        self.last_seen_var_ids_stack: list[str] = [] # this is a stack
        self.last_seen_func_id = ""

        # Variables related with quadruples
        self.quadruples_operands_stack: list[OperandType] = [] # this is a stack
        self.quadruples_variables_stack: list[Variable] = [] # this is a stack
        self.quadruples: list[str] = [] # here we'll be storing the final quadruples
        self.quadruples_tmp_var_index = 1 # used for indexes of tmp variables in quadruples

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
        self.last_seen_var_ids_stack.append(var_id)

    def enterVar_type(self, ctx):
        raw_var_type = str(ctx.type_().getText())

        # Detect the variable type
        var_type = None
        # TODO: this shouldn't be hardcoded
        if raw_var_type == "int":
            var_type = VariableType.INT
        elif raw_var_type == "float":
            var_type = VariableType.FLOAT
        else:
            raise Exception(f"ERROR: Unexpected variable type {raw_var_type}")

        # Pop all the seen vars and add them to our var table
        function_directory = self.dirfuncs[self.last_seen_func_id]
        while self.last_seen_var_ids_stack:
            last_seen_var_id = self.last_seen_var_ids_stack.pop()

            # check if variable is already present
            if last_seen_var_id in function_directory.vars:
                raise Exception(f"ERROR: Variable '{last_seen_var_id}' was already declared on function directory '{function_directory.name}'")
            
            # We create the new variable
            function_directory.vars[last_seen_var_id] = Variable(name=last_seen_var_id, type=var_type)

    def enterFactor_with_id(self, ctx):
        # TODO: improve comments
        factor_sign = str(ctx.factor_sign().getText())
        factor_id = str(ctx.ID().getText())

        variables_directory = self.dirfuncs[self.last_seen_func_id].vars
        current_var = None
        if factor_id in variables_directory:
            current_var = variables_directory[factor_id]
        else:
            raise Exception(f"ERROR: Variable {factor_id} has not been declared")
        
        quadruple_var = Variable(factor_sign + current_var.name, current_var.type)
        self.quadruples_variables_stack.append(quadruple_var)

    def enterFactor_with_cte(self, ctx):
        # TODO: improve comments
        factor_sign = str(ctx.factor_sign().getText())

        quadruple_var = None
        if ctx.cte().CTE_INT():
            # then we know our constant its an integer
            factor_cte = str(ctx.cte().CTE_INT().getText())
            quadruple_var = Variable(factor_sign + factor_cte, VariableType.INT)
        elif ctx.cte().CTE_FLOAT():
            # then we know our constant its a float
            factor_cte = str(ctx.cte().CTE_FLOAT().getText())
            quadruple_var = Variable(factor_sign + factor_cte, VariableType.FLOAT)
        # TODO: add else here to handle exception

        self.quadruples_variables_stack.append(quadruple_var)

    def enterTermino_operation(self, ctx):
        if ctx.TIMES():
            self.quadruples_operands_stack.append(OperandType.TIMES)
        elif ctx.DIVIDE():
            self.quadruples_operands_stack.append(OperandType.DIVIDE)
    
    def enterExp_operation(self, ctx):
        if ctx.PLUS():
            self.quadruples_operands_stack.append(OperandType.PLUS)
        elif ctx.MINUS():
            self.quadruples_operands_stack.append(OperandType.MINUS)

    def enterExpression_operation(self, ctx):
        if ctx.GREATER_THAN():
            self.quadruples_operands_stack.append(OperandType.GREATER_THAN)
        elif ctx.LESS_THAN():
            self.quadruples_operands_stack.append(OperandType.LESS_THAN)
        elif ctx.NOT_EQUALS():
            self.quadruples_operands_stack.append(OperandType.NOT_EQUALS)

    def enterFactor_with_parenthesis_left_parenthesis(self, ctx):
        self.quadruples_operands_stack.append(OperandType.LEFT_PARENTHESIS)

    def enterFactor_with_parenthesis_right_parenthesis(self, ctx):
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.LEFT_PARENTHESIS:
            self.quadruples_operands_stack.pop()
        else:
            # TODO: maybe this is impossible lol
            raise Exception(f"ERROR: Cannot process right parenthesis because there's no matching left parenthesis")

    def exitTermino(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] in [OperandType.PLUS, OperandType.MINUS]:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            semantic_cube_key = (left_var.type, right_var.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.type} and type {right_var.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_quadruple_var = "t" + str(self.quadruples_tmp_var_index)
            quadruple = " ".join([operand.to_symbol(), left_var.name, right_var.name, tmp_quadruple_var])
            self.quadruples_variables_stack.append(Variable(tmp_quadruple_var, result_type))

            self.quadruples_tmp_var_index += 1

            self.quadruples.append(quadruple)

    def exitFactor(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] in [OperandType.TIMES, OperandType.DIVIDE]:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            semantic_cube_key = (left_var.type, right_var.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.type} and type {right_var.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_quadruple_var = "t" + str(self.quadruples_tmp_var_index)
            quadruple = " ".join([operand.to_symbol(), left_var.name, right_var.name, tmp_quadruple_var])
            self.quadruples_variables_stack.append(Variable(tmp_quadruple_var, result_type))

            self.quadruples_tmp_var_index += 1

            self.quadruples.append(quadruple)
    
    def exitExp(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] in [OperandType.GREATER_THAN, OperandType.LESS_THAN, OperandType.NOT_EQUALS]:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            semantic_cube_key = (left_var.type, right_var.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.type} and type {right_var.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_quadruple_var = "t" + str(self.quadruples_tmp_var_index)
            quadruple = " ".join([operand.to_symbol(), left_var.name, right_var.name, tmp_quadruple_var])
            self.quadruples_variables_stack.append(Variable(tmp_quadruple_var, result_type))

            self.quadruples_tmp_var_index += 1

            self.quadruples.append(quadruple)

    def enterAssign(self, ctx):
        assign_id = str(ctx.ID().getText())

        variables_directory = self.dirfuncs[self.last_seen_func_id].vars
        current_var = None
        if assign_id in variables_directory:
            current_var = variables_directory[assign_id]
        else:
            raise Exception(f"ERROR: Variable {assign_id} has not been declared")
        
        quadruple_var = Variable(assign_id, current_var.type)
        self.quadruples_variables_stack.append(quadruple_var)
        self.quadruples_operands_stack.append(OperandType.ASSIGN)

    def exitAssign(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.ASSIGN:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            if (left_var.type != right_var.type):
                raise Exception(f"ERROR: Incompatible assignation between type {left_var.type} and type {right_var.type}")

            tmp_quadruple_var = "t" + str(self.quadruples_tmp_var_index)
            quadruple = " ".join([operand.to_symbol(), right_var.name, left_var.name])
            # self.quadruples_variables_stack.append(Variable(tmp_quadruple_var, result_type))

            # WE DON'T REALLY WANT THIS
            # self.quadruples_tmp_var_index += 1

            self.quadruples.append(quadruple)

    def enterPrint(self, ctx):
        self.quadruples_operands_stack.append(OperandType.PRINT)
    
    def exitPrint(self, ctx):
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.PRINT:
            var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            quadruple = " ".join([operand.to_symbol(), var.name])
            # self.quadruples_variables_stack.append(Variable(tmp_quadruple_var, result_type))

            # WE DON'T REALLY WANT THIS
            # self.quadruples_tmp_var_index += 1

            self.quadruples.append(quadruple)
