''' Inventory Class (../pickupables/inventories.py) '''

## IMPORTS

from .config import INVENTORY_MAX_WEIGHT

from collections import Counter

## ALL DECLARATION

__all__ = ('Inventory', )

## INVENTORY CLASS

class Inventory(set):
	'''
	Inventory is bound to client on the server
	and allows us to manage a "backpack" which
	can only store a maximum weight.

	:param Player player:
		Player to bind this inventory too.
	'''

	def __init__(self, owner, *args, **kwargs):
		'Specify the owner to bind this inventory too. Also can supply extra <list> args.'
		super(Inventory, self).__init__(*args, **kwargs)

		self.owner = owner
		self.max_weight = INVENTORY_MAX_WEIGHT

	def add(self, item):
		'Overriden <set.add> to check if a inventory is too full.'
		if not self.can_pickup(item):
			return

		super(Inventory, self).add(item)

	def can_pickup(self, item):
		'Checks if a inventory can pick up an item by calculating space available.'
		if item.weight > self.space:
			return False
		return True

	@property
	def weight(self):
		'Returns the current weight of the inventory.'
		return sum(item.weight for item in self)

	@property
	def space(self):
		'Returns the amount of space left in the inventory.'
		return self.max_weight - self.weight

	## HELPERS

	def find_by_name(self, name):
		'Finds each item in the inventory by a name and iterates over them.'
		for item in self:
			if item.name == name:
				yield item

	def count_by_names(self):
		'Returns a <collections.Counter> instance of the list respective to class names.'
		return Counter([x.name for x in self])