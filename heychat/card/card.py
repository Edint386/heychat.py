# card.py

from typing import List, Optional, Dict
from .module import _Module
from .interface import Types


class Card:
    """Card class for heychat.py card messages."""

    def __init__(self,
                 *modules: _Module,
                 color: Optional[str] = "#f7f7f8",
                 theme: Optional[Types.Theme] = None,
                 size: Types.Size = Types.Size.LARGE):
        self.type = "card"
        self.color = color
        self.theme = theme
        self.size = size
        self.modules: List[_Module] = list(modules)

    def append(self, module: _Module):
        self.modules.append(module)

    def _repr(self) -> Dict:
        data = {
            "type": self.type,
            "modules": [module._repr() for module in self.modules]
        }
        if self.color:
            data["color"] = self.color
        if self.theme:
            data["theme"] = self.theme.value
        if self.size:
            data["size"] = self.size.value
        return data