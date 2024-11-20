# module.py

from abc import ABC, abstractmethod
from typing import List, Union, Dict
from .element import Element, _Element
from .interface import Types


class _Module(ABC):
    """Abstract base class for modules."""

    @abstractmethod
    def _repr(self) -> Dict:
        pass


class Module:
    """Namespace for module classes."""

    class Header(_Module):
        """Header module."""

        def __init__(self, text: Union[Element.Text, str]):
            self.type = Types._Module.HEADER
            if isinstance(text, str):
                text = Element.Text(text, type=Types.Text.MD)
            self.text = text

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "content": self.text._repr()
            }

    class Section(_Module):
        """Section module."""

        def __init__(self,
                     *elements: Union[Element.Text, Element.Image, Element.Button, str]):
            self.elements: List[_Element] = []
            self.type = Types._Module.SECTION
            for element in elements:
                if isinstance(element, str):
                    self.elements.append(Element.Text(element))
                else:
                    self.elements.append(element)
            # 按钮/图片 不能和多个文本混合
            if len(self.elements) > 1:
                if any([isinstance(element, (Element.Image, Element.Button)) for element in self.elements]):
                    raise ValueError("Image/Button cannot be mixed with multiple text elements")

        def _repr(self) -> Dict:

            data = {
                "type": self.type.value,
                "paragraph": [element._repr() for element in self.elements]
            }
            return data

    class Divider(_Module):
        """Divider module."""

        def __init__(self, text: str = None):
            self.type = Types._Module.DIVIDER
            self.text = text

        def _repr(self) -> Dict:
            data = {"type": self.type.value}
            if self.text:
                data["text"] = self.text
            return data

    class ImageGroup(_Module):
        """Images module."""

        def __init__(self, *elements: Union[Element.Image, str]):
            self.type = Types._Module.IMAGE_GROUP
            self.elements = [Element.Image(element) if isinstance(element, str) else element
                             for element in elements]

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "elements": [element._repr() for element in self.elements]
            }

    class ButtonGroup(_Module):
        """Buttons module."""

        def __init__(self, *elements: Element.Button):
            self.type = Types._Module.BUTTON_GROUP
            self.elements = elements

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "btns": [element._repr() for element in self.elements]
            }

    class Countdown(_Module):
        """Countdown module."""

        def __init__(self, end_time: Union[int, float], mode: Union[Types.CountdownMode, str] = Types.CountdownMode.SECOND):
            self.type = Types._Module.COUNTDOWN
            self.mode = Types.CountdownMode(mode) if isinstance(mode, str) else mode
            self.end_time = int(end_time)

        def _repr(self) -> Dict:
            return {
                "type": self.type.value,
                "mode": self.mode.value,
                "end_time": self.end_time
            }



