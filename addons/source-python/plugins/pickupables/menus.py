''' Menus (../pickupables/menus.py) '''

## IMPORTS

from .players import player_inventories

from menus import PagedMenu
from menus import PagedOption

## ALL DECLARATION

__all__ = ('inventory_menu', )

##

def _inventory_menu_build(menu, index):
	'Inventory menu build callback...'
	player = player_inventories[index]

	inventory = player.inventory

	menu.title = 'Inventory ({i.weight}/{i.max_weight})'.format(i=inventory)

	menu.clear()
	for item, amount in inventory.count_by_names().items():
		menu.append(PagedOption('{} - {}'.format(item, amount), item))

def _inventory_menu_select(menu, index, choice):
	'Inventory menu select callback...'
	player = player_inventories[index]

	item = next(player.inventory.find_by_name(choice.value))
	item.on_use(player)
	menu.send()

inventory_menu = PagedMenu(build_callback=_inventory_menu_build,
	select_callback=_inventory_menu_select)