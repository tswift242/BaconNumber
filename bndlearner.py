from bs4 import BeautifulSoup
import urllib2
#from numpy import *

class BNDlearner:
	"""Learns the distribution the Bacon Number by
	scraping the data from Google's Bacon Number feature
	"""

	GOOGLE_URL_PREFIX = "https://www.google.com/search?q=bacon+number+"
	ANSWER_CSS_CLASS = "answer_predicate" #full class is "answer_predicate vk_h"

	def __init__(self):
		#pass in other arguments?
		#*** make distribution vector an instance variable?
		#use os.path for actor resource file, and use imdb tools to read this file??
		self.dist = 0 #TODO: change/remove this

	def getBaconNumber(self, actor):
		"""Returns the Bacon Number of the given actor

		:param actor: string specifying the full name of an actor, 
		e.g. "Johnny Depp"
		"""

		#TODO: look at replacing urllib2 stuff with requests
		#change user-agent to allow us to scrape data from Google
		opener = urllib2.build_opener()
		opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 6.1; Win64; X64; rv:25.0) Gecko 20100101 Firefox/25.0")]
		urllib2.install_opener(opener)

		actorURL = BNDlearner.GOOGLE_URL_PREFIX + actor.replace(" ", "+")
		actorHtml = urllib2.urlopen(actorURL).read()

		soup = BeautifulSoup(actorHtml)
		answerTag = soup.find("div", class_=BNDlearner.ANSWER_CSS_CLASS)

		#TODO: parse number out of answerTag

		return answerTag.string

	def learnBaconNumberDistribution():
		"""TODO: give parameters"""
		"""TODO: multithread this!!!"""
