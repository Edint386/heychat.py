# interface.py

from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, Dict, List


class Types:
    """Define various types for elements and modules."""

    class Theme(Enum):
        DEFAULT = "default" # grey
        PRIMARY = "primary" # blue
        SUCCESS = "success" # green
        DANGER = "danger" # red


    class Size(Enum):
        SMALL = "small"
        MEDIUM = "medium"
        LARGE = "large"

    class _Element(Enum):
        PLAIN_TEXT = "plain-text"
        KMARKDOWN = "kmarkdown"
        IMAGE = "image"
        BUTTON = "button"

    class _Module(Enum):
        SECTION = "section"
        HEADER = "header"
        DIVIDER = "divider"
        IMAGE_GROUP = "images"
        BUTTON_GROUP = "button-group"
        COUNTDOWN = "countdown"


    class Event(Enum):
        LINK = "link-to"
        SERVER = "server"
        INTERNAL = "internal"

    class Text(Enum):
        PLAIN = "plain-text"
        MD = "markdown"

    class CountdownMode(Enum):
        DEFAULT = "default"
        CALENDER = "calender"
        SECOND = "second"


def _get_repr(item) -> Union[str, Dict, List]:
    """A helper function for serialization."""
    if hasattr(item, '_repr'):
        return item._repr()
    elif isinstance(item, list):
        return [_get_repr(i) for i in item]
    else:
        return item

