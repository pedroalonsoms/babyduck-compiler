from dataclasses import dataclass
from semantics.VariableType import VariableType

@dataclass
class Variable:
    name: str
    type: VariableType