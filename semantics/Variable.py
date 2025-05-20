from dataclasses import dataclass
from typing import Optional
from semantics.VirtualDirections import VirtualDirections
from semantics.VariableScope import VariableScope
from semantics.VariableType import VariableType

@dataclass
class Variable:
    type: VariableType
    scope: VariableScope
    virtual_direction: Optional[int] = None
    name: Optional[str] = None

    def __post_init__(self):
        # Assign a virtual direction if not already assigned via the constructor
        if self.virtual_direction == None:
            # Check that it exists in the virtual direction map
            if (self.scope, self.type) in VirtualDirections.map:
                
                # If the counter is maxed out, then we can't increment it further
                if VirtualDirections.map[(self.scope, self.type)]["counter"] > VirtualDirections.map[(self.scope, self.type)]["high"]:
                    raise Exception(f"ERROR: Variable '{self.name}' can not be declared. Max variable declarations reached for type '{self.type}' and scope '{self.scope}'.")
                else:
                    # Get a copy of the counter
                    self.virtual_direction = VirtualDirections.map[(self.scope, self.type)]["counter"]
                    
                    # Increment the counter for the next variable
                    VirtualDirections.map[(self.scope, self.type)]["counter"] += 1
            else:
                raise Exception(f"ERROR: Variable of scope '{self.scope}' and type '{self.type}' is not supported")
        
        # Assign a name if not assigned via the constructor
        if self.name == None:
            # For temporary variables we need to automatically set the name (t1, t2, t3, t4, ...)
            if self.scope == VariableScope.TEMPORAL:
                tmp_var_subindex = VirtualDirections.map[(self.scope, self.type)]["counter"] - VirtualDirections.map[(self.scope, self.type)]["low"]
                print("PEDRO", tmp_var_subindex)
                self.name = "t" + str(tmp_var_subindex)
    
    def print(self, use_variable_name):
      if use_variable_name:
          return self.name
      return self.virtual_direction