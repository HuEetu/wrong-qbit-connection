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

def findConnections(circuits, ignore=torch.tensor([0])):
	# reshape so that the broadcast is done correctly to (n, q, q, l)
	# n = number of circuits, q = number of qubits, l = length of circuit
	# (n, q, 1, l)
	circuitsc = circuits.reshape(*circuits.shape[:2], 1, circuits.shape[-1])
	# (n, 1, q, l)
	circuitsr = circuits.reshape(circuits.shape[0], 1, *circuits.shape[1:])	
	sumMatrix = circuitsc + circuitsr
	sumIsZero = sumMatrix == 0
	notIgnoredGate = torch.isin(circuitsc, ignore, invert=True)
	areSame = circuitsc == circuitsr
	connections = sumIsZero.logical_or(areSame).logical_and(notIgnoredGate)

	return connections

def findExistingConnectionPairs(gates, unique=True, ignore=torch.tensor([0])):
	cons = findConnections(gates, ignore=ignore)
	conList = cons.nonzero()
	conPairs = [[] for _ in range(cons.shape[0])]
	
	for i, q1, q2, _ in conList:
		if q1 == q2: continue

		conPairs[i].append(sorted([q1, q2]))
	
	conPairs = [torch.tensor(circuitPairs) for circuitPairs in conPairs]
	if unique:
		conPairs = [circuitPairs.unique(dim=0) for circuitPairs in conPairs]

	return conPairs


def findIllegal(circuits, possibleConnections, ignore=torch.tensor([0])):
	conMatrix = makeConnectionMatrix(connections=possibleConnections)
	# reshape to (1, q, q, 1) to broadcast the matrix for number of circuits and
	# the length of the circuits
	conMatrix = conMatrix.reshape(1, *conMatrix.shape, 1)

	parallelConnections = findConnections(circuits, ignore=ignore)
	illegalConnections = parallelConnections.logical_and(conMatrix == 0)

	qubitHasIllegal = torch.any(illegalConnections, dim=1)
	columnHasIllegal = torch.any(qubitHasIllegal, dim=1)

	return columnHasIllegal

def findConnectableQubits(connections, needed):
	combinations = itertools.combinations(range(len(connections)), needed)

	possibleQubits = []
	for c in combinations:
		c_set = set(c)
		all_connected = True
		for q in c:
			qubits = set(connections[q])
			qubits.add(q)
			is_connected = c_set.issubset(qubits)
			all_connected = all_connected and is_connected
		

		if (all_connected):
			possibleQubits.append(c_set)

	return possibleQubits

		
def getLegalAndIllegalCircuitIndices(
	circuits, possibleConnections, ignore=torch.tensor([0])
):
	column_has_illegal = findIllegal(circuits, possibleConnections, ignore)
	column_has_illegal.shape
	circuit_has_illegal = column_has_illegal.any(dim=1)
	good = (circuit_has_illegal == 0).nonzero()
	bad = circuit_has_illegal.nonzero()

	return good.squeeze(dim=1), bad.squeeze(dim=1)