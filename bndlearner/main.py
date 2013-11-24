from bndlearner import BNDlearner
import os
import traceback
import sys
import time

from copy_reg import pickle
from types import MethodType

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
	
def _pickle_method(method):
	func_name = method.im_func.__name__
	obj = method.im_self
	cls = method.im_class
	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	for cls in cls.mro():
		try:
			func = cls.__dict__[func_name]
		except KeyError:
			pass
		else:
		    break
	return func.__get__(obj, cls)

if __name__ == "__main__":
	# for prettyprint() in beautifulsoup
	#reload(sys)
	#sys.setdefaultencoding("utf-8")
	pickle(MethodType, _pickle_method, _unpickle_method)
	start = time.time()
	main()
	end = time.time()
	print "total time: ",end-start
