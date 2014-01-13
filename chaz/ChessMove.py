# http://en.wikipedia.org/wiki/Algebraic_notation_(chess)
# http://en.wikipedia.org/wiki/Portable_Game_Notation
# http://chessprogramming.wikispaces.com/Algebraic+Chess+Notation

'''
Long Algebraic Notation will take on the form
<LAN move descriptor piece moves> ::= <Piece symbol><from square>['-'|'x']<to square>
<LAN move descriptor pawn moves>  ::= <from square>['-'|'x']<to square>[<promoted to>]
<Piece symbol> ::= 'N' | 'B' | 'R' | 'Q' | 'K'
'''

from ChessPiece import *

class ChessMove:
	def __init__(self, *args):
		self.isCaptureMove = False
		self.isPromoteMove = False
		self.isKingsideCastle = False
		self.isQueensideCastle = False
		if(len(args) == 1):			# Passed a movetext to be parsed
			assert(args[0].__class__ == str)
			self.notation = args[0]
			if(self.notation == "O.O"):self.isKingsideCastle = True
			if(self.notation == "O.O.O"):self.isQueensideCastle = True
			if(self.isKingsideCastle or self.isQueensideCastle):return
			assert('-' in self.notation or 'x' in self.notation)
			if 'x' in self.notation:self.isCaptureMove = True
			if(self.notation[0] in FileNames):self.type = TYPE.P
			else:self.type = TypeForIcon(self.notation[0])
			if(self.notation[-1:] in TypeIcons):
				self.isPromoteMove = True
				self.promoteType = TypeForIcon(self.notation[-1:])
			positions = self.notation
			if(self.type != TYPE.P):positions = positions[1:]
			if(self.isPromoteMove):positions = positions[:-1]
			if(self.isCaptureMove):moves = positions.split('x')
			else:moves = positions.split('-')
			self.fromPosition = ChessPosition(moves[0])
			self.toPosition = ChessPosition(moves[1])
		if(len(args) == 2):			# Passed piece, end_position
			assert(args[0].__class__ == ChessPiece)
			assert(args[1].__class__ == ChessPosition)
			raise NotImplementedError()
	def log(self):
		print(self.notation)
		if(self.isCaptureMove):print("Capture Move")
		if(self.isPromoteMove):print("Promote Move")