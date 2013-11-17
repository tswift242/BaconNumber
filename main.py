from bndlearner import BNDlearner
import os
import traceback
import sys
import time

def main():
	#actor = "johnny depp"
	maxBaconNumber = 10
	actorsFile = os.path.join("resources", "actors.txt")
	bndl = BNDlearner(maxBaconNumber)
	#bn = bndl.getBaconNumber(actor)
	#print bn
	try:
		bndl.learnBaconNumberDistribution(actorsFile)
	except IOError as e:
		traceback.print_exc()
	print bndl.dist

if __name__ == "__main__":
	#for prettyprint() in beautifulsoup
	reload(sys)
	sys.setdefaultencoding("utf-8")
	start = time.time()
	main()
	end = time.time()
	print "total time: ",end-start
