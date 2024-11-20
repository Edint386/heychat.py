# element.py

from abc import ABC, abstractmethod
from typing import Dict, Union
from .interface import Types


class _Element(ABC):
    """Abstract base class for elements."""

    @abstractmethod
    def _repr(self) -> Dict:
        pass


class Element:
    """Namespace for element classes."""

    class Text(_Element):
        """Text element."""

        def __init__(self, content: str, type: Types.Text = Types.Text.MD):
            self.type = type
            self.content = content

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "text": self.content
            }

    class Image(_Element):
        """Image element."""

        def __init__(self, url: str, size: Types.Size = Types.Size.MEDIUM):
            self.type = Types._Element.IMAGE
            self.url = url
            self.size = size

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "url": self.url,
                "size": self.size.value,
            }

    class Button(_Element):
        """Button element."""

        def __init__(self,
                     text: str,
                     value: str = '',
                     event: Types.Event = Types.Event.SERVER,
                     theme: Types.Theme = Types.Theme.SUCCESS):
            self.type = Types._Element.BUTTON
            self.text = text
            self.value = value
            self.event = event
            self.theme = theme

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "text": self.text,
                "value": self.value,
                "event": self.event.value,
                "theme": self.theme.value
            }