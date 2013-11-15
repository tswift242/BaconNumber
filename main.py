from bndlearner import BNDlearner
import sys
import time

def main():
	print "Let's learn the Bacon Number's distribution!"
	actor = "johnny depp"
	bndl = BNDlearner()
	bn = bndl.getBaconNumber(actor)
	print bn

if __name__ == "__main__":
	#for prettyprint() in beautifulsoup
	reload(sys)
	sys.setdefaultencoding("utf-8")
	start = time.time()
	main()
	end = time.time()
	print "total time: ",end-start
