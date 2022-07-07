"""
The card module holds the Face and Rank enum classes, along with the
Card and Deck data classes.
"""
import secrets
from dataclasses import dataclass, field
from enum import IntEnum, Enum
from itertools import product
from typing import Final, Union, List
from uuid import uuid4

from pycasinosim.exceptions import BadCardError


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

    DECK = 1
    SHOE = 2
    DECK_AND_SHOE = 3


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
        self._cards: List[Card] = [
            Card(card[1], card[0]) for card in product(list(Face), list(Rank))
        ]
        self._shuffled = False
        self._shuffle_cards()

    def _shuffle_cards(self):
        """
        Performs the shuffle at a deck level by drawing truly random cards
        from the deck and placing them in a new deck list until the original
        deck is empty. The new deck list is then assigned to the _cards
        variable.
        """
        if not self._shuffled and (
            self.shuffle == CardShuffle.DECK
            or self.shuffle == CardShuffle.DECK_AND_SHOE
        ):
            shuffled_cards = []
            while self.can_draw_card:
                i = secrets.choice(range(0, self.cards_remaining))
                shuffled_cards.append(self._cards.pop(i))
            self._cards = shuffled_cards
            self._shuffled = True

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


class Shoe:
    """
    A class that represents the Shoe on a card table. The shoe performs all
    drawing of cards and overdrawn card replacement. The shoe prevents 'bad
    cards' from being placed into the shoe.
    """

    def __init__(self, decks: int, card_shuffle: CardShuffle = None):
        """
        Creates a new instance of Shoe with a number of decks and an
        optional card shuffle. Decks must be an integer and be greater than
        0. Shuffles the card array if the CardShuffle is either Shoe or
        DeckAndShoe.

        :param decks: The number of decks in the shoe.
        :param card_shuffle: The type of shuffle the Shoe will perform. Has
        a default value of None.

        :raise TypeError: When CardShuffle is not None and not of type
        CardShuffle.
        :raise TypeError: When decks is not of type int.
        :raise ValueError: When decks is less than 1.
        """
        if card_shuffle is not None and not isinstance(card_shuffle, CardShuffle):
            raise TypeError("Card_shuffle must be of type CardShuffle")
        if not isinstance(decks, int):
            raise TypeError("Decks must be of type int")
        if decks < 1:
            raise ValueError("Decks must be greater than 1")
        self.shuffle: Final[CardShuffle] = card_shuffle
        self.decks: Final[int] = decks
        self._cards: List[Card] = []
        self._overdrawn_cards: List[Card] = []
        self._card_uuids: List[str] = []
        self._shoe_populated: bool = False
        self._populate_shoe()
        self._shuffled: bool = False
        self._shuffle_cards()

    def _shuffle_cards(self):
        """
        Performs the shuffle if the Deck has not already been shuffled, and if
        the shuffle is equal to either SHOE or DECK_AND_SHOE.
        """
        if not self._shuffled and (
            self.shuffle == CardShuffle.SHOE
            or self.shuffle == CardShuffle.DECK_AND_SHOE
        ):
            shuffled_cards = []
            while self.can_draw_card:
                i = secrets.choice(range(0, self.cards_remaining))
                shuffled_cards.append(self._cards.pop(i))
            self._cards = shuffled_cards
            self._shuffled = True

    @property
    def deck_count(self) -> int:
        """
        Returns the number of Decks the Shoe was constructed with.

        :return: An int.
        """
        return self.decks

    def _populate_shoe(self) -> None:
        """
        Iterates over a range of the number of Decks, creating a new
        instance of Deck each time. The Cards from each Deck are drawn and
        appended to the cards list, maintaining their (shuffled or
        un-shuffled) deck order. The uuid of each card is appended to the
        card uuids list.
        """
        if not self._shoe_populated:
            for i in range(0, self.decks):
                d = Deck(self.shuffle)
                for c in d:
                    self._card_uuids.append(c.uuid)
                    self._cards.append(c)
            self._shoe_populated = True

    def replace_overdrawn_card(self, card: Card) -> None:
        """
        Appends the card to the list of overdrawn cards.

        :param card: An instance of Card.

        :raise TypeError: When the card is not of type Card.
        :raises BadCardError: When the UUID of the card is None or is not
        listed in the uuids list.
        :raises BadCardError: When the card has already been placed back
        into the shoe.
        """
        if not isinstance(card, Card):
            raise TypeError("The card parameter must be of type Card")
        if card.uuid is None or card.uuid not in self._card_uuids:
            raise BadCardError(
                "This card has an invalid uuid and cannot be "
                "placed back into the shoe"
            )
        if self._is_card_in_shoe(card):
            raise BadCardError(
                "This card cannot be placed back into the shoe as it is "
                "already in the shoe"
            )
        self._overdrawn_cards.append(card)

    def _is_card_in_shoe(self, card: Card) -> bool:
        """
        Return True if the uuid of the given card is in the cards or
        overdrawn_cards list, otherwise returns False.

        :param card: An instance of Card.
        :return: A bool.

        :raise TypeError: When the card is not of type Card.
        """
        if not isinstance(card, Card):
            raise TypeError("The card parameter must be of type Card")
        return any(c.uuid == card.uuid for c in self._cards) or any(
            c.uuid == card.uuid for c in self._overdrawn_cards
        )

    @property
    def _use_overdrawn_card(self) -> bool:
        """
        Returns True if the length of the list of overdrawn cards is greater
        than 0, otherwise returns False.

        :return: A bool.
        """
        return len(self._overdrawn_cards) > 0

    def _draw_overdrawn_card(self) -> Union[Card, None]:
        """
        If there are overdrawn cards, a Card is popped from 0 and returned.

        :return: A card, or None.
        """
        if self._use_overdrawn_card:
            return self._overdrawn_cards.pop(0)
        else:
            return None

    def draw_card(self) -> Union[Card, None]:
        """
        First checks if there are overdrawn cards, if so, calls the draw
        overdrawn card function, otherwise if a card can be drawn from the
        cards list, it is drawn and returned.

        :return: A Card, or None.
        """
        if self._use_overdrawn_card:
            return self._draw_overdrawn_card()
        else:
            if self.can_draw_card:
                return self._cards.pop(0)
            else:
                return None

    @property
    def can_draw_card(self) -> bool:
        """
        Returns true if there are cards in the cards or overdrawn cards lists,
        otherwise returns false.

        :return: A bool.
        """
        return len(self._cards) > 0 or len(self._overdrawn_cards) > 0

    @property
    def cards_remaining(self) -> int:
        """
        Returns the combined number of cards in both the cards and overdrawn
        cards lists.

        :return: An int.
        """
        return len(self._cards) + len(self._overdrawn_cards)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Shoe in the format: Shoe: #
        decks, # cards remaining.

        :return: A string.
        """
        return f"Shoe: {self.decks} decks, {self.cards_remaining} " f"cards remaining"
