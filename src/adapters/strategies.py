"""Player purchasing strategies (adapter layer)."""

import random
from typing import Callable, Dict

from ..domain.models import Player, Property


from ..domain.constants import CAUTIOUS_THRESHOLD, DEMANDING_RENT_THRESHOLD

def impulsiveStrategy(player: Player, prop: Property) -> bool:
    """Impulsive: always buys the property."""
    return True


def demandingStrategy(player: Player, prop: Property) -> bool:
    """Demanding: buys only if rent > threshold."""
    return prop.rent > DEMANDING_RENT_THRESHOLD


def cautiousStrategy(player: Player, prop: Property) -> bool:
    """Cautious: buys only if will keep at least threshold after purchase."""
    return (player.balance - prop.price) >= CAUTIOUS_THRESHOLD


def randomStrategy(player: Player, prop: Property) -> bool:
    """Random: buys with probability 50%."""
    return random.random() < 0.5


STRATEGIES: Dict[str, Callable[[Player, Property], bool]] = {
    "impulsivo": impulsiveStrategy,
    "exigente": demandingStrategy,
    "cauteloso": cautiousStrategy,
    "aleatorio": randomStrategy,
}
