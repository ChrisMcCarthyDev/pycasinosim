from pycasinosim.casino.equipment.card import Card
from pycasinosim.casino.equipment.card import Deck
from pycasinosim.casino.equipment.card import Face
from pycasinosim.casino.equipment.card import Rank


# Card
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
