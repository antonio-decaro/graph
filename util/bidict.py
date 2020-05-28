
class Bidict(dict):
	"""
	This class is a bidirectional hashtable
	:author:
	"""
	def __init__(self, *args, **kwargs):
		super(Bidict, self).__init__(*args, **kwargs)
		# create the inverse of the dictionary
		self.inverse = {}

		# insert elements into the inverse dict
		for key, value in self.items():
			self.inverse.setdefault(value, []).append(key)

	def __setitem__(self, key, value):
		# update the inverse dictionary
		if key in self:
			self.inverse[self[key]].remove(key)

		# update the standard dictionary
		super(Bidict, self).__setitem__(key, value)

		# insert value as a list, cause a dict value can be inserted more then once
		self.inverse.setdefault(value, []).append(key)

	def __delitem__(self, key):
		# remove the element inside the inverse dict
		self.inverse.setdefault(self[key], []).remove(key)
		if self[key] in self.inverse and not self.inverse[self[key]]:
			del self.inverse[self[key]]
		super(Bidict, self).__delitem__(key)


__author__ = "Joshua Bronson <jab@math.brown.edu>"
