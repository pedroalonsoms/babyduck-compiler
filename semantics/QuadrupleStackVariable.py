from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING
from semantics.QuadruplePrintMode import QuadruplePrintMode
if TYPE_CHECKING:
    from semantics.BabyDuckSemanticListener import BabyDuckSemanticListener, Variable

@dataclass
class QuadrupleStackVariable:
    listener: 'BabyDuckSemanticListener'
    variable: 'Variable'
    sign: Optional[str] = None

    def print(self):
      if self.listener.quadruple_print_mode == QuadruplePrintMode.USE_VARIABLE_NAME:
          return (self.sign if self.sign else "") + self.variable.name
      return (self.sign if self.sign else "") + str(self.variable.virtual_direction)
