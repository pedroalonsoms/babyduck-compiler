from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from semantics.BabyDuckSemanticListener import Variable

@dataclass
class QuadrupleStackVariable:
    variable: 'Variable'
    sign: Optional[str] = None

    def print(self, use_variable_name=False):
      if use_variable_name:
          return (self.sign if self.sign else "") + self.variable.name
      return (self.sign if self.sign else "") + self.variable.virtual_direction
