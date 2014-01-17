from __future__ import print_function

from ChessPosition import *
from ChessBoard import *


class TYPE:P, N, B, R, Q, K = range(6)
TypeIcons = "PNBRQKpnbrqk"

# I don't like this, refactor later
def TypeForIcon(icon):
    if(icon == 'P'):return TYPE.P
    if(icon == 'N'):return TYPE.N
    if(icon == 'B'):return TYPE.B
    if(icon == 'R'):return TYPE.R
    if(icon == 'Q'):return TYPE.Q
    if(icon == 'K'):return TYPE.K
    if(icon == 'p'):return TYPE.P
    if(icon == 'n'):return TYPE.N
    if(icon == 'b'):return TYPE.B
    if(icon == 'r'):return TYPE.R
    if(icon == 'q'):return TYPE.Q
    if(icon == 'k'):return TYPE.K


class COLOR:WHITE, BLACK = range(2)

# Pawn Movement: Finished
#   Pawn promotion will occur via board move method
# Knight Movement: Finished
# Bishop Movement: Finished
# Rook Movement: Finished
# Queen Movement: Finished
# King Movement: Unfinished
#   Currently King can move into check
#   Currently King cannot castle


class ChessPiece:

    def __init__(self, type, color, pos):
        self.type = type
        self.setColor(color)
        self.pos = pos
        self.hasMoved = False
        self.pawnJustMovedForwardTwice = False

    # Decided to set local variables instead of methods so I don't call self.isWhite instead of self.isWhite() by accident
    def setColor(self, color):
        self.color = color
        self.isWhite = False
        self.isBlack = False
        if(self.color == COLOR.WHITE):
            self.isWhite = True
        if(self.color == COLOR.BLACK):
            self.isBlack = True

    def isOpponent(self, other):
        if(self.color != other.color):
            return True
        return False

    def icon(self):
        index = self.type
        if(self.isBlack):
            index += TYPE.K + 1
        return TypeIcons[index]

    def render(self):
        print(self.icon(), end='')

    def isPositionOnFarthestRank(self, _pos):
        if(self.isWhite and self.type == TYPE.P and _pos.rank == 7):
            return True
        if(self.isBlack and self.type == TYPE.P and _pos.rank == 0):
            return True
        return False

    def possibleMovementPositionsOnBoard(self, board):
        retVal = []
        if(self.type == TYPE.P):
            if(self.isWhite):
                direction = 1
            if(self.isBlack):
                direction = -1
            # Move directly ahead
            canPlace = True
            _pos = self.pos.copy()
            _pos.affect(0, 1 * direction)
            if(not board.emptyPathTo(self.pos, _pos)):
                canPlace = False
            _pos.metaData = POSITION_METADATA.MOVEMENT
            if(canPlace):
                retVal.append(_pos)
            # Directly ahead twice on first move
            canPlace = True
            _pos = self.pos.copy()
            _pos.affect(0, 2 * direction)
            if(not board.emptyPathTo(self.pos, _pos)):
                canPlace = False
            if(self.isWhite and self.pos.rank != 1):
                canPlace = False
            if(self.isBlack and self.pos.rank != 6):
                canPlace = False
            _pos.metaData = POSITION_METADATA.MOVEMENT
            if(canPlace):
                retVal.append(_pos)
            # Can likely refactor these two attacks into one
            # Diagonally forward left if occupied by an opponent
            canPlace = False
            occupant = board.firstCollidedPieceWithinRange(self.pos, 1, -1, direction)
            if(occupant and occupant.isOpponent(self)):
                canPlace = True
                _pos = occupant.pos.copy()
                _pos.metaData = POSITION_METADATA.ATTACK
            if(canPlace):
                retVal.append(_pos)
            # Diagonally forward right if occupied by an opponent
            canPlace = False
            occupant = board.firstCollidedPieceWithinRange(self.pos, 1, 1, direction)
            if(occupant and occupant.isOpponent(self)):
                canPlace = True
                _pos = occupant.pos.copy()
                _pos.metaData = POSITION_METADATA.ATTACK
            if(canPlace):
                retVal.append(_pos)
        elif(self.type == TYPE.N):
            positions = []
            positions.append(ChessPosition(self.pos.file - 2, self.pos.rank + 1))
            positions.append(ChessPosition(self.pos.file - 1, self.pos.rank + 2))
            positions.append(ChessPosition(self.pos.file + 2, self.pos.rank + 1))
            positions.append(ChessPosition(self.pos.file + 1, self.pos.rank + 2))
            positions.append(ChessPosition(self.pos.file - 2, self.pos.rank - 1))
            positions.append(ChessPosition(self.pos.file - 1, self.pos.rank - 2))
            positions.append(ChessPosition(self.pos.file + 2, self.pos.rank - 1))
            positions.append(ChessPosition(self.pos.file + 1, self.pos.rank - 2))
            for position in positions:
                if(position.isOnBoard()):
                    occupant = board.pieceAt(position)
                    if(occupant):
                        position.metaData = POSITION_METADATA.ATTACK
                    else:
                        position.metaData = POSITION_METADATA.MOVEMENT
                    shouldAdd = True
                    if(occupant and not occupant.isOpponent(self)):
                        shouldAdd = False
                    if(shouldAdd):
                        retVal.append(position)
        elif(self.type == TYPE.B):
            positions = []
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank + d * 1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank + d * 1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank + d * -1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank + d * -1))
            for position in positions:
                canPlace = True
                if(not board.emptyPathTo(self.pos, position)):
                    canPlace = False
                position.metaData = POSITION_METADATA.MOVEMENT
                if(canPlace):
                    retVal.append(position)
            attackables = []
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, -1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, -1))
            for occupant in attackables:
                if(occupant and occupant.isOpponent(self)):
                    _pos = occupant.pos.copy()
                    _pos.metaData = POSITION_METADATA.ATTACK
                    retVal.append(_pos)
        elif(self.type == TYPE.R):
            positions = []
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file, self.pos.rank + d * -1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file, self.pos.rank + d * 1))
            for position in positions:
                canPlace = True
                if(not board.emptyPathTo(self.pos, position)):
                    canPlace = False
                position.metaData = POSITION_METADATA.MOVEMENT
                if(canPlace):
                    retVal.append(position)
            attackables = []
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 0, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 0, -1))
            for occupant in attackables:
                if(occupant and occupant.isOpponent(self)):
                    _pos = occupant.pos.copy()
                    _pos.metaData = POSITION_METADATA.ATTACK
                    retVal.append(_pos)
        elif(self.type == TYPE.Q):
            positions = []
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank + d * 1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank + d * 1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank + d * -1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank + d * -1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * -1, self.pos.rank))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file + d * 1, self.pos.rank))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file, self.pos.rank + d * -1))
            for d in range(1, 8):positions.append(ChessPosition(self.pos.file, self.pos.rank + d * 1))
            for position in positions:
                canPlace = True
                if(not board.emptyPathTo(self.pos, position)):
                    canPlace = False
                position.metaData = POSITION_METADATA.MOVEMENT
                if(canPlace):
                    retVal.append(position)
            attackables = []
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, -1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, -1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, -1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 0, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 8, 0, -1))
            for occupant in attackables:
                if(occupant and occupant.isOpponent(self)):
                    _pos = occupant.pos.copy()
                    _pos.metaData = POSITION_METADATA.ATTACK
                    retVal.append(_pos)
        elif(self.type == TYPE.K):
            positions = []
            positions.append(ChessPosition(self.pos.file + -1, self.pos.rank + 1))
            positions.append(ChessPosition(self.pos.file + 1, self.pos.rank + 1))
            positions.append(ChessPosition(self.pos.file + -1, self.pos.rank + -1))
            positions.append(ChessPosition(self.pos.file + 1, self.pos.rank + -1))
            positions.append(ChessPosition(self.pos.file + -1, self.pos.rank))
            positions.append(ChessPosition(self.pos.file + 1, self.pos.rank))
            positions.append(ChessPosition(self.pos.file, self.pos.rank + -1))
            positions.append(ChessPosition(self.pos.file, self.pos.rank + 1))
            for position in positions:
                canPlace = True
                if(not board.emptyPathTo(self.pos, position)):
                    canPlace = False
                position.metaData = POSITION_METADATA.MOVEMENT
                if(canPlace):
                    retVal.append(position)
            attackables = []
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, -1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, 1, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, -1, -1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, 1, -1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, -1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, 1, 0))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, 0, 1))
            attackables.append(board.firstCollidedPieceWithinRange(self.pos, 1, 0, -1))
            for occupant in attackables:
                if(occupant and occupant.isOpponent(self)):
                    _pos = occupant.pos.copy()
                    _pos.metaData = POSITION_METADATA.ATTACK
                    retVal.append(_pos)
        return retVal
