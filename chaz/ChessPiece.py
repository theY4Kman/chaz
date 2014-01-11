from ChessPosition import *

class TYPE:P, N, B, R, Q, K = range(6)
TypeIcons = "PNBRQKpnbrqk"

class COLOR:WHITE, BLACK = range(2)

class ChessPiece:
	def __init__(self, type, color, pos):
		self.type = type
		self.color = color
		self.pos = pos
		self.hasMoved = False
		self.pawnJustMovedForwardTwice = False
	def icon(self):
		index = self.type
		if(self.color == COLOR.BLACK):index += TYPE.K+1
		return TypeIcons[index]
	def render(self):
		print(self.icon(), end='')