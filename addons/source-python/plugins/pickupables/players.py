''' Player Dictionary (../pickupables/players.py) '''

## IMPORTS

from .config import PLAYER_CLASS
from .inventories import Inventory

from events import Event
from players.dictionary import PlayerDictionary

## ALL DECLARATION

__all__ = ('player_inventories', )

## PLAYER DICT CONSTRUCTION

player_inventories = PlayerDictionary(PLAYER_CLASS)

## PLAYER INVENTORY MANAGEMENT

_activated = []

@Event('player_spawn')
def _on_player_connect_create_inv(event_data):
	'Initialisation of Inventory for each joining player.'
	userid = event_data['userid']

	global _activated
	if not userid in _activated:
		player = player_inventories.from_userid(userid)
		player.inventory = Inventory(player)
		_activated.append(userid)

@Event('player_disconnect')
def _on_player_disconnect_reset_inventory(event_data):
	userid = event_data['userid']

	global _activated
	_activated.remove(userid)