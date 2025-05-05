from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener
from antlr4 import *
import os
import pytest

def main():
    # Leemos todos los test-cases adentro del folder
    folder_path = './tests/semantic/test_cases'
    for filename in os.listdir(folder_path): # Por cada archivo
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Leemos los contenidos de ese test-file
            test_input = file.read()

            # Lo metemos a los files del baby-duck generados por ANTLR
            input_stream = InputStream(test_input)
            lexer = BabyDuckLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = BabyDuckParser(stream)

            tree = parser.programa()  # 'programa' es nuestra "startRule"

            walker = ParseTreeWalker()
            listener = BabyDuckSemanticListener()
            if filename == "test_02.txt":
                with pytest.raises(Exception) as error:
                    walker.walk(listener, tree)
                
                assert str(error.value) == "ERROR: Variable 'k' was already declared on function directory 'pelos'"
                print("ARCHIVO = ", file_path, "TUVO UN ERROR: ", str(error.value))
            elif filename == "test_03.txt":
                with pytest.raises(Exception) as error:
                    walker.walk(listener, tree)
                
                assert str(error.value) == "ERROR: Function 'uno' was already declared"
                print("ARCHIVO = ", file_path, "TUVO UN ERROR: ", str(error.value))
            elif filename == "test_04.txt":
                with pytest.raises(Exception) as error:
                    walker.walk(listener, tree)
                
                assert str(error.value) == "ERROR: Function 'uno' was already declared"
                print("ARCHIVO = ", file_path, "TUVO UN ERROR: ", str(error.value))
            else:
                walker.walk(listener, tree)

                # Imprimir el directorio de funciones
                print("ARCHIVO = ", file_path, "DIRECTORIO DE FUNCIONES = ", listener.dirfuncs)
            
            print()

if __name__ == "__main__":
    main()