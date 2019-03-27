from math import ceil, log2, pow

class SegTree():

	####################################################
	# Initializes the segtree                          #
	####################################################
	# Variables                                        #
	# array = Initial array to build the segtree       #
	####################################################
	def __init__(self, array):
		# storing the array size
		self.array_size = len(array)
		# calculating the tree size
		self.tree_size = 2*int(pow(2, ceil(log2(self.array_size)))) - 1
		# Building an empty tree
		self.tree = [None for x in range(self.tree_size)]
		# Filling the empty tree
		self.build(array, 0)
		print(self.tree)

	####################################################
	# Builds the segtree                               #
	####################################################
	# Variables                                        #
	# array = Fragment of the initial array            #
	# position = Position in the tree array            #
	####################################################
	def build(self, array, position):
		# If the array has just one value, puts it on the tree
		if(len(array) == 1):
			self.tree[position] = array[0]
		else:
			# Separate the array into two arrays, one to the left, one to the right of the segtree
			# Then the father nodes save the sum of the value of the children's nodes
			n = len(array)
			mid = ceil(n/2)
			self.tree[position] = self.build(array[0:mid], 2*position+1) + self.build(array[mid:n], 2*position+2)
		# Returns the value of the tree node
		return self.tree[position]

	####################################################
	# Returns the sum of the range [qs:qe] of an array #
	####################################################
	# Variables                                        #
	# ss = Start of the array                          #
	# se = End of the array                            #
	# qs = Start of the sum range                      #
	# qe = End of the sum range                        #
	# position = Position in the segtree               #
	####################################################
	def getSumUtil(self, ss, se, qs, qe, position):
		# if the tree node is inside the range of the search returns the node's value
		if(qs <= ss and qe >= se):
			return self.tree[position]

		# if the tree node is outside the range of the search returns 0
		if(se < qs or ss > qe):
			return 0

		mid = ceil((ss + se)/2)
		# Gets the sum of every node inside the range
		return self.getSumUtil(ss, mid, qs, qe, 2*position+1) + self.getSumUtil(mid+1, se, qs, qe, 2*position+2)


	####################################################
	# Calls getSumUtil                                 #
	####################################################
	# Variables                                        #
	# qs = Start of the sum range                      #
	# qe = End of the sum range                        #
	####################################################
	def getSum(self, qs, qe):
		return self.getSumUtil(0, self.array_size - 1, qs, qe, 0)


def main():
	arr = [1, 3, 5, 7, 9, 11]
	segtree = SegTree(arr)
	print(segtree.getSum(0, 3))

if __name__ == '__main__':
	main()

