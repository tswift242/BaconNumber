from bndlearner import BNDlearner
import os
import traceback
import sys
import time
from pickle_method import register_pickle_method

def main():
	maxBaconNumber = 10
	numProcs = 4
	actorsFile = os.path.join("resources", "actors.txt")

	bndl = BNDlearner(maxBaconNumber, numProcs)
	try:
		bndl.learnBaconNumberDistributionFromFile(actorsFile)
	except IOError as e:
		traceback.print_exc()
	print "\n\n",bndl.dist
	
if __name__ == "__main__":
	register_pickle_method()
	start = time.time()
	main()
	end = time.time()
	print "total time: ",end-start
