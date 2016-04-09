from itertools import zip_longest
import fileinput

__author__ = "twluo@ucsd.edu, A98063711, elc036@ucsd.edu, A10842526, r1chin@ucsd.edu, A10653551"

class PrimeClass(object):
	def __init__(self, target):
		self.target = str(target)
		n = int(''.join(['9' for __ in self.target]))
		self.primeList = self.generatePrimes(n)

	def padLeftZero(self, x, y):
		diff = len(x) - len(y)
		if diff == 0:
			return (x, y)
		elif diff < 0:
			return (x.zfill(len(y)), y)
		else:
			return (x, y.zfill(len(x)))

	def generatePrimes(self, n):
		a = list(range(2, n))
		for x in a:
		  comp = []
		  for y in range(a.index(x),len(a)):
		    q = x * a[y]
		    if q <= max(a):
		      comp.append(q)
		    else:
		      break
		  for z in comp:
		    a.remove(z)	
		return [self.padLeftZero(str(i), self.target)[0] for i in a]

	def hammingDistance(self, x, y):
		numDiffs = 0
		for i, j in zip_longest(x, y):
			if i != j:
				numDiffs += 1
		return numDiffs

	def getPossibleActions(self, currentPrime):
		possibleActions = []
		for i in self.primeList:
			if self.hammingDistance(currentPrime, i) == 1:
				possibleActions.append(i)
		return possibleActions

	def printPath(self, parentList, startingPrime, finalPrime):
		path = [finalPrime]
		while parentList[path[-1]][0] != startingPrime:
			path.append(parentList[path[-1]][0])
		path.append(startingPrime)
		path.reverse()
		return path


	def getPath(self, startingPrime, finalPrime):
		for i in range(0,8):
			visited = set()
			parentList = {}
			queue = []
			queue.append((startingPrime, 0))
			while queue:
				currentPrime, currentCost = queue.pop()
				currentCost = currentCost + 1
				visited.add(currentPrime)
				if currentPrime == finalPrime:
					return self.printPath(parentList, startingPrime, finalPrime)
				for child in self.getPossibleActions(currentPrime):
					if child not in parentList:
						parentList[child] = (currentPrime, currentCost)
					elif parentList[child][1] >= currentCost:
						parentList[child] = (currentPrime, currentCost)
					if child not in visited and currentCost <= i:
						queue.append((child, currentCost)) 
		return "UNSOLVABLE"

def main():
	for line in fileinput.input():
		primes = line.split()
		pc = PrimeClass(primes[0])
		print(pc.getPath(primes[0], primes[1]))

if __name__ == '__main__':
	main()

