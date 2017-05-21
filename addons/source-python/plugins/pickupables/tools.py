''' Pythonic Tools (../pickupables/tools.py) '''

## IMPORTS


## ALL DECLARATION

__all__ = ('get_subclasses', 'get_subclass_dict', )

## TOOL FUNCTIONS

def get_subclasses(cls):
	'Retrieve all subclasses for a given python class.'
	for sub_cls in cls.__subclasses__():
		yield sub_cls
		yield from get_subclasses(sub_cls)

def get_subclass_dict(cls):
	'Retrieve a dictionary for all subclasses for a given python class.'
	return {sub.__name__: sub for sub in get_subclasses(cls)}