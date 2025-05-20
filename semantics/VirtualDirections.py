from semantics.VariableScope import VariableScope
from semantics.VariableType import VariableType

class VirtualDirections:
    # Variables related with the declaration of functions and variables
    map = {
        (VariableScope.GLOBAL, VariableType.INT): {"low": 1_000, "high": 4_999, "counter": 1_000},
        (VariableScope.GLOBAL, VariableType.FLOAT): {"low": 5_000, "high": 8_999, "counter": 5_000},

        (VariableScope.LOCAL, VariableType.INT): {"low": 9_000, "high": 12_999, "counter": 9_000},
        (VariableScope.LOCAL, VariableType.FLOAT): {"low": 13_000, "high": 16_999, "counter": 13_000},

        (VariableScope.TEMPORAL, VariableType.INT): {"low": 17_000, "high": 20_999, "counter": 17_000},
        (VariableScope.TEMPORAL, VariableType.FLOAT): {"low": 21_000, "high": 24_999, "counter": 21_000},
        (VariableScope.TEMPORAL, VariableType.BOOLEAN): {"low": 25_000, "high": 28_999, "counter": 25_000},

        (VariableScope.CONSTANTS, VariableType.INT): {"low": 29_000, "high": 32_999, "counter": 29_000},
        (VariableScope.CONSTANTS, VariableType.FLOAT): {"low": 33_000, "high": 36_999, "counter": 33_000},
        (VariableScope.CONSTANTS, VariableType.STRING): {"low": 37_000, "high": 40_999, "counter": 37_000},
    }

    @staticmethod
    def reset_counters():
        for key, value in VirtualDirections.map.items():
            value["counter"] = value["low"]
    