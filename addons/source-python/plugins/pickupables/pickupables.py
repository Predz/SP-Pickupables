''' Core (../pickupables/pickupables.py) '''

## IMPORTS

from .items import *
from .menus import inventory_menu
from .players import player_inventories

from commands.say import SayCommand
from entities.entity import Entity
from entities.datamaps import InputData
from entities.helpers import index_from_pointer
from entities.hooks import EntityCondition
from entities.hooks import EntityPreHook
from events import Event
from memory import make_object
from messages import SayText2
from players import UserCmd
from players.constants import PlayerButtons

## INVENTORY HANDLERS

@Event('player_spawn')
def _on_spawn_clear_inv(event_data):
	'Empty a clients inventory upon spawning.'
	userid = event_data['userid']
	player = player_inventories.from_userid(userid)
	player.inventory.clear()
	player.primary_weapon = None
	player.secondary_weapon = None


## ITEM HANDLERS

@EntityPreHook(EntityCondition.equals_entity_classname('prop_physics_override'), 'use')
def _on_use_add_to_inv(stack_data):
	'Add items to the inventory which have a <use> input.'
	entity = make_object(Entity, stack_data[0])
	player = player_inventories[make_object(InputData, stack_data[1]).activator.index]

	item = items.find_by_index(entity.index)
	if not item:
		return

	item.on_pickup(player)

@EntityPreHook(EntityCondition.is_player, 'run_command')
def _on_use_add_weapon(stack_data):
	'Add items to the inventory which do not have the <use> input.'
	## If a <Item> cannot be accessed via the <use> input. We try to find it by
	## hooking the player\'s <run_command> and firing a trace ray upon <PlayerButtons.USE>
	## being pushed.
	usercmd = make_object(UserCmd, stack_data[1])

	if not usercmd.buttons & PlayerButtons.USE:
		return

	player = player_inventories[index_from_pointer(stack_data[0])]
	trace = player.get_trace_ray()

	if not trace.did_hit() or trace.entity_index == 0:
		return

	item = items.find_by_index(trace.entity_index)
	if not item or item.entity.classname != 'prop_dynamic':
		return

	item.on_remove()
	item.on_pickup(player)

@EntityPreHook(EntityCondition.is_player, 'drop_weapon')
def _on_drop_remove_weapon(stack_data):
	'Remove weapons that are dropped. This is to stop weapon duplicating.'
	## We could turn the weapon into a physics prop, however for some reason weapon models
	## do not function as props with physics :s
	index = index_from_pointer(stack_data[1])

	item = items.find_by_index(index)
	if item:
		item.on_dropped(player_inventories[index_from_pointer(stack_data[0])])


## TEST SAY REGISTERS

@SayCommand('inv')
def _on_inv_check(command, index, team):
	inventory_menu.send(index)

@SayCommand('test')
def _on_say(command, index, team):
	player = player_inventories[index]

	AK47.create(player.view_coordinates)

@SayCommand('test2')
def _on_say(command, index, team):
	player = player_inventories[index]

	Ammo.create(player.view_coordinates)