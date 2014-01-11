class TYPE:P, N, B, R, Q, K = range(6)
TypeIcons = "PNBRQKpnbrqk"

class COLOR:WHITE, BLACK = range(2)

class ChessPosition:
	def __init__(self, *args):
		if len(args) == 1:		# String such as "a3" or "h7"
			self.file = ord((args[0][0])) - ord('a')
			self.rank = (int)(args[0][1]) - 1
		elif len(args) == 2:	# Index of file followed by index of row
			self.file = args[0]
			self.rank = args[1]

class ChessPiece:
	def __init__(self, type, color, pos):
		self.type = type
		self.color = color
		self.pos = pos
	def icon(self):
		index = self.type
		if(self.color == COLOR.BLACK):index += TYPE.K+1
		return TypeIcons[index]
	def render(self):
		print(self.icon(), end='')

class ChessBoard:
	pieces = []
	def __init__(self):
		self.reset()
	def reset(self):
		for d in range(0, 8):
			self.pieces.append(ChessPiece(TYPE.P, COLOR.WHITE, ChessPosition(d, 1)))
		self.pieces.append(ChessPiece(TYPE.R, COLOR.WHITE, ChessPosition("a1")))
		self.pieces.append(ChessPiece(TYPE.N, COLOR.WHITE, ChessPosition("b1")))
		self.pieces.append(ChessPiece(TYPE.B, COLOR.WHITE, ChessPosition("c1")))
		self.pieces.append(ChessPiece(TYPE.Q, COLOR.WHITE, ChessPosition("d1")))
		self.pieces.append(ChessPiece(TYPE.K, COLOR.WHITE, ChessPosition("e1")))
		self.pieces.append(ChessPiece(TYPE.B, COLOR.WHITE, ChessPosition("f1")))
		self.pieces.append(ChessPiece(TYPE.N, COLOR.WHITE, ChessPosition("g1")))
		self.pieces.append(ChessPiece(TYPE.R, COLOR.WHITE, ChessPosition("h1")))
		for d in range(0, 8):
			self.pieces.append(ChessPiece(TYPE.P, COLOR.BLACK, ChessPosition(d, 6)))
		self.pieces.append(ChessPiece(TYPE.R, COLOR.BLACK, ChessPosition("a8")))
		self.pieces.append(ChessPiece(TYPE.N, COLOR.BLACK, ChessPosition("b8")))
		self.pieces.append(ChessPiece(TYPE.B, COLOR.BLACK, ChessPosition("c8")))
		self.pieces.append(ChessPiece(TYPE.Q, COLOR.BLACK, ChessPosition("d8")))
		self.pieces.append(ChessPiece(TYPE.K, COLOR.BLACK, ChessPosition("e8")))
		self.pieces.append(ChessPiece(TYPE.B, COLOR.BLACK, ChessPosition("f8")))
		self.pieces.append(ChessPiece(TYPE.N, COLOR.BLACK, ChessPosition("g8")))
		self.pieces.append(ChessPiece(TYPE.R, COLOR.BLACK, ChessPosition("h8")))
	def pieceAt(self, pos):
		for ChessPiece in self.pieces:
			if(ChessPiece.pos.file == pos.file and ChessPiece.pos.rank == pos.rank):
				return ChessPiece
	def render(self):
		print('-' * 10)
		for rank in range(7, -1, -1):
			print('|', end='')
			for file in range(0, 8):
				piece = self.pieceAt(ChessPosition(file, rank))
				if(piece):piece.render()
				else:
					if(rank%2 == 0 and file%2 != 0):print(' ', end='')
					elif(rank%2 != 0 and file%2 == 0):print(' ', end='')
					else:print("\u2592", end='')
			print('|', end='')
			print('')
		print('-' * 10)