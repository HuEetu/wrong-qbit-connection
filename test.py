import torch

def makeConnectionMatrix(connections):
	maximum = torch.max(connections)
	minimum = torch.min(connections)
	sideLength = maximum - minimum + 1
	conMatrix = torch.zeros(sideLength, sideLength)

	for j, i in connections:
		conMatrix[j, i] = 1
		conMatrix[i, j] = 1
	return conMatrix

def findConnections(gates):
	sumMatrix = gates + gates.T
	sumIsZero = sumMatrix == 0
	notZeroGate = (gates != 0)
	connections = notZeroGate.logical_and(sumIsZero)

	return connections

def findExistingConnectionPairs(gates, unique=True):
	cons = findConnections(gates)
	conList = cons.nonzero()
	conPairs = torch.tensor([sorted(p) for p in conList])
	if unique:
		conPairs = conPairs.unique(dim=0)

	return conPairs


def removeIllegal(parallelGates, possibleConnections):
	conMatrix = makeConnectionMatrix(connections=possibleConnections)

	parallelConnections = findConnections(parallelGates)
	illegalConnections = parallelConnections.logical_and(conMatrix == 0)
	legalConnections = parallelConnections.logical_and(conMatrix == 1)

	hasIllegal = torch.any(illegalConnections, dim=1)
	hasLegal = torch.any(legalConnections, dim=1)
	allIllegal = hasIllegal.logical_and(hasLegal.logical_not())

	return allIllegal

def removeIllegalTest():
	connections = torch.tensor(
		[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
	)
	gates = torch.tensor([[1, 2, 3, -1, 4, 2, -2, 0, 0]])
	r = removeIllegal(gates, connections)

	print(gates)
	print(r)

def existingPairsTest():
	gates = torch.tensor([[1, 2, 3, -1, 4, 2, -2, 0, 0]])
	print(gates.nonzero(as_tuple=True))
	conPairs = findExistingConnectionPairs(gates)
	print(conPairs)

if __name__ == "__main__":
	existingPairsTest()