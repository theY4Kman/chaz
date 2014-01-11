from ChessPosition import *
from ChessBoard import *

class TYPE:P, N, B, R, Q, K = range(6)
TypeIcons = "PNBRQKpnbrqk"

class COLOR:WHITE, BLACK = range(2)

# Pawn Movement: Finished
#	Pawn promotion will occur via board move method
# Knight Movement: Finished
# Bishop Movement: Finished
# Rook Movement: Finished
# Queen Movement: Finished
# King Movement: Unfinished
#	Currently King can move into check

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
	def possibleMovementPositionsOnBoard(self, board):
		retVal = []
		if(self.type == TYPE.P):
			if(self.color == COLOR.WHITE):direction = 1;
			if(self.color == COLOR.BLACK):direction = -1;
			# Move directly ahead
			canPlace = True
			_pos = copy.deepcopy(self.pos)
			_pos.rank += 1*direction
			if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
			if(not _pos.isOnBoard()):canPlace = False
			_pos.metaData = POSITION_METADATA.MOVEMENT;
			if(canPlace):retVal.append(_pos)
			# Directly ahead twice on first move
			canPlace = True
			_pos = copy.deepcopy(self.pos)
			_pos.rank += 2*direction
			if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
			if(not _pos.isOnBoard()):canPlace = False
			if(self.color == COLOR.WHITE and self.pos.rank != 1):canPlace = False
			if(self.color == COLOR.BLACK and self.pos.rank != 6):canPlace = False
			_pos.metaData = POSITION_METADATA.MOVEMENT
			if(canPlace):retVal.append(_pos)
			# Diagonally forward left if occupied by an opponent
			canPlace = False
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, -1, direction)
			if(occupant and occupant.color != self.color):
				canPlace = True
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK;
			if(canPlace):retVal.append(_pos)
			# Diagonally forward right if occupied by an opponent
			canPlace = False
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, 1, direction)
			if(occupant and occupant.color != self.color):
				canPlace = True
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK;
			if(canPlace):retVal.append(_pos)
		elif(self.type == TYPE.N):
			# -2, 1
			_pos = copy.deepcopy(self.pos)
			_pos.file += -2
			_pos.rank += 1
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# -1, 2
			_pos = copy.deepcopy(self.pos)
			_pos.file += -1
			_pos.rank += 2
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# 1, 2
			_pos = copy.deepcopy(self.pos)
			_pos.file += 1
			_pos.rank += 2
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# 2, 1
			_pos = copy.deepcopy(self.pos)
			_pos.file += 2
			_pos.rank += 1
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# 2, -1
			_pos = copy.deepcopy(self.pos)
			_pos.file += 2
			_pos.rank += -1
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# 1, -2
			_pos = copy.deepcopy(self.pos)
			_pos.file += 1
			_pos.rank += -2
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# -1, -2
			_pos = copy.deepcopy(self.pos)
			_pos.file += -1
			_pos.rank += -2
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
			# -2, -1
			_pos = copy.deepcopy(self.pos)
			_pos.file += -2
			_pos.rank += -1
			occupant = board.pieceAt(_pos)
			if(_pos.isOnBoard()):
				if(occupant):_pos.metaData = POSITION_METADATA.ATTACK
				else:_pos.metaData = POSITION_METADATA.MOVEMENT
				shouldAdd = True
				if(occupant and occupant.color == self.color):shouldAdd = False
				if(shouldAdd):retVal.append(_pos)
		elif(self.type == TYPE.B):
			# Movement Diagonally Up Left
			xDirection = -1
			yDirection = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Up Right
			xDirection = 1
			yDirection = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Left
			xDirection = -1
			yDirection = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Right
			xDirection = 1
			yDirection = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Attack Diagonally Up Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, -1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Up Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, 1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, 1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, -1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
		elif(self.type == TYPE.R):
			# Movement Horizontally Left
			direction = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Horizontally Right
			direction = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Up
			direction = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Down
			direction = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Attack Left
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 8, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Right
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 8, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Up
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 8, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Down
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 8, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
		elif(self.type == TYPE.Q):
			# Movement Diagonally Up Left
			xDirection = -1
			yDirection = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Up Right
			xDirection = 1
			yDirection = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Left
			xDirection = -1
			yDirection = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Right
			xDirection = 1
			yDirection = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Horizontally Left
			direction = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Horizontally Right
			direction = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Up
			direction = 1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Down
			direction = -1
			for d in range(1, 8):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Attack Diagonally Up Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, -1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Up Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, 1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, 1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 8, -1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Left
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 8, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Right
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 8, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Up
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 8, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Down
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 8, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
		elif(self.type == TYPE.K):
			# Movement Diagonally Up Left
			xDirection = -1
			yDirection = 1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Up Right
			xDirection = 1
			yDirection = 1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Left
			xDirection = -1
			yDirection = -1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Diagonally Down Right
			xDirection = 1
			yDirection = -1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*xDirection
				_pos.rank += d*yDirection
				if(not board.emptyDirectDiagonalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Horizontally Left
			direction = -1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Horizontally Right
			direction = 1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.file += d*direction
				if(not board.emptyDirectHorizontalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Up
			direction = 1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Movement Vertically Down
			direction = -1
			for d in range(1, 2):
				canPlace = True
				_pos = copy.deepcopy(self.pos)
				_pos.rank += d*direction
				if(not board.emptyDirectVerticalTo(self.pos, _pos)):canPlace = False
				if(not _pos.isOnBoard()):canPlace = False
				_pos.metaData = POSITION_METADATA.MOVEMENT
				if(canPlace):retVal.append(_pos)
			# Attack Diagonally Up Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, -1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Up Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, 1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Right
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, 1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Diagonally Down Left
			occupant = board.firstDiagonallyCollidedPieceWithinRange(self.pos, 1, -1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Left
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Right
			occupant = board.firstHorizontallyCollidedPieceWithinRange(self.pos, 1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Up
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 1, 1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
			# Attack Down
			occupant = board.firstVerticallyCollidedPieceWithinRange(self.pos, 1, -1)
			if(occupant and occupant.color != self.color):
				_pos = copy.deepcopy(occupant.pos)
				_pos.metaData = POSITION_METADATA.ATTACK
				retVal.append(_pos)
		return retVal