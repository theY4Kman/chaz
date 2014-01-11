FileNames = "abcdefgh"

class ChessPosition:
	def __init__(self, *args):
		if len(args) == 1:		# String such as "a3" or "h7"
			self.file = ord((args[0][0])) - ord('a')
			self.rank = (int)(args[0][1]) - 1
		elif len(args) == 2:	# Index of file followed by index of row
			self.file = args[0]
			self.rank = args[1]
	def toParsableString(self):
		return FileNames[self.file] + str(self.rank + 1)