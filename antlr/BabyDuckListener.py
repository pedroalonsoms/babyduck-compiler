# Generated from BabyDuck.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .BabyDuckParser import BabyDuckParser
else:
    from BabyDuckParser import BabyDuckParser

# This class defines a complete listener for a parse tree produced by BabyDuckParser.
class BabyDuckListener(ParseTreeListener):

    # Enter a parse tree produced by BabyDuckParser#epsilon.
    def enterEpsilon(self, ctx:BabyDuckParser.EpsilonContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#epsilon.
    def exitEpsilon(self, ctx:BabyDuckParser.EpsilonContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#program_id.
    def enterProgram_id(self, ctx:BabyDuckParser.Program_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#program_id.
    def exitProgram_id(self, ctx:BabyDuckParser.Program_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#main.
    def enterMain(self, ctx:BabyDuckParser.MainContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#main.
    def exitMain(self, ctx:BabyDuckParser.MainContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#programa.
    def enterPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#programa.
    def exitPrograma(self, ctx:BabyDuckParser.ProgramaContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#dec_vars.
    def enterDec_vars(self, ctx:BabyDuckParser.Dec_varsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#dec_vars.
    def exitDec_vars(self, ctx:BabyDuckParser.Dec_varsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#dec_funcs.
    def enterDec_funcs(self, ctx:BabyDuckParser.Dec_funcsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#dec_funcs.
    def exitDec_funcs(self, ctx:BabyDuckParser.Dec_funcsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#var_id.
    def enterVar_id(self, ctx:BabyDuckParser.Var_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#var_id.
    def exitVar_id(self, ctx:BabyDuckParser.Var_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#var_type.
    def enterVar_type(self, ctx:BabyDuckParser.Var_typeContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#var_type.
    def exitVar_type(self, ctx:BabyDuckParser.Var_typeContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#vars.
    def enterVars(self, ctx:BabyDuckParser.VarsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#vars.
    def exitVars(self, ctx:BabyDuckParser.VarsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#vars_content.
    def enterVars_content(self, ctx:BabyDuckParser.Vars_contentContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#vars_content.
    def exitVars_content(self, ctx:BabyDuckParser.Vars_contentContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#mas_vars_content.
    def enterMas_vars_content(self, ctx:BabyDuckParser.Mas_vars_contentContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#mas_vars_content.
    def exitMas_vars_content(self, ctx:BabyDuckParser.Mas_vars_contentContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#list_id.
    def enterList_id(self, ctx:BabyDuckParser.List_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#list_id.
    def exitList_id(self, ctx:BabyDuckParser.List_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#type.
    def enterType(self, ctx:BabyDuckParser.TypeContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#type.
    def exitType(self, ctx:BabyDuckParser.TypeContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#func_id.
    def enterFunc_id(self, ctx:BabyDuckParser.Func_idContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#func_id.
    def exitFunc_id(self, ctx:BabyDuckParser.Func_idContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#funcs.
    def enterFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#funcs.
    def exitFuncs(self, ctx:BabyDuckParser.FuncsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#list_params.
    def enterList_params(self, ctx:BabyDuckParser.List_paramsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#list_params.
    def exitList_params(self, ctx:BabyDuckParser.List_paramsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#body.
    def enterBody(self, ctx:BabyDuckParser.BodyContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#body.
    def exitBody(self, ctx:BabyDuckParser.BodyContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#dec_statement.
    def enterDec_statement(self, ctx:BabyDuckParser.Dec_statementContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#dec_statement.
    def exitDec_statement(self, ctx:BabyDuckParser.Dec_statementContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#statement.
    def enterStatement(self, ctx:BabyDuckParser.StatementContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#statement.
    def exitStatement(self, ctx:BabyDuckParser.StatementContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#assign.
    def enterAssign(self, ctx:BabyDuckParser.AssignContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#assign.
    def exitAssign(self, ctx:BabyDuckParser.AssignContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#condition.
    def enterCondition(self, ctx:BabyDuckParser.ConditionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#condition.
    def exitCondition(self, ctx:BabyDuckParser.ConditionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cycle.
    def enterCycle(self, ctx:BabyDuckParser.CycleContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cycle.
    def exitCycle(self, ctx:BabyDuckParser.CycleContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#f_call.
    def enterF_call(self, ctx:BabyDuckParser.F_callContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#f_call.
    def exitF_call(self, ctx:BabyDuckParser.F_callContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#list_expression.
    def enterList_expression(self, ctx:BabyDuckParser.List_expressionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#list_expression.
    def exitList_expression(self, ctx:BabyDuckParser.List_expressionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#print.
    def enterPrint(self, ctx:BabyDuckParser.PrintContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#print.
    def exitPrint(self, ctx:BabyDuckParser.PrintContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#print_args.
    def enterPrint_args(self, ctx:BabyDuckParser.Print_argsContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#print_args.
    def exitPrint_args(self, ctx:BabyDuckParser.Print_argsContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#expression.
    def enterExpression(self, ctx:BabyDuckParser.ExpressionContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#expression.
    def exitExpression(self, ctx:BabyDuckParser.ExpressionContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#exp.
    def enterExp(self, ctx:BabyDuckParser.ExpContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#exp.
    def exitExp(self, ctx:BabyDuckParser.ExpContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#termino.
    def enterTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#termino.
    def exitTermino(self, ctx:BabyDuckParser.TerminoContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#factor.
    def enterFactor(self, ctx:BabyDuckParser.FactorContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#factor.
    def exitFactor(self, ctx:BabyDuckParser.FactorContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#factor_sign.
    def enterFactor_sign(self, ctx:BabyDuckParser.Factor_signContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#factor_sign.
    def exitFactor_sign(self, ctx:BabyDuckParser.Factor_signContext):
        pass


    # Enter a parse tree produced by BabyDuckParser#cte.
    def enterCte(self, ctx:BabyDuckParser.CteContext):
        pass

    # Exit a parse tree produced by BabyDuckParser#cte.
    def exitCte(self, ctx:BabyDuckParser.CteContext):
        pass



del BabyDuckParser