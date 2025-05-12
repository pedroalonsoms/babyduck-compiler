import os
import pytest
from antlr4 import *
from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener

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
    assert listener.dirfuncs is not None

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
    print(f"DIRFUNCS = {listener.dirfuncs}")
    assert listener.dirfuncs is not None

def test_test_06():
    listener = parse_and_walk(load_test_case("test_06.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert len(listener.quadruples) > 0

def test_test_07():
    listener = parse_and_walk(load_test_case("test_07.txt"))
    print("QUADRUPLES:", listener.quadruples)
    assert len(listener.quadruples) > 0