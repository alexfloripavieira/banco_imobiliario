"""Player purchasing strategies (adapter layer)."""

import random
from typing import Callable, Dict

from ..domain.models import Player, Property


def impulsive_strategy(player: Player, prop: Property) -> bool:
    """Impulsive: always buys the property."""
    return True


def demanding_strategy(player: Player, prop: Property) -> bool:
    """Demanding: buys only if rent > 50."""
    return prop.rent > 50


def cautious_strategy(player: Player, prop: Property) -> bool:
    """Cautious: buys only if will keep at least 80 after purchase."""
    return (player.balance - prop.price) >= 80


def random_strategy(player: Player, prop: Property) -> bool:
    """Random: buys with probability 50%."""
    return random.random() < 0.5


STRATEGIES: Dict[str, Callable[[Player, Property], bool]] = {
    "impulsivo": impulsive_strategy,
    "exigente": demanding_strategy,
    "cauteloso": cautious_strategy,
    "aleatorio": random_strategy,
}
