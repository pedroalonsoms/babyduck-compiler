import os
import pytest
from antlr4 import *
from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener, Variable
from semantics.Function import Function
from semantics.FunctionType import FunctionType
from semantics.VariableType import VariableType
from semantics.VariableScope import VariableScope
from semantics.QuadruplePrintMode import QuadruplePrintMode

TEST_CASES_DIR = './tests/semantic/test_cases'

def load_test_case(filename: str) -> str:
    """Load the contents of a single test case file."""

    file_path = os.path.join(TEST_CASES_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_and_walk(input_str, quadruple_print_mode: QuadruplePrintMode = QuadruplePrintMode.USE_VARIABLE_NAME):
    input_stream = InputStream(input_str)
    lexer = BabyDuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BabyDuckParser(stream)
    tree = parser.programa()
    walker = ParseTreeWalker()
    listener = BabyDuckSemanticListener(quadruple_print_mode=quadruple_print_mode)
    walker.walk(listener, tree)
    return listener

def test_test_01():
    listener = parse_and_walk(load_test_case("test_01.txt"))
    assert listener.dirfuncs == {
        'pelos': Function(
            name='pelos',
            type=FunctionType.VOID,
            vars={
                'a': Variable(listener=listener, name='a', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_000),
                'k': Variable(listener=listener, name='k', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_001),
                'j': Variable(listener=listener, name='j', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_002),
                'i': Variable(listener=listener, name='i', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_003),
                'y': Variable(listener=listener, name='y', type=VariableType.FLOAT, scope=VariableScope.GLOBAL, virtual_direction=5_000),
                'x': Variable(listener=listener, name='x', type=VariableType.FLOAT, scope=VariableScope.GLOBAL, virtual_direction=5_001),
            }
        ),
        'uno': Function(
            name='uno',
            type=FunctionType.VOID,
            vars={
                # TODO: fix this stuff
                'i': Variable(listener=listener, name='i', type=VariableType.INT, scope=VariableScope.LOCAL, virtual_direction=9_000),
                'x': Variable(listener=listener, name='x', type=VariableType.INT, scope=VariableScope.LOCAL, virtual_direction=9_001),
            }
        )
    }

def test_test_02():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_02.txt"))
    assert str(error.value) == "ERROR: Variable 'k' was already declared on function directory 'pelos'"

def test_test_03():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_03.txt"))
    assert str(error.value) == "ERROR: Function 'uno' was already declared"

def test_test_04():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_04.txt"))
    assert str(error.value) == "ERROR: Function 'uno' was already declared"

def test_test_05():
    listener = parse_and_walk(load_test_case("test_05.txt"))
    assert listener.dirfuncs == {
        'Test1': Function(
            name='Test1',
            type=FunctionType.VOID,
            vars={
                'global2': Variable(listener=listener, name='global2', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_000),
                'global1': Variable(listener=listener, name='global1', type=VariableType.INT, scope=VariableScope.GLOBAL, virtual_direction=1_001),
                'global3': Variable(listener=listener, name='global3', type=VariableType.FLOAT, scope=VariableScope.GLOBAL, virtual_direction=5_000),
            }
        ),
        'testFunc': Function(
            name='testFunc',
            type=FunctionType.VOID,
            vars={
                'param2': Variable(listener=listener, name='param2', type=VariableType.FLOAT, scope=VariableScope.LOCAL, virtual_direction=13_000),
                'param1': Variable(listener=listener, name='param1', type=VariableType.INT, scope=VariableScope.LOCAL, virtual_direction=9_000),
                'local1': Variable(listener=listener, name='local1', type=VariableType.INT, scope=VariableScope.LOCAL, virtual_direction=9_001),
                'local2': Variable(listener=listener, name='local2', type=VariableType.FLOAT, scope=VariableScope.LOCAL, virtual_direction=13_001),
            }
        )
    }

def test_test_06():
    listener = parse_and_walk(load_test_case("test_06.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b',
                                   '= 3 c', 
                                   '* b -c t1',
                                   '* t1 8.0 t2',
                                   '+ a t2 t3', 
                                   '= t3 d']

def test_test_07():
    listener = parse_and_walk(load_test_case("test_07.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '< a b t1',
                                   'GOTO_F t1 5']

def test_test_08():
    listener = parse_and_walk(load_test_case("test_08.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '* a b t1', 
                                   '+ 1.0 5 t2', 
                                   '/ t1 t2 t3', 
                                   '+ 8.7 t3 t4', 
                                   '= t4 c']

def test_test_09():
    listener = parse_and_walk(load_test_case("test_09.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '* a b t1', 
                                   '+ 1.0 5 t2', 
                                   '/ t1 t2 t3', 
                                   '+ 8.7 t3 t4',
                                   '= t4 c']

def test_test_10():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_10.txt"))
    assert str(error.value) == "ERROR: Variable d has not been declared"

def test_test_11():
    listener = parse_and_walk(load_test_case("test_11.txt"))
    assert listener.quadruples == ['= 5 a', 
                                   '= 6 b', 
                                   '+ a b t1', 
                                   '= t1 c', 
                                   'PRINT c', 
                                   '+ 1 2 t2', 
                                   '+ t2 3 t3', 
                                   '* 4 5 t4', 
                                   '+ t3 t4 t5', 
                                   'PRINT t5']

def test_test_12():
    listener = parse_and_walk(load_test_case("test_12.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '* a b t1', 
                                   '+ 1.0 5 t2', 
                                   '/ t1 t2 t3',
                                   '+ 8.7 t3 t4', 
                                   '= t4 c', 
                                   '= 5 a', 
                                   '= 6 b', 
                                   '< a b t5',
                                   'GOTO_F t5 16',
                                   '/ a b t6', 
                                   '= t6 c', 
                                   'PRINT c',
                                   'GOTO 20',
                                   '+ b 1 t7', 
                                   '/ a t7 t8', 
                                   '= t8 c', 
                                   'PRINT c']

def test_test_13():
    listener = parse_and_walk(load_test_case("test_13.txt"))
    assert listener.quadruples == ['= 1 A', 
                                   '= 2 B', 
                                   '= 3 C', 
                                   '= 4 D', 
                                   '> A B t1', 
                                   'GOTO_F t1 16', 
                                   '* C D t2', 
                                   '= t2 B', 
                                   '+ C D t3', 
                                   '> B t3 t4', 
                                   'GOTO_F t4 15', 
                                   '+ A B t5', 
                                   '= t5 C', 
                                   'PRINT B', 
                                   'GOTO 24', 
                                   '+ A B t6', 
                                   '= t6 C', 
                                   '> A C t7', 
                                   'GOTO_F t7 24', 
                                   '+ B A t8', 
                                   '= t8 D', 
                                   '+ A B t9', 
                                   'PRINT t9', 
                                   '* D A t10', 
                                   '- B t10 t11', 
                                   '= t11 C']

def test_test_14():
    listener = parse_and_walk(load_test_case("test_14.txt"))
    assert listener.quadruples == ['= 1 A', 
                                   '= 6 B', 
                                   '< A B t1', 
                                   'GOTO_F t1 8', 
                                   '+ A 1 t2', 
                                   '= t2 A', 
                                   'GOTO 3']

def test_test_15():
    listener = parse_and_walk(load_test_case("test_15.txt"))
    # TODO: check that this is actually correct
    assert listener.quadruples == [
                                '= 1.0 A', 
                                '= 2.0 B', 
                                '= 3.0 C', 
                                '= 4.0 D', 
                                '= 5.0 E',
                                '= 6.0 F', 
                                '= 7.0 G', 
                                '= 8.0 H', 
                                '= 9.0 J', 
                                '= 10.0 K', 
                                '/ E F t1', 
                                '- D t1 t2', 
                                '* C t2 t3', 
                                '* t3 H t4', 
                                '+ B t4 t5', 
                                '= t5 A', 
                                '- E F t6', 
                                '= t6 B', 
                                '* A B t7', 
                                '- t7 C t8', 
                                '* D E t9', 
                                '+ G H t10',
                                '/ t9 t10 t11', 
                                '> t8 t11 t12', 
                                'GOTO_F t12 55', 
                                '* J K t13', 
                                '+ t13 B t14', 
                                '= t14 H', 
                                '< B H t15', 
                                'GOTO_F t15 45', 
                                '+ H J t16', 
                                '= t16 B', 
                                '+ A C t17', 
                                '> B t17 t18', 
                                'GOTO_F t18 44', 
                                '* B C t19', 
                                '+ A t19 t20', 
                                'PRINT t20',
                                '- D E t21', 
                                'PRINT t21',
                                '- B J t22', 
                                '= t22 B', 
                                'GOTO 33', 
                                'GOTO 54', 
                                '- A D t23', 
                                '+ C B t24', 
                                '< t23 t24 t25', 
                                'GOTO_F t25 54', 
                                '+ A B t26', 
                                '= t26 A', 
                                '- B D t27', 
                                'PRINT t27', 
                                'GOTO 45', 
                                'GOTO 19', 
                                '+ A B t28',
                                '= t28 F']

def test_test_16():
    listener = parse_and_walk(load_test_case("test_16.txt"))
    # TODO: check that this is actually correct
    assert listener.quadruples == ['= 1.0 A', 
                                   '= 2.0 B', 
                                   '+ A B t1', 
                                   'PRINT t1', 
                                   '* A B t2', 
                                   'PRINT t2']
    
def test_test_16():
    listener = parse_and_walk(load_test_case("test_16.txt"))
    assert listener.quadruples == ['= 1.0 A', 
                                   '= 2.0 B', 
                                   '+ A B t1', 
                                   'PRINT t1', 
                                   '* A B t2', 
                                   'PRINT t2']
    
def test_test_17():
    listener = parse_and_walk(load_test_case("test_17.txt"))
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '= 3 c', 
                                   '* b -c t1', 
                                   '* t1 8.0 t2', 
                                   '+ a t2 t3', 
                                   '= t3 d', 
                                   '< a b t4',
                                   'GOTO_F t4 11', 
                                   'PRINT "HELLO WORLD"']
    
    virtual_direction_listener = parse_and_walk(load_test_case("test_17.txt"), quadruple_print_mode=QuadruplePrintMode.USE_VIRTUAL_DIRECTION)
    assert virtual_direction_listener.quadruples == ['8 29000 1002', 
                                                     '8 29001 1001',
                                                     '8 29002 1000',
                                                     '3 1001 -1000 17000',
                                                     '3 17000 33000 21000',
                                                     '1 1002 21000 21001',
                                                     '8 21001 5000',
                                                     '6 1002 1001 25000',
                                                     '12 25000 11',
                                                     '11 37000']
