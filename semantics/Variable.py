from dataclasses import dataclass, field
from semantics.VariableType import VariableType

@dataclass
class Variable:
    name: str
    type: VariableType