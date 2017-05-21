''' Configuration (../pickupables/config.py) '''

## IMPORTS

from entities.entity import Entity
from players.entity import Player
from weapons.entity import Weapon

## CONFIG

ITEM_ENTITY_TYPES = Entity, Weapon

INVENTORY_MAX_WEIGHT = 32.0

PLAYER_CLASS = Player