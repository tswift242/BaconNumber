from bndlearner import BNDlearner
import sys

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
	main()
