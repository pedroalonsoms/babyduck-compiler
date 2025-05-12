import os
import pytest
from antlr4 import *
from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener
from semantics.Function import Function
from semantics.FunctionType import FunctionType
from semantics.Variable import Variable
from semantics.VariableType import VariableType

TEST_CASES_DIR = './tests/semantic/test_cases'

def load_test_case(filename: str) -> str:
    """Load the contents of a single test case file."""

    file_path = os.path.join(TEST_CASES_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_and_walk(input_str):
    input_stream = InputStream(input_str)
    lexer = BabyDuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BabyDuckParser(stream)
    tree = parser.programa()
    walker = ParseTreeWalker()
    listener = BabyDuckSemanticListener()
    walker.walk(listener, tree)
    return listener

def test_test_01():
    listener = parse_and_walk(load_test_case("test_01.txt"))
    print(f"DIRFUNCS = {listener.dirfuncs}")
    assert listener.dirfuncs == {
        'pelos': Function(
            name='pelos',
            type=FunctionType.VOID,
            vars={
                'a': Variable(name='a', type=VariableType.INT),
                'k': Variable(name='k', type=VariableType.INT),
                'j': Variable(name='j', type=VariableType.INT),
                'i': Variable(name='i', type=VariableType.INT),
                'y': Variable(name='y', type=VariableType.FLOAT),
                'x': Variable(name='x', type=VariableType.FLOAT),
            }
        ),
        'uno': Function(
            name='uno',
            type=FunctionType.VOID,
            vars={
                'i': Variable(name='i', type=VariableType.INT),
                'x': Variable(name='x', type=VariableType.INT),
            }
        )
    }

def test_test_02():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_02.txt"))
    print(error.value)
    assert str(error.value) == "ERROR: Variable 'k' was already declared on function directory 'pelos'"

def test_test_03():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_03.txt"))
    print(error.value)
    assert str(error.value) == "ERROR: Function 'uno' was already declared"

def test_test_04():
    with pytest.raises(Exception) as error:
        parse_and_walk(load_test_case("test_04.txt"))
    print(error.value)
    assert str(error.value) == "ERROR: Function 'uno' was already declared"

def test_test_05():
    listener = parse_and_walk(load_test_case("test_05.txt"))
    print(f"DIRFUNCS = {listener.dirfuncs}")
    assert listener.dirfuncs == {
        'Test1': Function(
            name='Test1',
            type=FunctionType.VOID,
            vars={
                'global2': Variable(name='global2', type=VariableType.INT),
                'global1': Variable(name='global1', type=VariableType.INT),
                'global3': Variable(name='global3', type=VariableType.FLOAT),
            }
        ),
        'testFunc': Function(
            name='testFunc',
            type=FunctionType.VOID,
            vars={
                'param1': Variable(name='param1', type=VariableType.INT),
                'param2': Variable(name='param2', type=VariableType.FLOAT),
                'local1': Variable(name='local1', type=VariableType.INT),
                'local2': Variable(name='local2', type=VariableType.FLOAT),
            }
        )
    }

def test_test_06():
    listener = parse_and_walk(load_test_case("test_06.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b',
                                   '= 3 c', 
                                   '* b -c t1',
                                   '* t1 8.0 t2',
                                   '+ a t2 t3', 
                                   '= t3 d']

def test_test_07():
    listener = parse_and_walk(load_test_case("test_07.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '< a b t1']

def test_test_08():
    listener = parse_and_walk(load_test_case("test_08.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert listener.quadruples == ['= 1 a', 
                                   '= 2 b', 
                                   '* a b t1', 
                                   '+ 1.0 5 t2', 
                                   '/ t1 t2 t3', 
                                   '+ 8.7 t3 t4', 
                                   '= t4 c']

def test_test_09():
    listener = parse_and_walk(load_test_case("test_09.txt"))
    print("QUADRUPLES:", listener.quadruples)
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
    print(error.value)
    assert str(error.value) == "ERROR: Variable d has not been declared"

def test_test_11():
    listener = parse_and_walk(load_test_case("test_11.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert listener.quadruples == ['= 5 a', 
                                   '= 6 b', 
                                   '+ a b t1', 
                                   '= t1 c', 
                                   'print c', 
                                   '+ 1 2 t2', 
                                   '+ t2 3 t3', 
                                   '* 4 5 t4', 
                                   '+ t3 t4 t5', 
                                   'print t5']

def test_test_12():
    listener = parse_and_walk(load_test_case("test_12.txt"))
    print("QUADRUPLES:", listener.quadruples)
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
                                   '/ a b t6', 
                                   '= t6 c', 
                                   'print c', 
                                   '+ b 1 t7', 
                                   '/ a t7 t8', 
                                   '= t8 c', 
                                   'print c']
    