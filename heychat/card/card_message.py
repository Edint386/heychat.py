# card_message.py

from typing import List, Union, Dict
from .card import Card
from .interface import _get_repr

class CardMessage(dict):
    """
    CardMessage class that inherits from list and can be serialized using json.dumps.
    """

    def __init__(self, *cards: Card):
        super().__init__()
        self['data'] = [_get_repr(card) for card in cards]

    def append(self, card: Card):
        """Append a card to the message."""
        self['data'].append(_get_repr(card))

    def __iter__(self):
        """Override __iter__ to return the serialized representation of the cards."""
        for card in super().__iter__():
            yield _get_repr(card)