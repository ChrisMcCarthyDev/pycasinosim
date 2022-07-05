"""
The card module holds the CardFace and CardRank enum classes, along with the
Card and Deck data classes.
"""
from dataclasses import dataclass, field
from enum import IntEnum
from itertools import product
from uuid import uuid4


class CardRank(IntEnum):
    """
    CardRank Enum class holds the card ranks from Ace through to King.
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
    def as_abbreviation(self) -> str:
        """
        An abbreviation of the CardRank. Cards 2 through to 10 are
        returned as their value as a string, whereas ACE, JACK, QUEEN,
        and KING are returned as the first character of their name.

        :return: An abbreviated CardRank name.
        """
        if (self.value >= 2) and (self.value <= 10):
            return str(self.value)
        return self.name[0]


class CardFace(IntEnum):
    """
    CardFace Enum class to hold the four card faces.
    """
    CLUB = 1
    DIAMOND = 2
    HEART = 3
    SPADE = 4

    @property
    def colour(self) -> str:
        """
        The CardFace colour.

        :return: red if the CardFace is DIAMOND or HEART, otherwise black.
        """
        if self is CardFace.DIAMOND or self is CardFace.HEART:
            return "red"
        return "black"

    @property
    def as_symbol(self) -> str:
        """
        The CardFace symbol.

        :return: Returns the card face symbol as a string.
        """
        if self is CardFace.CLUB:
            return "♣"
        elif self is CardFace.DIAMOND:
            return "♦"
        elif self is CardFace.HEART:
            return "♥"
        elif self is CardFace.SPADE:
            return "♠"


@dataclass(frozen=True)
class Card:
    """
    The Card class is a frozen dataclass that takes a CardRank and a
    CardFace. Each instance of Card is assigned an uuid as a string.
    """
    rank: CardRank
    face: CardFace
    uuid: str = field(default_factory=lambda: str(uuid4()))

    @property
    def as_abbreviation(self) -> str:
        """
        An abbreviation of the Card by combining the CardRank abbreviation
        and the CardFace symbol.

        :return: The Card abbreviation as a string.
        """
        return f"{self.rank.as_abbreviation}{self.face.as_symbol}"


@dataclass(frozen=True)
class Deck:
    """
    The Deck class is a frozen dataclass that has a list of cards that is
    generated as the product of the CardFace members and the CardRank members.
    """
    cards: set[Card] = field(
        default_factory=lambda: list(
            [Card(card[1], card[0]) for card
                in product(list(CardFace), list(CardRank))]
        )
    )
