from pycasinosim.casino.equipment.card import Card, Shoe, CardShuffle
from pycasinosim.casino.equipment.card import Deck
from pycasinosim.casino.equipment.card import Face
from pycasinosim.casino.equipment.card import Rank


# Card
from pycasinosim.exceptions import BadCardError


def test_face_symbol():
    c = Card(Rank.ACE, Face.HEART)
    assert c.face.symbol == "♥"


def test_rank_abbreviation():
    c = Card(Rank.ACE, Face.HEART)
    assert c.rank.abbreviation == "A"


def test_rank_colour():
    c1 = Card(Rank.ACE, Face.HEART)
    assert c1.face.colour == "red"

    c2 = Card(Rank.ACE, Face.SPADE)
    assert c2.face.colour == "black"


def test_card_eq_by_uuid():
    c1 = Card(Rank.ACE, Face.HEART)
    c2 = Card(Rank.ACE, Face.HEART)
    assert c1 != c2


# Deck
def test_deck_generation():
    d = Deck()
    assert d.cards_remaining == 52


def test_empty_deck():
    d = Deck()
    while d.can_draw_card:
        d.draw_card()
    assert d.cards_remaining == 0


# Shoe
def test_deck_generation():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    assert s.cards_remaining == 312


def test_card_replacement():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    c = s.draw_card()
    can_replace = True
    try:
        s.replace_overdrawn_card(c)
    except BadCardError as e:
        can_replace = False
    assert can_replace


def test_card_repeat_replacement():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    c = s.draw_card()
    try:
        s.replace_overdrawn_card(c)
    except BadCardError as e:
        pass
    repeat_replacement = False
    try:
        s.replace_overdrawn_card(c)
        repeat_replacement = True
    except BadCardError as e:
        pass
    assert not repeat_replacement


def test_replaced_card_then_drawn():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    c = s.draw_card()
    target_uuid = c.uuid
    try:
        s.replace_overdrawn_card(c)
    except BadCardError as e:
        pass

    assert s.draw_card().uuid == target_uuid


def test_bad_card_replacement():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    c = s.draw_card()
    c1 = Card(Rank.ACE, Face.HEART)
    can_replace = True
    try:
        s.replace_overdrawn_card(c1)
    except BadCardError as e:
        can_replace = False
    assert can_replace is False


def test_empty_shoe():
    s = Shoe(6, CardShuffle.DECK_AND_SHOE)
    for i in range(312):
        s.draw_card()
    assert s.cards_remaining == 0
