from antlr.BabyDuckListener import BabyDuckListener
from semantics.Function import Function
from semantics.FunctionType import FunctionType
from semantics.Variable import Variable
from semantics.VariableType import VariableType
from semantics.VariableScope import VariableScope
from semantics.OperandType import OperandType
from semantics.SemanticCube import SEMANTIC_CUBE
from semantics.QuadrupleStackVariable import QuadrupleStackVariable
from semantics.VirtualDirections import VirtualDirections
from semantics.QuadruplePrintMode import QuadruplePrintMode
from antlr4 import *

class BabyDuckSemanticListener(BabyDuckListener):
    def __init__(self, quadruple_print_mode: QuadruplePrintMode = QuadruplePrintMode.USE_VARIABLE_NAME):
        super().__init__()

        # Variables related with function and variable declarations
        self.dirfuncs: dict[str, Function] = {}
        self.program_id = ""
        self.last_seen_var_ids_stack: list[str] = [] # this is a stack
        self.last_seen_func_id = ""
        self.virtual_directions = VirtualDirections()

        # Variables related with quadruples
        self.quadruples_operands_stack: list[OperandType] = [] # this is a stack
        self.quadruples_variables_stack: list[QuadrupleStackVariable] = [] # this is a stack
        self.quadruples: list[str] = [] # here we'll be storing the final quadruples
        self.quadruple_print_mode = quadruple_print_mode

        # Variables related with conditionals, loops and jumps
        self.quadruple_jumps_stack: list[int] = [] # this is a stack

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
            scope = None
            if self.last_seen_func_id == self.program_id:
                scope = VariableScope.GLOBAL
            else:
                scope = VariableScope.LOCAL
            function_directory.vars[last_seen_var_id] = Variable(listener=self, name=last_seen_var_id, type=var_type, scope=scope)

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
        
        self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, sign=factor_sign, variable=current_var))

    def enterFactor_with_cte(self, ctx):
        # TODO: improve comments
        factor_sign = str(ctx.factor_sign().getText())

        if ctx.cte().CTE_INT():
            # then we know our constant its an integer
            factor_cte = str(ctx.cte().CTE_INT().getText())
            current_var = Variable(listener=self, name=factor_sign + factor_cte, type=VariableType.INT, scope=VariableScope.CONSTANTS)
        elif ctx.cte().CTE_FLOAT():
            # then we know our constant its a float
            factor_cte = str(ctx.cte().CTE_FLOAT().getText())
            current_var = Variable(listener=self, name=factor_sign + factor_cte, type=VariableType.FLOAT, scope=VariableScope.CONSTANTS)
        # TODO: add else here to handle exception
        
        self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=current_var))

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

            semantic_cube_key = (left_var.variable.type, right_var.variable.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.type} and type {right_var.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_var = Variable(listener=self, type=result_type, scope=VariableScope.TEMPORAL)
            quadruple = " ".join([operand.to_symbol(), 
                                   left_var.print(), 
                                   right_var.print(), 
                                   tmp_var.print()])

            self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=tmp_var))
            self.quadruples.append(quadruple)

    def exitFactor(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] in [OperandType.TIMES, OperandType.DIVIDE]:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            semantic_cube_key = (left_var.variable.type, right_var.variable.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.variable.type} and type {right_var.variable.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_var = Variable(listener=self, type=result_type, scope=VariableScope.TEMPORAL)
            quadruple = " ".join([operand.to_symbol(),
                                   left_var.print(), 
                                   right_var.print(), 
                                   tmp_var.print()])

            self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=tmp_var))
            self.quadruples.append(quadruple)
    
    def exitExp(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] in [OperandType.GREATER_THAN, OperandType.LESS_THAN, OperandType.NOT_EQUALS]:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            semantic_cube_key = (left_var.variable.type, right_var.variable.type, operand)
            if semantic_cube_key not in SEMANTIC_CUBE:
                raise Exception(f"ERROR: Unsupported operand {operand} between type {left_var.variable.type} and type {right_var.variable.type}")
            result_type = SEMANTIC_CUBE[semantic_cube_key]

            tmp_var = Variable(listener=self, type=result_type, scope=VariableScope.TEMPORAL)
            quadruple = " ".join([operand.to_symbol(), 
                                   left_var.print(),
                                   right_var.print(), 
                                   tmp_var.print()])

            self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=tmp_var))
            self.quadruples.append(quadruple)

    def enterAssign(self, ctx):
        assign_id = str(ctx.ID().getText())

        variables_directory = self.dirfuncs[self.last_seen_func_id].vars
        current_var = None
        if assign_id in variables_directory:
            current_var = variables_directory[assign_id]
        else:
            raise Exception(f"ERROR: Variable {assign_id} has not been declared")
        
        self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=current_var))
        self.quadruples_operands_stack.append(OperandType.ASSIGN)

    def exitAssign(self, ctx):
        # TODO: comment this better
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.ASSIGN:
            right_var = self.quadruples_variables_stack.pop()
            left_var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            if (left_var.variable.type != right_var.variable.type):
                raise Exception(f"ERROR: Incompatible assignation between type {left_var.type} and type {right_var.type}")

            quadruple = " ".join([operand.to_symbol(), 
                                   right_var.print(), 
                                   left_var.print()])
            self.quadruples.append(quadruple)

    def enterPrint_cte_string(self, ctx):
        # Whenever we see a string, we need to create a constant variable and add it to the quadruples
        current_var = Variable(listener=self, name=str(ctx.CTE_STRING().getText()), type=VariableType.STRING, scope=VariableScope.CONSTANTS)
        self.quadruples_variables_stack.append(QuadrupleStackVariable(listener=self, variable=current_var))

    def enterPrint(self, ctx):
        # Append a print operand to the stack for the following expression
        self.quadruples_operands_stack.append(OperandType.PRINT)
    
    def enterPrint_comma(self, ctx):
        # Parse the previous expression and add it to the quadruples
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.PRINT:
            var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            quadruple = " ".join([operand.to_symbol(), 
                                   var.print()])
            self.quadruples.append(quadruple)
        else:
            #TODO: maybe this is impossible lol
            pass

        # Append a print operand to the stack for the following expression
        self.quadruples_operands_stack.append(OperandType.PRINT)
    
    def enterPrint_right_parenthesis(self, ctx):
        # Parse the previous expression and add it to the quadruples
        if self.quadruples_operands_stack and self.quadruples_operands_stack[-1] == OperandType.PRINT:
            var = self.quadruples_variables_stack.pop()
            operand = self.quadruples_operands_stack.pop()

            quadruple = " ".join([operand.to_symbol(), 
                                   var.print()])
            self.quadruples.append(quadruple)
        else:
            #TODO: maybe this is impossible lol
            pass

    def enterIf_condition_right_parenthesis(self, ctx):
        if self.quadruples_variables_stack:
            var = self.quadruples_variables_stack.pop()

            if var.variable.type != VariableType.BOOLEAN:
                raise Exception(f"ERROR: Incompatible condition type {var.variable.type} for if statement (it should be boolean)")

            quadruple = " ".join([OperandType.GOTO_F.to_symbol(), 
                                    var.print(),
                                    "TO_FILL"])
            
            self.quadruples.append(quadruple)
            self.quadruple_jumps_stack.append(len(self.quadruples) - 1)
            
        # TODO: else, raise exception
    
    def enterIf_condition_else(self, ctx):
        # Create and push the "GOTO" quadruple
        quadruple = " ".join([OperandType.GOTO.to_symbol(), 
                        "TO_FILL"])
        self.quadruples.append(quadruple)
        goto_quadruple_index = len(self.quadruples)-1 # Note how we're not pushing the quadruple index to the stack yet
        
        # Now we're exactly at the start of the else statement
        # We need to fill the "TO_FILL" in the previous quadruple
        if self.quadruple_jumps_stack:
            jump_index = self.quadruple_jumps_stack.pop()
            self.quadruples[jump_index] = self.quadruples[jump_index].replace("TO_FILL", str(len(self.quadruples) + 1))
        else:
            # Throw exception if the stack is empty
            raise Exception("ERROR: Unmatched 'else' encountered. No corresponding 'if' statement was found on the stack.")
        
        # Now we need to create a jump for the "GOTO" quadruple we created at the beginning of this function
        self.quadruple_jumps_stack.append(goto_quadruple_index)

    def enterIf_condition_semi_colon(self, ctx):
        if self.quadruple_jumps_stack:
            # We need to fill the "TO_FILL" in the previous quadruple (either a GOTO - for if-else-statement, or a GOTO_F - for if-statement)
            jump_index = self.quadruple_jumps_stack.pop()
            self.quadruples[jump_index] = self.quadruples[jump_index].replace("TO_FILL", str(len(self.quadruples) + 1))
        else:
            # Throw exception if the stack is empty
            raise Exception("ERROR: Unmatched 'end-if' encountered. No corresponding 'if' statement was found on the stack.")
        
    def enterCycle(self, ctx):
        self.quadruple_jumps_stack.append(len(self.quadruples) + 1)

    def enterCycle_right_parenthesis(self, ctx):
        if self.quadruples_variables_stack:
            var = self.quadruples_variables_stack.pop()

            if var.variable.type != VariableType.BOOLEAN:
                raise Exception(f"ERROR: Incompatible condition type {var.variable.type} for while statement (it should be boolean)")

            quadruple = " ".join([OperandType.GOTO_F.to_symbol(), 
                                    var.print(),
                                    "TO_FILL"])
            
            self.quadruples.append(quadruple)
            self.quadruple_jumps_stack.append(len(self.quadruples) - 1)

    def enterCycle_semi_colon(self, ctx):
        # Save the "GOTO_F" quadruple index
        # TODO: check if the stack is empty
        goto_f_quadruple_index = self.quadruple_jumps_stack.pop()

        # Save the "while_start" quadruple index
        # TODO: check if the stack is empty
        while_start_quadruple_index = self.quadruple_jumps_stack.pop()

        # Create and push the "GOTO" quadruple
        quadruple = " ".join([OperandType.GOTO.to_symbol(), 
                        str(while_start_quadruple_index)])
        self.quadruples.append(quadruple)

        # We need to fill the "TO_FILL" in the previous quadruple (for the GOTO_F statement)
        self.quadruples[goto_f_quadruple_index] = self.quadruples[goto_f_quadruple_index].replace("TO_FILL", str(len(self.quadruples) + 1))        
