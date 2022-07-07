"""
The card module holds the Face and Rank enum classes, along with the
Card and Deck data classes.
"""
import secrets
from dataclasses import dataclass, field
from enum import IntEnum, Enum
from itertools import product
from typing import Final, Union
from uuid import uuid4


class Rank(IntEnum):
    """
    Rank Enum class holds the card ranks from Ace through to King.
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def is_picture_card(self) -> bool:
        """
        To determine if the Card is a picture card or not.

        :return: True if the card is an ACE, JACK, QUEEN, or KING, otherwise
            False.
        """
        return self.value in [1, 10, 11, 12, 13]

    @property
    def abbreviation(self) -> str:
        """
        An abbreviation of the Rank. Cards 2 through to 10 are
        returned as their value as a string, whereas ACE, JACK, QUEEN,
        and KING are returned as the first character of their name.

        :return: An abbreviated Rank name.
        """
        if (self.value >= 2) and (self.value <= 10):
            return str(self.value)
        return self.name[0]


class Face(IntEnum):
    """
    Face Enum class to hold the four card faces.
    """

    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4

    @property
    def colour(self) -> str:
        """
        The Face colour.

        :return: red if the Face is DIAMOND or HEART, otherwise black.
        """
        if self is Face.DIAMOND or self is Face.HEART:
            return "red"
        return "black"

    @property
    def symbol(self) -> str:
        """
        The Face symbol.

        :return: Returns the card face symbol as a string.
        """
        if self is Face.CLUB:
            return "♣"
        elif self is Face.DIAMOND:
            return "♦"
        elif self is Face.HEART:
            return "♥"
        elif self is Face.SPADE:
            return "♠"


@dataclass(frozen=True)
class Card:
    """
    The Card class is a frozen dataclass that takes a Rank and a
    Face. Each instance of Card is assigned an uuid as a string.
    """

    rank: Rank
    face: Face
    uuid: str = field(default_factory=lambda: str(uuid4()))

    @property
    def abbreviation(self) -> str:
        """
        An abbreviation of the Card by combining the Rank abbreviation
        and the Face symbol.

        :return: The Card abbreviation as a string.
        """
        return f"{self.rank.abbreviation}{self.face.symbol}"


class CardShuffle(Enum):
    """
    CardShuffle Enum class for the three types of shuffle.
    """

    Deck = 1
    Shoe = 2
    DeckAndShoe = 3


class Deck:
    """
    A class to represent a standard 52-card deck that is generated as the
    product of the Face members and the Rank members.
    """

    def __init__(self, card_shuffle: CardShuffle = None):
        """
        Creates a new instance of Deck with an optional card shuffle.
        Shuffles the card array if the CardShuffle is either Deck or
        DeckAndShoe.

        :param card_shuffle:
        """
        if card_shuffle is not None and not isinstance(card_shuffle, CardShuffle):
            raise TypeError("The shuffle parameter must be of type CardShuffle")
        self.shuffle: Final[CardShuffle] = card_shuffle
        self._cards: list[Card] = [
            Card(card[1], card[0]) for card in product(list(Face), list(Rank))
        ]

        self._shuffled = False
        if self.shuffle == CardShuffle.Deck or self.shuffle == CardShuffle.DeckAndShoe:
            self._shuffle_cards()

    def _shuffle_cards(self):
        """
        Performs the shuffle at a deck level by drawing truly random cards
        from the deck and placing them in a new deck list until the original
        deck is empty. The new deck list is then assigned to the _cards
        variable.
        """
        if not self._shuffled:
            shuffled_cards = []
            while self.can_draw_card:
                i = secrets.choice(range(0, self.cards_remaining))
                shuffled_cards.append(self._cards.pop(i))
            self._cards = shuffled_cards

    def draw_card(self) -> Union[Card, None]:
        """
        If a card can be drawn from the cards array, it is drawn and
        returned, otherwise None is returned.
        :return: Either an instance of Card, or None.
        """
        if self.can_draw_card:
            return self._cards.pop(0)
        else:
            return None

    @property
    def can_draw_card(self) -> bool:
        """
        Returns true if the there are cards in the cards array, otherwise
        returns false.
        """
        return len(self._cards) > 0

    @property
    def cards_remaining(self) -> int:
        """
        Returns the number of cards in the cards array.
        """
        return len(self._cards)

    def __iter__(self):
        """
        An iterator that provides easy access to all of the cards in order.
        """
        return self

    def __next__(self):
        """
        If a can can be drawn, it is drawn and returned.

        :raise StopIteration: When cards can no longer be drawn.
        """
        if self.can_draw_card:
            return self.draw_card()
        raise StopIteration

    def __repr__(self):
        return f"Deck: {self.cards_remaining} cards remaining"
