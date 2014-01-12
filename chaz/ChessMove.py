# http://en.wikipedia.org/wiki/Algebraic_notation_(chess)
# http://en.wikipedia.org/wiki/Portable_Game_Notation

from ChessPiece import *

class ChessMove:
	def __init__(self, *args):
		self.isCaptureMove = False
		self.isEnPassantMove = False
		self.isPromotionMove = False
		self.isKingsideCastle = False
		self.isQueensideCastle = False

		if(len(args) == 1):			# Passed a movetext to be parsed
			assert(args[0].__class__ == str)
			self.notation = args[0]
			if(self.notation[0] in FileNames):self.type = TYPE.P
			else:self.type = TypeForIcon(self.notation[0])
			if("x" in self.notation):self.isCaptureMove = True
			if("e.p." in self.notation):self.isEnPassantMove = True
			if("=" in self.notation):self.isPromotionMove = True
			if("O.O" in self.notation):
				self.isKingsideCastle = True
				self.isQueensideCastle = False
				self.type = TYPE.K
			if("O.O.O" in self.notation):
				self.isKingsideCastle = False
				self.isQueensideCastle = True
				self.type = TYPE.K
		if(len(args) == 3):			# Passed start_position, end_position, ChessBoard
			assert(args[0].__class__ == ChessPosition)
			assert(args[1].__class__ == ChessPosition)
			assert(args[2].__class__ == ChessBoard)
			raise NotImplementedError()
	def log(self):
		print("Logging:", self.notation)
		print("Type:", TypeIcons[self.type])
		if(self.isCaptureMove):print("capture move")
		if(self.isEnPassantMove):print("en passant move")
		if(self.isPromotionMove):print("pawn promotion move")
		if(self.isKingsideCastle):print("castle kingside move")
		if(self.isQueensideCastle):print("castle queenside move")
	def isEqualTo(self, move):		# In the event that moves are formatted differently but are the same exact moves
		raise NotImplementedError()