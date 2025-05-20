from semantics.VariableScope import VariableScope
from semantics.VariableType import VariableType

class VirtualDirections:
    def __init__(self):
        # Variables related with the declaration of functions and variables
        self.map = {
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

    def get_counter(self, scope: VariableScope, type: VariableType):
        """
        Get the counter for a given scope and type.
        """
        return self.map[(scope, type)]["counter"]

    def increment_counter(self, scope: VariableScope, type: VariableType):
        """
        Increment the counter for a given scope and type.
        """
        # If the counter is maxed out, then we can't increment it further
        if self.is_virtual_direction_maxed_out(scope, type):
            raise Exception(f"ERROR: Max variable declarations reached for type '{type}' and scope '{scope}'.")
        else:
            self.map[(scope, type)]["counter"] += 1

    def get_amount_of_variables(self, scope: VariableScope, type: VariableType):
        """
        Get the amount of variables of a given scope and type.
        """
        return self.map[(scope, type)]["counter"] - self.map[(scope, type)]["low"]
    
    def is_virtual_direction_maxed_out(self, scope: VariableScope, type: VariableType):
        return self.map[(scope, type)]["counter"] > self.map[(scope, type)]["high"]

    def get_next_temporal_index(self):
        """
        Get the next temporal index considering all types.
        """
        # Get the next temporal index for all types
        next_temporal_index = (self.get_amount_of_variables(VariableScope.TEMPORAL, VariableType.INT) +
                               self.get_amount_of_variables(VariableScope.TEMPORAL, VariableType.FLOAT) +
                               self.get_amount_of_variables(VariableScope.TEMPORAL, VariableType.BOOLEAN))
        return next_temporal_index
    
    