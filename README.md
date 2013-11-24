bndlearner: bacon number distribution learner
========

bndlearner is a module for learning the distribution vector of the bacon number for a provided list of actors, using Google's builtin tool for looking up the bacon number of a particular actor.

Requirements
------------

bndlearner requires the following python modules:
* requests
* bs4 (BeautifulSoup 4)
* numpy

For more information, refer to requirements.txt

Usage
------------
First, create an object of class BNDlearner as follows:
`bndl = BNDlearner(maxBaconNumber, numProcs)`
Here, `maxBaconNumber` is the maximum bacon number accounted for in the distribution, and `numProcs` is the number of processes to run the computation on.

To then use this object to learn the distribution of the bacon number for a list of actors, make the following method call:
`bndl.learnBaconNumberDistribution(actors, normalize)`
where `actors` is a list of strings specifying names of actors, and `normalize` is a boolean specifying whether the distribution should be normalized.

To learn the distribution for a group of actors specified in a file named `actorsFile`, use the following syntax:
`bndl.learnBaconNumberDistributionFromFile(actorsFile)`

The resulting distribution will both be returned, and assigned to the instance variable bndl.dist.
