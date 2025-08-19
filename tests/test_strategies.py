from src.adapters.strategies import (
    cautious_strategy,
    demanding_strategy,
    impulsive_strategy,
    random_strategy,
)
from src.domain.models import Player, Property


def test_impulsive_always_buys():
    p = Player(name="imp", strategy="impulsivo", balance=200)
    prop = Property(position=0, price=100, rent=10)
    assert impulsive_strategy(p, prop) is True


def test_demanding_requires_rent_gt_50():
    p = Player(name="dem", strategy="exigente", balance=200)
    prop1 = Property(position=0, price=100, rent=51)
    prop2 = Property(position=1, price=100, rent=50)
    assert demanding_strategy(p, prop1) is True
    assert demanding_strategy(p, prop2) is False


def test_cautious_requires_reserve():
    p = Player(name="cau", strategy="cauteloso", balance=200)
    prop = Property(position=0, price=120, rent=10)
    assert cautious_strategy(p, prop) is True
    prop2 = Property(position=1, price=150, rent=10)
    assert cautious_strategy(p, prop2) is False


def test_random_strategy_probability():
    p = Player(name="ran", strategy="aleatorio", balance=1000)
    prop = Property(position=0, price=100, rent=10)
    trues = 0
    for _ in range(1000):
        if random_strategy(p, prop):
            trues += 1
    assert 300 < trues < 700
