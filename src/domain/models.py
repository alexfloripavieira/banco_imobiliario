"""Domain models: Player and Property."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Property:
    position: int
    price: int
    rent: int
    owner: Optional['Player'] = None


@dataclass
class Player:
    name: str
    strategy: str
    balance: int = 300
    position: int = 0
    properties: List[Property] = field(default_factory=list)
    active: bool = True

    def move(self, steps: int, board_size: int) -> bool:
        """Move player and return True if completed a lap"""
        prev = self.position
        self.position = (self.position + steps) % board_size
        return (prev + steps) >= board_size

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

    def release_properties(self) -> None:
        for p in list(self.properties):
            p.owner = None
        self.properties.clear()
