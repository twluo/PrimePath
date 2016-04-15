import math
import fileinput
import time

__author__ = "twluo@ucsd.edu, A98063711, elc036@ucsd.edu, A10842526, r1chin@ucsd.edu, A10653551"

#Prime Tests inspired by
#https://pythonism.wordpress.com/2008/05/04/looking-at-prime-numbers-in-python/

class PrimeClass(object):
	def __init__(self):
		pass

	def primalityTest(self, number):
		number = float(number)
		if number != 2.0 and number % 2 == 0:
			return False
		if number != 3.0 and number % 3 == 0:
			return False
		for j in range(1, int((number**0.5 + 1)/6.0 + 1)):
			if number % (6*j - 1) == 0:
				return False
			if number % (6*j + 1) == 0:
				return False
		return True

	def oneOff (self, number):
		toreturn = []
		for idx, c in enumerate(str(number)):
			num = list(str(number))
			for n in range(10):
				change = str(n)
				if change == c:
					continue
				num[idx] = change
				totest = ''.join(num)
				if len(num) == len(str(int(totest))):
					if self.primalityTest(totest):
						toreturn.append(int(totest))
		return toreturn

	def hammingDistance(self, x, y):
		if len(x) != len(y):
			return 
		numDiffs = 0
		for i, j in zip(x, y):
			if i != j:
				numDiffs += 1
		return numDiffs

	def getPossibleActions(self, currentPrime):
		return self.oneOff(currentPrime)

	def printPath(self, parentList, startingPrime, finalPrime):
		path = [finalPrime]
		while parentList[path[-1]][0] != startingPrime:
			path.append(parentList[path[-1]][0])
		path.append(startingPrime)
		path.reverse()
		return path

	def stepIn(self, currentPrime, pathSoFar, targetPrime, maxDepth):
		if currentPrime == targetPrime:
			return pathSoFar
		if len(pathSoFar) > maxDepth:
			return
		for child in self.getPossibleActions(currentPrime):
			if child not in pathSoFar:
				pathSoFar.append(child)
				path = self.stepIn(child, pathSoFar, targetPrime, maxDepth)
				if path is not None:
					return path
				pathSoFar.pop()

	def getPath(self, startingPrime, finalPrime):
		if startingPrime == finalPrime:
			return str(startingPrime)
		if not self.primalityTest(startingPrime):
			return "UNSOLVABLE"
		if int(math.log10(startingPrime)) != int(math.log10(finalPrime)):
			return "UNSOLVABLE"
		for maxDepth in range (0,8):
			path = self.stepIn(startingPrime, [startingPrime], finalPrime, maxDepth)
			if path is not None:
				return path
		return "UNSOLVABLE"

	def pathToStr(self, list):
		if type(list) == str:
			return list
		acc = ""
		for x in list:
			acc += str(x) + " "
		acc = acc[:-1]
		return acc
		
def main():
	wf = open("p3_output.txt", 'w')
	wf.truncate()
	for line in fileinput.input():
		primes = line.split()
		start = time.clock()
		wf.write("Running " + primes[0] + " " + primes[1] + "\n")
		pc = PrimeClass()
		output = pc.pathToStr(pc.getPath(int(primes[0]), int(primes[1])))
		print(output)
		wf.write(output + "\n")
		end = time.clock()
		total = end - start
		m, s = divmod(total, 60)
		h, m = divmod(m, 60)
		wf.write ("%d:%02d:%02d\n" % (h, m, s))
		wf.write (str(total) + "s\n")
		wf.write("\n")

if __name__ == '__main__':
	main()

