**SP-Pickupables** implements pickupable props into the source engine.
The client on the server can then use the item and store it within an inventory;
which inturn can then be accessed via a simple menu. The player's inventory has public
attributes such as maximum weight, current weight, and available space. The inventory
always checks whether an item can be picked up or not.

**Player Inventories**

All player inventories are held inside a <PlayerDictionary> which is stored in <pickupables.players>
```python
from pickupables.players import player_inventories

player_inventories[<index>].inventory.add(<Item>)
```

**Custom Items**

Items are created by subclassing <pickupables.items.Item> or <pickupables.items.Weapon>. The
Weapon class contains some extra in game functions that allow for picking up weapons, because
the engine will not allow physics props with weapon models, and neither can you manipulate a 
weapons data. Instead the extra functions create a prop_dynamic at a location and handle its
usage separately.
```python
from pickupables.items import Item, Weapon

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
```
