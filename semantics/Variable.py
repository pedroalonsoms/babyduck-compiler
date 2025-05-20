from dataclasses import dataclass
from typing import Optional
from semantics.QuadruplePrintMode import QuadruplePrintMode
from semantics.VariableScope import VariableScope
from semantics.VariableType import VariableType
from typing import TYPE_CHECKING

# We only want to import the type
if TYPE_CHECKING:
    from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener 

@dataclass
class Variable:
    listener: 'BabyDuckSemanticListener' # we need this to access the virtual directions (dependency injection)
    type: VariableType
    scope: VariableScope
    virtual_direction: Optional[int] = None
    name: Optional[str] = None

    def __post_init__(self):
        # Assign a virtual direction if not already assigned via the constructor
        if self.virtual_direction == None:
            # Check that it exists in the virtual direction map
            if (self.scope, self.type) in self.listener.virtual_directions.map:
                # Get a copy of the counter
                self.virtual_direction = self.listener.virtual_directions.get_counter(self.scope, self.type)
                
                # Increment the counter for the next variable
                self.listener.virtual_directions.increment_counter(self.scope, self.type)
            else:
                raise Exception(f"ERROR: Variable of scope '{self.scope}' and type '{self.type}' is not supported")
        
        # Assign a name if not assigned via the constructor
        if self.name == None:
            # For temporary variables we need to automatically set the name (t1, t2, t3, t4, ...)
            if self.scope == VariableScope.TEMPORAL:
                tmp_var_subindex = self.listener.virtual_directions.get_next_temporal_index()
                self.name = "t" + str(tmp_var_subindex)
    
    def print(self):
      if self.listener.quadruple_print_mode == QuadruplePrintMode.USE_VARIABLE_NAME:
          return self.name
      return str(self.virtual_direction)