from copy_reg import pickle
from types import MethodType

"""Module for picking and unpickling instance methods of classes, as well as
for registering these functions with pickle.
Taken Steven Bethard's solution at: 
http://bytes.com/topic/python/answers/552476-why-cant-you-pickle-instancemethods#edit2155350
"""

# registers methods for pickling and unpickling a class instance method
def register_pickle_method():
	pickle(MethodType, _pickle_method, _unpickle_method)

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
