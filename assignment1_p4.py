import fileinput
import time
try:
    import Queue as queue  # ver. < 3.0
except ImportError:
    import queue as queue

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
        toreturn = set()
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
                        toreturn.add(int(totest))
        return toreturn

    def hammingDistance(self, x, y):
        if len(x) != len(y):
            return
        numDiffs = 0
        for i, j in zip_longest(x, y):
            if i != j:
                numDiffs += 1
        return numDiffs

    def getPossibleActions(self, currentPrime):
            return self.oneOff(currentPrime)

    def printPath(self, parentList, startingPrime, finalPrime):
        path = [finalPrime]
        while parentList[path[-1]] != startingPrime:
            path.append(parentList[path[-1]])
        path.append(startingPrime)
        path.reverse()
        return path


    def getPath(self, startingPrime, finalPrime):
        if startingPrime == finalPrime:
            return str(startingPrime)
        forwardList = {}
        backwardList = {}
        qi = queue.Queue()
        qj = queue.Queue()
        qi.put(startingPrime)
        qj.put(finalPrime)
        while not qi.empty() and not qj.empty():
            if not qi.empty():
                currentPrimeForward = qi.get()
                if currentPrimeForward == finalPrime or currentPrimeForward in backwardList:
                    return self.printPathBiDi(forwardList, backwardList, currentPrimeForward, startingPrime, finalPrime)
                for childForward in self.getPossibleActions(currentPrimeForward):
                    if childForward not in forwardList:
                        forwardList[childForward] = currentPrimeForward
                        qi.put(childForward)
                    #Resolve dup childForward???
            if not qj.empty():
                currentPrimeBackward = qj.get()
                if currentPrimeBackward == startingPrime or currentPrimeBackward in forwardList:
                    return self.printPathBiDi(forwardList, backwardList, currentPrimeBackward, startingPrime, finalPrime)
                for childBackward in self.getPossibleActions(currentPrimeBackward):
                    if childBackward not in backwardList:
                        backwardList[childBackward] = currentPrimeBackward
                        qj.put(childBackward)
                    #Resolve Dup???
        return 'UNSOLVABLE', ''

    def printPathBiDi(self, forwardList, backwardList, cp, startingPrime, finalPrime):
        forwardpath = [cp]
        backwardpath = [cp]
        while forwardList[forwardpath[-1]] != startingPrime:
            forwardpath.append(forwardList[forwardpath[-1]])
        if backwardList:
            while backwardList[backwardpath[-1]] != finalPrime:
                #print(backwardpath[-1], backwardList[backwardpath[-1]])
                backwardpath.append(backwardList[backwardpath[-1]])
            backwardpath.append(finalPrime)
        forwardpath.append(startingPrime)
        forwardpath.reverse()
        backwardpath.reverse()
        #print (forwardpath + backwardpath)
        return forwardpath, backwardpath

    def pathToStr(self, list):
        if type(list) == str:
            return list
        acc = ""
        for x in list:
            acc += str(x) + " "
        acc = acc[:-1]
        return acc

def main():
    wf = open("p4_output.txt", 'w')
    wf.truncate()
    for line in fileinput.input():
        primes = line.split()
        start = time.clock()
        wf.write("Running " + primes[0] + " " + primes[1] + "\n")
        pc = PrimeClass()
        fpath, bpath = pc.getPath(int(primes[0]), int(primes[1]))
        output = (pc.pathToStr(fpath) + "\n" + pc.pathToStr(bpath) + ("\n" if (bpath != '') else bpath))
        print(output)
        wf.write(output)
        end = time.clock()
        total = end - start
        m, s = divmod(total, 60)
        h, m = divmod(m, 60)
        wf.write ("%d:%02d:%02d\n" % (h, m, s))
        wf.write (str(total) + "s\n")
        wf.write("\n")

if __name__ == '__main__':
    main()

