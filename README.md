# babyduck-compiler
A compiler written in python for the babyduck programming language, from scratch.

How to run on MacOS (you need both java and python)
```bash
brew install openjdk

python3 -m venv env
soruce /env/bin/activate
pip install antlr4-tools
pip install antlr4-python3-runtime
```

Compile Python files
```bash
antlr4 -Dlanguage=Python3 BabyDuck.g4 -o antlr
```

Create GUI
```bash
antlr4-parse BabyDuck.g4 programa -gui tests/syntax/test_cases/test_01.txt
```

```python
python main.py
```

Run tests
```python
pytest -s -v semantic_test.py
```