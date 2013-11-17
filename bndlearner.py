from bs4 import BeautifulSoup
import requests
import re
from numpy import *

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
		#*** make distribution vector an instance variable?
		self.dist = zeros((maxBaconNumber+1,1))

	def getBaconNumber(self, actor):
		"""Returns the Bacon Number of the given actor

		:param actor: string specifying the full name of an actor, 
		e.g. "Johnny Depp"
		"""

		actorURL = BNDlearner.GOOGLE_URL_PREFIX + actor.replace(" ", "+")
		#change user-agent to allow us to scrape data from Google
		actorHtml = requests.get(actorURL, headers = BNDlearner.DEFAULT_USER_AGENT).text

		#parse bacon number information from html
		soup = BeautifulSoup(actorHtml)
		answerTag = soup.find(class_=BNDlearner.ANSWER_CSS_CLASS)

		#parse number out of answerTag's string and return it
		return self.extractNumber(answerTag.string)

	def learnBaconNumberDistribution(self, actorsFile):
		"""Learns the distribution of the bacon number for the
		provided list of actors.

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

		"""TODO: multithread this!!!"""
		"""TODO: consider using numpy.histogram (especially after multithreading)"""
		#compute bacon number for each actor, and increment counter in distribution
		for actor in actors:
			bn = self.getBaconNumber(actor)
			self.dist[bn] += 1

		#normalize distribution
		numActors = len(actors)
		self.dist /= numActors

	#private static
	#extracts the first number from a string, casts it to an integer, and then returns it
	def extractNumber(self, string):
		match = re.match(BNDlearner.NUMBER_EXTRACTOR_REGEX, string, re.S)
		return int(match.group(1))
