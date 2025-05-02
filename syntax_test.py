from antlr.BabyDuckLexer import BabyDuckLexer
from antlr.BabyDuckParser import BabyDuckParser
from antlr4 import *
import os

def main():
    # Leemos todos los test-cases adentro del folder
    folder_path = './tests/syntax/test_cases'
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

            # Imprimir árbol de sintáxis
            print("ARCHIVO = ", file_path, "ARBOL DE SINTAXIS = ", tree.toStringTree(recog=parser))
            print()

if __name__ == "__main__":
    main()