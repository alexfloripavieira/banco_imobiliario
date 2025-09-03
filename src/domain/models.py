"""Domain models: Player and Property."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


from .constants import INITIAL_BALANCE

@dataclass
class Property:
    position: int
    price: int
    rent: int
    owner: Optional["Player"] = None


@dataclass
class Player:
    name: str
    strategy: str
    balance: int = INITIAL_BALANCE
    position: int = 0
    properties: List[Property] = field(default_factory=list)
    active: bool = True

    def move(self, steps: int, boardSize: int) -> bool:
        """Move player and return True if completed a lap"""
        prev = self.position
        self.position = (self.position + steps) % boardSize
        return (prev + steps) >= boardSize

    def pay(self, amount: int) -> None:
        self.balance -= amount
        if self.balance < 0:
            self.active = False

    def receive(self, amount: int) -> None:
        self.balance += amount

    def buy(self, prop: Property) -> None:
        self.balance -= prop.price
        self.properties.append(prop)
        prop.owner = self

    def releaseProperties(self) -> None:
        for p in list(self.properties):
            p.owner = None
        self.properties.clear()
