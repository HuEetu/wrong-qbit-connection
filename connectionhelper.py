import torch

def makeConnectionMatrix(connections):
	maximum = torch.max(connections)
	minimum = torch.min(connections)
	sideLength = maximum - minimum + 1
	conMatrix = torch.zeros(sideLength, sideLength)

	for j, i in connections:
		conMatrix[j, i] = 1
		conMatrix[i, j] = 1

	# reshape to (1, q, q, 1) to broadcast the matrix for number of circuits and
	# the length of the circuits
	return conMatrix.reshape(1, *conMatrix.shape, 1)

def findConnections(circuits):
	# reshape so that the broadcast is done correctly
	# from (b, q, l) to (b, q, q, l)
	circuitsc = circuits.reshape(*circuits.shape[:2], 1, circuits.shape[-1])
	circuitsr = circuits.reshape(circuits.shape[0], 1, *circuits.shape[1:])	
	sumMatrix = circuitsc + circuitsr
	sumIsZero = sumMatrix == 0
	notZeroGate = (circuitsc != 0)
	connections = notZeroGate.logical_and(sumIsZero)

	return connections

def findExistingConnectionPairs(gates, unique=True):
	cons = findConnections(gates)
	conList = cons.nonzero()
	conPairs = torch.tensor([sorted(p[1:3]) for p in conList])
	if unique:
		conPairs = conPairs.unique(dim=0)

	return conPairs


def removeIllegal(circuits, possibleConnections):
	conMatrix = makeConnectionMatrix(connections=possibleConnections)

	parallelConnections = findConnections(circuits)
	illegalConnections = parallelConnections.logical_and(conMatrix == 0)
	legalConnections = parallelConnections.logical_and(conMatrix == 1)

	hasIllegal = torch.any(illegalConnections, dim=1)
	hasLegal = torch.any(legalConnections, dim=1)
	allIllegal = hasIllegal.logical_and(hasLegal.logical_not())

	return allIllegal