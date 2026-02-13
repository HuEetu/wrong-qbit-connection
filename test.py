import torch
import connectionhelper

def getTestGates(set=0):
	gateSets = [
		torch.tensor([
			[
				[1, 2, 3],
				[2, 3, 0],
				[3, 5, 0],
				[-3, 8, -3],
				[-1, 0, 2]
			],
			[
				[1, 0, 3],
				[2, 3, 0],
				[3, -3, -1],
				[-3, 8, -3],
				[-1, 0, 1]
			]
		]),
		torch.tensor([
			[
				[1, 2, 3],
				[2, 3, 0],
				[3, 5, 0],
				[-3, 8, -3],
				[-1, 0, 2]
			],
			[
				[1, 0, 3],
				[2, 3, 0],
				[3, -3, -1],
				[-3, 8, -3],
				[-1, 0, 1]
			],
			[
				[1, 2, 3],
				[2, 3, 0],
				[0, 5, 0],
				[0, 8, -3],
				[-1, 0, 2]
			]
		]),
		torch.tensor([
			[
				[1, 2, 3, 9, 9, 9],
				[2, 3, 0, 9, 9, 9],
				[3, 5, 0, 9, 9, 9],
				[-3, 8, -3, 9, 9, 9],
				[-1, 0, 2, 9, 9, 9]
			],
			[
				[1, 0, 3, 9, 9, 9],
				[2, 3, 0, 9, 9, 9],
				[3, -3, -1, 9, 9, 9],
				[-3, 8, -3, 9, 9, 9],
				[-1, 0, 1, 9, 9, 9]
			],
			[
				[1, 2, 3, 9, 9, 9],
				[2, 3, 0, 9, 9, 9],
				[0, 5, 0, 9, 9, 9],
				[0, 8, -3, 9, 9, 9],
				[-1, 0, 2, 9, 9, 9]
			]
		])
	]

	return gateSets[set]

def getTestConnections(set=0):
	connectionSets =[
		torch.tensor([(0, 1), (0, 2), (0, 3), (0, 4)]),
		torch.tensor([(0,1), (0,2), (0,3), (0,4), (1, 2)]),
		torch.tensor([
			(0, 1), (0, 2), (0, 3), (0, 4),
			(1, 2), (1, 3),
			(2, 4),
			(3, 4)
		])
	]

	return connectionSets[set]


def removeIllegalTest():
	connections = getTestConnections()
	gates = getTestGates()

	r = connectionhelper.findIllegal(gates, connections)

	print(gates)
	print(r)

def existingPairsTest():
	gates = getTestGates()
	conPairs = connectionhelper.findExistingConnectionPairs(gates)
	print(conPairs)

def findConnectionsTest():
	gates = getTestGates()

	cm = connectionhelper.findConnections(gates)
	print(cm.shape)
	print(cm)

def makeQubitToConnectionsTest():
	cons = getTestConnections(1)
	consMap = connectionhelper.makeQubitToConnectionsList(cons)
	print(consMap)

def possibleConnectionsTest():
	cons = getTestConnections(1)
	consList = connectionhelper.makeQubitToConnectionsList(cons)


	possible = connectionhelper.findConnectableQubits(consList, 2)

	print(possible)

def getLegalAndIllegalIndicesTest():
	gates = getTestGates(1)
	cons = getTestConnections()

	good, bad = connectionhelper.getLegalAndIllegalCircuitIndices(gates, cons)
	print(gates)
	print(cons)
	print(good)
	print(bad)

def connectableComplicateTest():
	cons = getTestConnections(2)
	consList = connectionhelper.makeQubitToConnectionsList(cons)
	print(consList)


	possible = connectionhelper.findConnectableQubits(consList, 3)

	print(possible)

def findIllegalShapeTest():
	gates = getTestGates(1)
	cons = getTestConnections(2)

	good, bad = connectionhelper.getLegalAndIllegalCircuitIndices(gates, cons)

	print(good.shape)
	print(good)
	print(bad.shape)

def paddingTest():
	gates = getTestGates(2)
	cons = getTestConnections(2)

	ignore = torch.tensor([0,9])
	good, bad = connectionhelper.getLegalAndIllegalCircuitIndices(
		gates, cons, ignore=ignore
	)
	print(good.shape)
	print(good)
	print(bad.shape)
	print(bad)

if __name__ == "__main__":
	existingPairsTest()
	removeIllegalTest()
	possibleConnectionsTest()
	makeQubitToConnectionsTest()
	findConnectionsTest()
	getLegalAndIllegalIndicesTest()
	connectableComplicateTest()
	findIllegalShapeTest()
	paddingTest()
