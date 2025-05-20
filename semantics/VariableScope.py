from enum import Enum, auto

class VariableScope(Enum):
    GLOBAL = auto()
    LOCAL = auto()
    TEMPORAL = auto()
    CONSTANTS = auto()