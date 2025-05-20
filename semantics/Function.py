from dataclasses import dataclass, field
from semantics.FunctionType import FunctionType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from semantics.BabyDuckSemanticListener import Variable


@dataclass
class Function:
    name: str
    type: FunctionType
    vars: dict[str, 'Variable'] = field(default_factory=dict) # gpt fixed me this
