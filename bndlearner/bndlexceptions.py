"""Custom exceptions"""

class NoBaconNumber(Exception):

	def __init__(self, message, actor):
		Exception.__init__(self, message)
		self.actor = actor

	def __str__(self):
		return "{0}: {1}".format(self.actor, Exception.__str__(self))
