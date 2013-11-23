import requests
from bs4 import BeautifulSoup
import re
from numpy import zeros
from numpy import histogram, arange, uint8, float16
from bndlexceptions import NoBaconNumber

class BNDlearner:
	"""Learns the distribution the Bacon Number by
	scraping the data from Google's Bacon Number feature
	"""

	GOOGLE_URL_PREFIX = "https://www.google.com/search?q=bacon+number+"
	ANSWER_CSS_CLASS = "answer_predicate" #full class is "answer_predicate vk_h"
	NUMBER_EXTRACTOR_REGEX = ".*(\d+).*"
	#TODO: possibly make this argument to self
	DEFAULT_USER_AGENT = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; X64; rv:25.0) Gecko 20100101 Firefox/25.0"}

	def __init__(self, maxBaconNumber):
		"""
		:attribute maxBaconNumber: maximum bacon number accounted for in the distribution
		:attribute dist: bacon number distribution vector for values between 0 and 
		maxBaconNumber, inclusive
		"""
		self.maxBaconNumber = maxBaconNumber
		self.dist = zeros((self.maxBaconNumber+1), dtype=float16) #smallest available float type

	def getBaconNumber(self, actor):
		"""Returns the Bacon Number of the given actor.

		:param actor: string specifying the full name of an actor, 
		e.g. "Johnny Depp"
		"""

		actorURL = BNDlearner.GOOGLE_URL_PREFIX + actor.replace(" ", "+")
		#change user-agent to allow us to scrape data from Google
		actorHtml = requests.get(actorURL, headers = BNDlearner.DEFAULT_USER_AGENT).text

		#parse bacon number information from html
		soup = BeautifulSoup(actorHtml)
		answerTag = soup.find(class_=BNDlearner.ANSWER_CSS_CLASS)
		if answerTag is None:
			raise NoBaconNumber("no bacon number found", actor)

		#parse number out of answerTag's string and return it
		return self.extractNumber(answerTag.string)

	def learnBaconNumberDistributionFromFile(self, actorsFile):
		"""Learns the distribution of the bacon number for the
		list of actors provided in the given file.

		:param actorsFile: string specifying the filename of 
		a list of actors
		"""

		#obtain list of actors
		try:
			f = open(actorsFile, "r")
		except IOError:
			raise #let the caller handle this
		else:
			actors = f.readlines()
			f.close()

		self.learnBaconNumberDistribution(actors)

	def learnBaconNumberDistribution(self, actors):
		"""Learns the distribution of the bacon number for the
		provided list of actors.
		This approach stores computed bacon numbers in an intermediate array 
		to avoid otherwise necessary synchronization costs on the shared resource self.dist.
		A histogram is then created across the intermediate array and then normalized, 
		leading to the final distribution.
		As a result, this approach is faster under multiprocessing, but does require an extra amount of memory on a linear order.

		:param actors: list of actor names
		"""

		numActors = len(actors)
		baconNumbers = zeros((numActors), dtype=uint8) # smallest available int type
		# TODO: multithread this!!!
		for index, actor in enumerate(actors):
			try:
				bn = self.getBaconNumber(actor)
			except NoBaconNumber as e:
				print "Warning: {0}".format(str(e))
			else:
				if bn <= self.maxBaconNumber:
					baconNumbers[index] = bn
				else:
					print "Warning: bacon number {0} for actor {1} exceeds maximum bacon number of {2}, and so is being ignored".format(bn,actor,self.maxBaconNumber)

		# compute normalized histogram from the gathered bacon numbers
		# histogram's bins have upperbound maxBaconNumber+2 so that bacon numbers 
		# maxBaconNumber-1 and maxBaconNumber are quantized into different bins
		self.dist, bins = histogram(baconNumbers, bins=arange(self.maxBaconNumber+2), density=True)

	def learnBaconNumberDistribution2(self, actors):
		"""Learns the distribution of the bacon number for the
		provided list of actors.
		This approach does not store computed bacon numbers in an intermediate array, 
		but rather manually computes the histogram of the distribution online.
		As a result, this approach is more costly (time-wise) and 
		more complicated when multiprocessing

		:param actors: list of actor names
		"""

		for actor in actors:
			try:
				bn = self.getBaconNumber(actor)
			except NoBaconNumber as e:
				print "Warning: {0}".format(str(e))
			else:
				if bn <= self.maxBaconNumber:
					self.dist[bn] += 1
				else:
					print "Warning: bacon number {0} for actor {1} exceeds maximum bacon number of {2}, and so is being ignored".format(bn,actor,self.maxBaconNumber)

		# normalize distribution
		numActors = len(actors)
		self.dist /= numActors

	#private static
	def extractNumber(self, string):
		"""Extracts the first number from a string, 
		casts it to an integer, and then returns it.

		:param string: string to be matched against regex NUMBER_EXTRACTOR_REGEX
		"""

		match = re.match(BNDlearner.NUMBER_EXTRACTOR_REGEX, string, re.S)
		return int(match.group(1))
