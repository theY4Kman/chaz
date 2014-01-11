import copy
from ChessPiece import *

class ChessBoard:
	def __init__(self, *args):
		if len(args) == 0:
			self.pieces = []
			self.activeColor = COLOR.WHITE
			self.reset()
			self.halfMove = 0
			self.fullMove = 1
		elif len(args) == 1:
			# Set board to mimic FEN input
			raise NotImplementedError()
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
		print(self.FENNotation())
	def isAValidMove(self, move):
		# Move shall be in the format 'FromTo' e.g. 'a2a3'
		return True
	def FENNotation(self):
		emptyCount = 0
		retVal = ""
		for rank in range(7, -1, -1):
			for file in range(0, 8):
				piece = self.pieceAt(ChessPosition(file, rank))
				if(piece):
					if(emptyCount > 0):
						retVal += str(emptyCount)
						emptyCount = 0
					retVal += piece.icon()
				else:emptyCount = emptyCount + 1
			if(emptyCount > 0):retVal += str(emptyCount)
			emptyCount = 0
			if(rank != 0):retVal += "/"
		retVal += " "
		if(self.activeColor == COLOR.WHITE):retVal += "w"
		if(self.activeColor == COLOR.BLACK):retVal += "b"
		retVal += " "
		castling = ""
		whiteKing = self.pieceAt(ChessPosition("e1"))
		whiteQueenSideRook = self.pieceAt(ChessPosition("a1"))
		whiteKingSideRook = self.pieceAt(ChessPosition("h1"))
		blackKing = self.pieceAt(ChessPosition("e8"))
		blackQueenSideRook = self.pieceAt(ChessPosition("a8"))
		blackKingSideRook = self.pieceAt(ChessPosition("h8"))
		if((whiteKing is not None and whiteKingSideRook is not None) and (not whiteKing.hasMoved and not whiteKingSideRook.hasMoved)):castling += "K"
		if((whiteKing is not None and whiteQueenSideRook is not None) and (not whiteKing.hasMoved and not whiteQueenSideRook.hasMoved)):castling += "Q"
		if((blackKing is not None and blackKingSideRook is not None) and (not blackKing.hasMoved and not blackKingSideRook.hasMoved)):castling += "k"
		if((blackKing is not None and blackQueenSideRook is not None) and (not blackKing.hasMoved and not blackQueenSideRook.hasMoved)):castling += "q"
		if(castling == ""):castling += "-"
		retVal += castling
		retVal += " "
		# Oddly enough the En Passant point is the spot 'behind' the moved pawn
		enPassant = ""
		for d in range(0, len(self.pieces)):
			if(self.pieces[d].pawnJustMovedForwardTwice):
				pos = copy.deepcopy(self.pieces[d].pos)
				direction = 1
				if(self.pieces[d].color == COLOR.BLACK):direction = -1
				pos.rank -= direction
				enPassant = pos.toParsableString()
				break
		if(enPassant == ""):enPassant = "-"
		retVal += enPassant
		retVal += " "
		retVal += str(self.halfMove)
		retVal += " "
		retVal += str(self.fullMove)
		return retVal