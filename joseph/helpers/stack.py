import collections


class Stack(collections.deque):
	"""
	A very simpy stack object based on the standard 
	``collections.deque`` object, but with some 
	convenience methods added to it. 
	
	While these methods give easy access to indexing of
	the object, it's suggested to a regular list if 
	this is something that will happen often as lists 
	are quicker at these operations.
	
	ex:
		stack = Stack('foo', 'bar')
		
		x = stack.get_('foo')
		print(x)
		>>> 'foo'
		print(stack)
		>>> stack(['foo', 'bar'])
		
		x = stack.pop_('foo')
		print(x)
		>>> 'foo'
		print(stack)
		>>> stack(['bar'])
		
		stack.del_('foo')
		stack.del_('bar')
		print(stack)
		>>> stack([])
	"""
	
	def __init__(self, *args):
		"""
		Makes super call to ``collections.deque`` and 
		updates itself with provided :param: `args`. 
		
		:param args: Values to add to `self` on init
		"""
		super(collections.deque, self).__init__()
		
		if args:
			self.extend(args)
	
	def del_(self, item):
		"""
		Deletes an item from `self` by its value, this
		is done by finding the item's index.
		
		:param item: Item to delete
		"""
		del self[self.index(item)]
		
	def pop_(self, item):
		""" 
		Like :meth: `del_` but returns the deleted item
		
		:param item: Item to delete and return
		"""
		item = self[self.index(item)]
		self.del_(item)
		
		return item
		
	def __repr__(self):
		return 'stack({0})'.format(list(self))