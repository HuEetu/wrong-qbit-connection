import torch
import connectionhelper

def removeIllegalTest():
	connections = torch.tensor(
		[(0, 1), (0, 2), (0, 3), (0, 4)]
	)
	gates = torch.tensor([
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
	])

	r = connectionhelper.removeIllegal(gates, connections)

	print(gates)
	print(r)

def existingPairsTest():
	gates = torch.tensor([
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
	])
	conPairs = connectionhelper.findExistingConnectionPairs(gates)
	print(conPairs)

if __name__ == "__main__":
	existingPairsTest()
	#transposeTest()
	#removeIllegalTest()