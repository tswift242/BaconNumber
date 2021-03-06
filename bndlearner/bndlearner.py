import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from bndlexceptions import NoBaconNumber
from multiprocessing import Pool, cpu_count
import math

class BNDlearner(object):
	"""Learns the distribution the Bacon Number by
	scraping the data from Google's Bacon Number feature
	"""

	GOOGLE_URL_PREFIX = "https://www.google.com/search?q=bacon+number+"
	ANSWER_CSS_CLASS = "answer_predicate" # full class is "answer_predicate vk_h"
	NUMBER_EXTRACTOR_REGEX = ".*(\d+).*"
	DEFAULT_USER_AGENT = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; X64; rv:25.0) Gecko 20100101 Firefox/25.0"}

	def __init__(self, maxBaconNumber=12, numProcs=cpu_count()):
		"""
		:attribute maxBaconNumber: maximum bacon number accounted for in the distribution
		:attribute dist: bacon number distribution vector for values between 0 and 
		maxBaconNumber, inclusive
		:attribute numProcs: number of processes to run the learning computation on
		"""

		self.maxBaconNumber = maxBaconNumber
		self.dist = np.zeros((self.maxBaconNumber+1), dtype=np.float16)
		self.numProcs = numProcs

	def learnBaconNumberDistributionFromFile(self, actorsFile, normalize=True):
		"""Learns the distribution of the bacon number for the
		list of actors provided in the given file.

		:param actorsFile: string specifying the filename of 
		a list of actors
		"""

		# obtain list of actors
		try:
			f = open(actorsFile, "r")
		except IOError:
			raise # let the caller handle this
		else:
			actors = f.readlines()
			f.close()
		# remove trailing newlines
		actors = [actor.rstrip() for actor in actors]

		return self.learnBaconNumberDistribution(actors, normalize, 0)

	def learnBaconNumberDistribution(self, actors, normalize=True, mode=0):
		"""Learns the distribution of the bacon number in a way dependent
		on the input mode, and self.numProcs

		:param actors: list of actor names
		:param normalize: boolean indicating whether or not the resulting distribution
		vector should be normalized
		:param mode: how the distribution should be calculated
		"""
		if self.numProcs == 1: # single process case
			self.dist = self._learnBaconNumberDistributionSP(actors, normalize)
		elif mode == 0: # first multiprocessing approach
			self.dist = self._learnBaconNumberDistributionMP(actors, normalize)
		elif mode == 1: # second multiprocessing approach
			self.dist = self._learnBaconNumberDistributionMP2(actors, normalize)
		else: # default case
			self.dist = self._learnBaconNumberDistributionMP(actors, normalize)
		return self.dist

	def _learnBaconNumberDistributionMP(self, actors, normalize=True):
		"""Learns the distribution of the bacon number for the
		provided list of actors using multiprocessing.
		Uses parallel divide-and-conquer approach of doing P parallel
		calls across P process, each on an actor sub-list of size N/P.

		:param actors: list of actor names
		:param normalize: boolean indicating whether or not the resulting distribution
		vector should be normalized
		"""

		pool = Pool(processes=self.numProcs)
		# number of actors for each process to handle
		numActors = len(actors)
		chunksize = int(math.ceil(numActors / float(self.numProcs)))
		# partition actors into per-process sub-lists
		chunks = [actors[i: i+chunksize]
					for i in range(0, len(actors), chunksize)]
		# cumulative distribution across all processes
		cumdist = np.zeros((self.maxBaconNumber+1), dtype=np.float16)
		# TODO: see if we can get any performance gains by using imap_unordered instead
		for dist in pool.imap_unordered(self._learnBaconNumberDistributionCountsSP, chunks):
			cumdist += dist
		pool.close()
		if normalize:
			cumdist /= numActors
		return cumdist

	def _learnBaconNumberDistributionSP(self, actors, normalize=True):
		"""Learns the distribution of the bacon number for the
		provided list of actors.
		This approach does not store computed bacon numbers in an intermediate array, 
		but rather manually computes the histogram of the distribution online.
		As a result, this approach is more costly (time-wise) and 
		more complicated when multiprocessing, and so we leave it as a single process
		implementation.

		:param actors: list of actor names
		:param normalize: boolean indicating whether or not the resulting distribution
		vector should be normalized
		"""

		dist = np.zeros((self.maxBaconNumber+1), dtype=np.float16)
		for actor in actors:
			try:
				bn = self.getBaconNumber(actor)
			except NoBaconNumber as e:
				print "Warning: {0}".format(str(e))
			else:
				if bn <= self.maxBaconNumber:
					dist[bn] += 1
				else:
					print "Warning: bacon number {0} for actor {1} exceeds maximum bacon number of {2}, and so is being ignored".format(bn,actor,self.maxBaconNumber)

		# normalize distribution
		if normalize:
			numActors = len(actors)
			dist /= numActors
		return dist

	def _learnBaconNumberDistributionCountsSP(self, actors):
		"""Shortcut for learnBaconNumerDistribution2 with normalize set to False.
		Simplies using the function with multiprocessing.
		"""

		return self._learnBaconNumberDistributionSP(actors, False)

	def _learnBaconNumberDistributionMP2(self, actors, normalize=True):
		"""Learns the distribution of the bacon number for the
		provided list of actors.
		This approach stores computed bacon numbers in an intermediate array 
		to avoid otherwise necessary synchronization costs on the shared resource dist.
		A histogram is then created across the intermediate array and then normalized, 
		leading to the final distribution.
		As a result, this approach is faster under multiprocessing than an approach that
		doesn't store intermediate results (such as the single process implementation), 
		but does require an extra amount of memory on a linear order.

		:param actors: list of actor names
		:param normalize: boolean indicating whether or not the resulting distribution
		vector should be normalized
		"""

		numActors = len(actors)
		baconNumbers = np.zeros((numActors), dtype=np.uint8)

		pool = Pool(processes=self.numProcs)
		chunksize = int(math.ceil(numActors / (2 * float(self.numProcs))))
		# TODO: this does not handle NoBaconNumber exceptions gracefully
		for index, bn in enumerate(pool.imap_unordered(self.getBaconNumber, actors, chunksize)):
			if bn <= self.maxBaconNumber:
				baconNumbers[index] = bn
			else:
				print "Warning: bacon number {0} for actor {1} exceeds maximum bacon number of {2}, and so is being ignored".format(bn,actor,self.maxBaconNumber)
		pool.close()

		# single process version commented out below
		#for index, actor in enumerate(actors):
			#try:
				#bn = self.getBaconNumber(actor)
			#except NoBaconNumber as e:
				#print "Warning: {0}".format(str(e))
			#else:
				#if bn <= self.maxBaconNumber:
					#baconNumbers[index] = bn
				#else:
					#print "Warning: bacon number {0} for actor {1} exceeds maximum bacon number of {2}, and so is being ignored".format(bn,actor,self.maxBaconNumber)

		# compute normalized histogram from the gathered bacon numbers
		# histogram's bins have upperbound maxBaconNumber+2 so that bacon numbers 
		# maxBaconNumber-1 and maxBaconNumber are quantized into different bins
		dist, bins = np.histogram(baconNumbers, bins=np.arange(self.maxBaconNumber+2), density=normalize)
		return dist

	def getBaconNumber(self, actor):
		"""Returns the Bacon Number of the given actor.

		:param actor: string specifying the full name of an actor, 
		e.g. "Johnny Depp"
		"""

		actorURL = BNDlearner.GOOGLE_URL_PREFIX + actor.replace(" ", "+")
		# change user-agent to allow us to scrape data from Google
		actorHtml = requests.get(actorURL, headers = BNDlearner.DEFAULT_USER_AGENT).text

		# parse bacon number information from html
		soup = BeautifulSoup(actorHtml)
		answerTag = soup.find(class_=BNDlearner.ANSWER_CSS_CLASS)
		if answerTag is None:
			raise NoBaconNumber("no bacon number found", actor)

		# parse number out of answerTag's string and return it
		return self._extractNumber(answerTag.string)

	# private static
	def _extractNumber(self, string):
		"""Extracts the first number from a string, 
		casts it to an integer, and then returns it.

		:param string: string to be matched against regex NUMBER_EXTRACTOR_REGEX
		"""

		match = re.match(BNDlearner.NUMBER_EXTRACTOR_REGEX, string, re.S)
		return int(match.group(1))
