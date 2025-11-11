import torch
import itertools

def makeConnectionMatrix(connections):
	maximum = torch.max(connections)
	minimum = torch.min(connections)
	sideLength = maximum - minimum + 1
	conMatrix = torch.eye(sideLength)

	for j, i in connections:
		conMatrix[j, i] = 1
		conMatrix[i, j] = 1

	return conMatrix

def makeQubitToConnectionsList(connections):

	connectionMapping = [set() for _ in range(int(torch.max(connections)) + 1)]

	for q1, q2 in connections:
		q1_i = int(q1)
		q2_i = int(q2)
		connectionMapping[q1_i].add(q2_i)
		connectionMapping[q2_i].add(q1_i)
		
	return connectionMapping

def findConnections(circuits):
	# reshape so that the broadcast is done correctly to (n, q, q, l)
	# n = number of circuits, q = number of qubits, l = length of circuit
	# (n, q, 1, l)
	circuitsc = circuits.reshape(*circuits.shape[:2], 1, circuits.shape[-1])
	# (n, 1, q, l)
	circuitsr = circuits.reshape(circuits.shape[0], 1, *circuits.shape[1:])	
	sumMatrix = circuitsc + circuitsr
	sumIsZero = sumMatrix == 0
	notZeroGate = (circuitsc != 0)
	areSame = circuitsc == circuitsr
	connections = sumIsZero.logical_or(areSame).logical_and(notZeroGate)

	return connections

def findExistingConnectionPairs(gates, unique=True):
	cons = findConnections(gates)
	conList = cons.nonzero()
	conPairs = [[] for _ in range(cons.shape[0])]
	
	for i, q1, q2, _ in conList:
		if q1 == q2: continue

		conPairs[i].append(sorted([q1, q2]))
	
	conPairs = [torch.tensor(circuitPairs) for circuitPairs in conPairs]
	if unique:
		conPairs = [circuitPairs.unique(dim=0) for circuitPairs in conPairs]

	return conPairs


def findIllegal(circuits, possibleConnections):
	conMatrix = makeConnectionMatrix(connections=possibleConnections)
	# reshape to (1, q, q, 1) to broadcast the matrix for number of circuits and
	# the length of the circuits
	conMatrix = conMatrix.reshape(1, *conMatrix.shape, 1)

	parallelConnections = findConnections(circuits)
	illegalConnections = parallelConnections.logical_and(conMatrix == 0)

	qubitHasIllegal = torch.any(illegalConnections, dim=1)
	columnHasIllegal = torch.any(qubitHasIllegal, dim=1)

	return columnHasIllegal

def findConnectableQubits(connections, needed):
	combinations = itertools.combinations(range(len(connections)), needed)

	possibleSet = set()
	for c in combinations:
		conList = []
		for q in c:
			qubits = set(connections[q])
			qubits.add(q)
			conList.append(qubits)
		
		qubitIntersection = frozenset(set.intersection(*conList))

		if (len(qubitIntersection) >= needed):
			possibleSet.add(qubitIntersection)
	
	possibleQubits = [set(qi) for qi in possibleSet]
	return possibleQubits

		
		
		


