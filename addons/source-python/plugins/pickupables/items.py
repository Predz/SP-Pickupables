''' Item Classes (../pickupables/items.py) '''

## IMPORTS

from .config import ITEM_ENTITY_TYPES
from .tools import get_subclass_dict

from engines.precache import Model
from entities.entity import Entity
from entities.helpers import index_from_pointer
from weapons.entity import Weapon as SPWeapon

## STORAGE OF ALL ITEMS

class Items(list):
	'This class is used to store all <Items> and retrieve them by an attribute.'
	def find_by_index(self, index):
		for item in self:
			if not item.entity:
				continue
			elif item.entity.index == index:
				return item
		return None
items = Items()

## GENERIC ITEM CLASSES

class Item(object):
	'''
	Item is a unused class which implements
	all specific attributes a static item
	needs. Item has to be subclassed
	and given event methods to be used
	successfully.
	'''

	name = 'Unnamed'
	description = 'Unnamed Item'
	weight = 0.0
	model_path = ''
	model = None

	def __init__(self, entity):
		'Wrap the item around the entity, and store for later use.'
		self.entity = entity

	def __new__(cls, *args, **kwargs):
		'Store all the new instances inside the <Items> list.'
		instance = object.__new__(cls)
		items.append(instance)
		return instance

	def on_remove(self):
		'To be called when the item wants to be removed/destroyed.'
		raise NotImplementedError('Must be overriden in a subclass of <Item>.')

	def on_pickup(self, player):
		'To be called upon the item being picked up by the player.'
		raise NotImplementedError('Must be overriden in a subclass of <Item>.')

	def on_use(self, player):
		'To be called upon the item being used by a player.'
		raise NotImplementedError('Must be overriden in a subclass of <Item>.')

	def on_dropped(self, player):
		'To be called upon the item being dropped. Only applicable to weapons.'
		raise NotImplementedError('Must be overriden in a subclass of <Item>.')

	@property
	def entity(self):
		'Return the entity which this item wraps around.'
		return self._entity

	@entity.setter
	def entity(self, entity):
		'Only allow the setting of the item if it is of these types.'
		if type(entity) not in ITEM_ENTITY_TYPES:
			raise TypeError('Cannot bind <Item> to type <{}>. Must be type <{}>'.format(
				type(entity), ITEM_ENTITY_TYPES))
		self._entity = entity

	@classmethod
	def get_subclasses(cls):
		'Returns all subclasses of <Item>. For use in other plugins that want to iterate'\
		' over all possible items.'
		return get_subclass_dict(cls)

class Weapon(Item):
	classname = ''
	model = object()
	name = 'A Weapon'
	slot = 'primary'
	weight = 0.0

	@classmethod
	def create(cls, location):
		'Creation of the item in game. Proceed with this...'
		entity = Entity.create('prop_dynamic')
		entity.model = cls.model
		entity.origin = location
		entity.spawn()
		entity.delay(0.1, entity.enable_collision, cancel_on_level_end=True)
		return cls(entity)

	def __init__(self, *args, **kwargs):
		'Setting the ammo and clip count of the weapon on pickup.'
		super().__init__(*args, **kwargs)
		self.ammo = 0
		self.clip = 15

	def on_remove(self):
		'Called upon the wanted removal of the entity.'
		self.entity.remove()

	def on_use(self, player):
		'Called upon the item being used. <use> input.'
		weapon = getattr(player, '{}_weapon'.format(self.slot))
		if weapon:
			weapon._save_ammo()
			player.delay(0.1, weapon._drop, (player, ), cancel_on_level_end=True)
			player.inventory.add(weapon)
		player.inventory.discard(self)
		player.delay(0.2, self._setup_weapon, (player, ), cancel_on_level_end=True)

	def on_pickup(self, player):
		'Upon the item being picked up. Called after all checks.'
		if getattr(player, '{}_weapon'.format(self.slot)):
			player.inventory.add(self)
		else:
			self._setup_weapon(player)

	def on_dropped(self, player):
		'Called when the weapon is dropped by a player.'
		setattr(player, '{}_weapon'.format(self.slot), None)
		self.entity.delay(0.1, self.entity.remove, cancel_on_level_end=True)

	def _setup_weapon(self, player):
		'When the weapon is given, this sets up the ammo and clip.'
		self.entity = SPWeapon(index_from_pointer(player.give_named_item(self.classname)))
		self._setup_ammo()
		setattr(player, '{}_weapon'.format(self.slot), self)

	def _drop(self, player):
		'Drop the item from the player.'
		player.drop_weapon(self.entity.pointer)
		player.delay(0.1, self.entity.remove, cancel_on_level_end=True)

	def _save_ammo(self):
		'Saves the current ammo and clip counts.'
		self.ammo = self.entity.ammo
		self.clip = self.entity.clip

	def _setup_ammo(self):
		'Sets the current ammo and clip counts.'
		self.entity.ammo = self.ammo
		self.entity.clip = self.clip

## CUSTOMISED ITEM SUBCLASSES

class AK47(Weapon):
	classname = 'weapon_ak47'
	model = Model('models/weapons/w_rif_ak47.mdl')
	name = 'AK47'
	slot = 'primary'
	weight = 12.0


class Ammo(Item):
	name = 'Ammo (10 Primary Bullets)'
	model = Model('models/props/coop_cementplant/coop_ammo_stash/coop_ammo_stash_empty.mdl')
	weight = 0.5

	@classmethod
	def create(cls, location):
		entity = Entity.create('prop_physics_override')
		entity.model = cls.model
		entity.origin = location
		entity.spawn_flags = 256
		entity.solid_flags = 152
		entity.collision_group = 11
		entity.spawn()
		return cls(entity)

	def on_use(self, player):
		if not player.primary:
			return

		player.primary.ammo += 10
		player.inventory.discard(self)

	def on_remove(self):
		self.entity.remove()

	def on_pickup(self, player):
		player.inventory.add(self)
		self.on_remove()