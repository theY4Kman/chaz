from __future__ import print_function

from ChessPiece import *
from ChessMove import *

# Noteworthy optimizations:
#   Possible movement positions for each piece are cached
#      so that they do not have to be recalculated every check
#       allowing simulators to access the position data often
#       without potential slowdowns of the simulator. This mean
#       the cache has to be flushed after every move of a piece
#       otherwise antiquated-cache data might persist leading
#       to incorrect future movement analysis on the board.
#       This means it's important to move pieces ONLY via the
#       processMove() function and no others

# Pawn Movement: Finished
# Knight Movement: Finished
# Bishop Movement: Finished
# Rook Movement: Finished
# Queen Movement: Finished
# King Movement: Unfinished
#   Currently King can move into check
#   Currently King cannot castle
#   Currently player can move if King is is check


class ChessBoard:

    def __init__(self, *args):
        if len(args) == 0:
            self.pieces = []
            self.activeColor = COLOR.WHITE
            self.halfMoves = 0
            self.fullMoves = 1
            self.overlayOn = False
            self.overlayPiece = None
            self.reset()
            self.possibleMovementPositionsCache = {}
        elif len(args) == 1:
            # TODO: Set board to mimic FEN input
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

    def clear(self):
        self.turnOffOverlay()
        self.pieces = []

    def getWinner(self):
        whiteAlive = False
        blackAlive = False
        for piece in self.pieces:
            if(piece.type == TYPE.K):
                if(piece.color == COLOR.WHITE):whiteAlive = True
                if(piece.color == COLOR.BLACK):blackAlive = True
        if(not whiteAlive):return COLOR.BLACK
        if(not blackAlive):return COLOR.WHITE
        return None

    def pieceAt(self, pos):
        for ChessPiece in self.pieces:
            if(ChessPiece.pos.file == pos.file and ChessPiece.pos.rank == pos.rank):
                return ChessPiece

    def setOverlayTo(self, piece):
        self.overlayPiece = piece
        self.overlayOn = True

    def turnOffOverlay(self):
        self.overlayPiece = None
        self.overlayOn = False

    def render(self):
        overlayPositions = []
        if(self.overlayOn):
            overlayPositions = self.possibleMovementPositionsOf(self.overlayPiece)
        print('-' * 10)
        for rank in range(7, -1, -1):
            print('|', end='')
            for file in range(0, 8):
                pos = ChessPosition(file, rank)
                piece = self.pieceAt(pos)
                overlayAlreadyWritten = False
                for _pos in overlayPositions:
                    if(_pos.isEqualTo(pos)):
                        if(_pos.metaData == POSITION_METADATA.MOVEMENT):
                            print("X", end='')
                        elif(_pos.metaData == POSITION_METADATA.ATTACK):
                            print("A", end='')
                        overlayAlreadyWritten = True
                if(not overlayAlreadyWritten):
                    if(piece):
                        piece.render()
                    else:
                        if(rank % 2 == 0 and file % 2 != 0):
                            print(' ', end='')
                        elif(rank % 2 != 0 and file % 2 == 0):
                            print(' ', end='')
                        else:
                            print("\u2592", end='')
            print('|', end='')
            print('')
        print('-' * 10)
        print(self.FENNotation())

    def piecesOfColor(self, color):
        retVal = []
        for piece in self.pieces:
            if(piece.color == color):
                retVal.append(piece)
        if(len(retVal) == 0):
            print("!!!Board no longer has any pieces of active color, crash imminent!!!")
        return retVal

    def emptyPathTo(self, a, b):
        isHorizontal = False
        isVertical = False
        isDiagonal = False
        if(not a.isOnBoard() or not b.isOnBoard()):
            return False
        if(a.rank == b.rank and a.file != b.file):
            isHorizontal = True
        elif(a.file == b.file and a.rank != b.rank):
            isVertical = True
        elif(a.file != b.file and a.rank != b.rank and abs(a.file - b.file) == abs(a.rank - b.rank)):
            isDiagonal = True
        else:
            return False
        if(isHorizontal):
            if(a.file < b.file):
                direction = 1
            else:
                direction = -1
            delta = abs(a.file - b.file) + 1
            for d in range(1, delta):
                obsticle = self.pieceAt(ChessPosition(a.file + d * direction, a.rank))
                if(obsticle):
                    return False
            return True
        elif(isVertical):
            if(a.rank < b.rank):
                direction = 1
            else:
                direction = -1
            delta = abs(a.rank - b.rank) + 1
            for d in range(1, delta):
                obsticle = self.pieceAt(ChessPosition(a.file, a.rank + d * direction))
                if(obsticle):
                    return False
            return True
        elif(isDiagonal):
            if(a.file < b.file):
                xDirection = 1
            else:
                xDirection = -1
            if(a.rank < b.rank):
                yDirection = 1
            else:
                yDirection = -1
            delta = abs(a.file - b.file) + 1
            for d in range(1, delta):
                obsticle = self.pieceAt(ChessPosition(a.file + d * xDirection, a.rank + d * yDirection))
                if(obsticle):
                    return False
            return True

    def firstOccupiedPositionWithinRange(self, pos, totalRange, xDirection, yDirection):
        for d in range(1, totalRange + 1):
            _pos = ChessPosition(pos.file + d * xDirection, pos.rank + d * yDirection)
            if(_pos.isOnBoard()):
                obsticle = self.pieceAt(_pos)
                if(obsticle is not None):
                    return _pos
        return None

    def isAValidMove(self, move):
        assert(move.__class__ == ChessMove)
        piece = self.pieceAt(move.fromPosition)
        if(piece == None):
            print("Wha'chu mean you want to move a piece that doesn't exist?! You cray cray")
            return False
        if(piece.color != self.activeColor):
            print("You mean it's not your turn, and your trying to move anyways? CHEATER!")
            return False
        occupant = self.pieceAt(move.toPosition)
        for pos in self.possibleMovementPositionsOf(piece):
            if(pos.isEqualTo(move.toPosition)):
                if(occupant != None and occupant.isOpponent(piece) and not move.isCaptureMove):
                    print("Trying to move to a board position with an occupant opponent but not capturing it is strictly forbidden")
                    return False
                if(occupant == None and move.isCaptureMove):
                    print("Trying to capture on a board position without an opponent is silly, and strictly forbidden")
                    return False
                if(piece.type == TYPE.P):
                    if(piece.isPositionOnFarthestRank(piece.pos)):
                        print("A pawn was supposed to promote, but didn't. Can't handle the responsibilities?!")
                        return False
                return True
        return False

    def processMove(self, move):
        if(self.isAValidMove(move)):
            piece = self.pieceAt(move.fromPosition)
            if(move.isCaptureMove):
                toCapture = self.pieceAt(move.toPosition)
                self.pieces.remove(toCapture)
            if(move.isPromoteMove):
                piece.type = move.promoteType
            if(move.castleType == CASTLETYPE.K):
                pass
            if(move.castleType == CASTLETYPE.Q):
                pass
            piece.pos = move.toPosition

            if(move.isPawnMove or move.isCaptureMove):
                self.halfMoves = 0
            else:
                self.halfMoves += 1
            if(self.activeColor == COLOR.WHITE):
                self.activeColor = COLOR.BLACK
            else:
                self.fullMoves += 1
                self.activeColor = COLOR.WHITE
            self.possibleMovementPositionsCache.clear()
        else:
            print("Tried to play illigal move:", move.notation())

    def potentialMovementPositionsOf(self, piece):
        retVal = []
        if(piece.type == TYPE.P):
            if(piece.isWhite):direction = 1
            if(piece.isBlack):direction = -1
            retVal.append(ChessPosition(piece.pos.file, piece.pos.rank + direction*1))
            if(piece.isOnStartingPawnPosition()):
                retVal.append(ChessPosition(piece.pos.file, piece.pos.rank + direction*2))
        if(piece.type == TYPE.N):
            retVal.append(ChessPosition(piece.pos.file - 2, piece.pos.rank + 1))
            retVal.append(ChessPosition(piece.pos.file - 1, piece.pos.rank + 2))
            retVal.append(ChessPosition(piece.pos.file + 2, piece.pos.rank + 1))
            retVal.append(ChessPosition(piece.pos.file + 1, piece.pos.rank + 2))
            retVal.append(ChessPosition(piece.pos.file - 2, piece.pos.rank - 1))
            retVal.append(ChessPosition(piece.pos.file - 1, piece.pos.rank - 2))
            retVal.append(ChessPosition(piece.pos.file + 2, piece.pos.rank - 1))
            retVal.append(ChessPosition(piece.pos.file + 1, piece.pos.rank - 2))
        movementRange = 8
        if(piece.type == TYPE.K):
            movementRange = 2
        if(piece.type == TYPE.B or piece.type == TYPE.Q or piece.type == TYPE.K):
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d * -1, piece.pos.rank + d *  1))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d *  1, piece.pos.rank + d *  1))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d * -1, piece.pos.rank + d * -1))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d *  1, piece.pos.rank + d * -1))
        if(piece.type == TYPE.R or piece.type == TYPE.Q or piece.type == TYPE.K):
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d * -1, piece.pos.rank + d *  0))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d *  1, piece.pos.rank + d *  0))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d *  0, piece.pos.rank + d * -1))
            for d in range(1, movementRange):retVal.append(ChessPosition(piece.pos.file + d *  0, piece.pos.rank + d *  1))

        retVal = [x for x in retVal if x is not None and x.isOnBoard()]
        return retVal

    def potentialAttackPositionsOf(self, piece):
        retVal = []
        if(piece.type == TYPE.P):
            if(piece.isWhite):direction = 1
            if(piece.isBlack):direction = -1
            retVal.append(ChessPosition(piece.pos.file - 1, piece.pos.rank + direction))
            retVal.append(ChessPosition(piece.pos.file + 1, piece.pos.rank + direction))
        if(piece.type == TYPE.N):
            retVal += self.potentialMovementPositionsOf(piece)
        movementRange = 8
        if(piece.type == TYPE.K):
            movementRange = 2
        if(piece.type == TYPE.B or piece.type == TYPE.Q or piece.type == TYPE.K):
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange, -1,  1))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange,  1,  1))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange, -1, -1))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange,  1, -1))
        if(piece.type == TYPE.R or piece.type == TYPE.Q or piece.type == TYPE.K):
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange, -1,  0))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange,  1,  0))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange,  0,  1))
            retVal.append(self.firstOccupiedPositionWithinRange(piece.pos, movementRange,  0, -1))
        retVal = [x for x in retVal if x is not None and x.isOnBoard()]
        return retVal

    def possibleMovementPositionsOf(self, piece):
        assert(piece in self.pieces)
        if(self.possibleMovementPositionsCache.get(piece) is not None):
            return self.possibleMovementPositionsCache.get(piece)
        retVal = []
        movementPositions = []
        attackPositions = []
        if(piece.type == TYPE.P or piece.type == TYPE.B or piece.type == TYPE.R or piece.type == TYPE.Q):
            potentialMovements = self.potentialMovementPositionsOf(piece)
            for movement in potentialMovements:
                if(self.emptyPathTo(piece.pos, movement)):
                    movement.metaData = POSITION_METADATA.MOVEMENT
                    movementPositions.append(movement)
            potentialAttacks = self.potentialAttackPositionsOf(piece)
            for attack in potentialAttacks:
                occupant = self.pieceAt(attack)
                if(occupant and occupant.isOpponent(piece)):
                    attack.metaData = POSITION_METADATA.ATTACK
                    attackPositions.append(attack)
        if(piece.type == TYPE.N):
            potentialMovements = self.potentialMovementPositionsOf(piece)
            for movement in potentialMovements:
                movement.metaData = POSITION_METADATA.MOVEMENT
                movementPositions.append(movement)
            potentialAttacks = self.potentialAttackPositionsOf(piece)
            for attack in potentialAttacks:
                occupant = self.pieceAt(attack)
                if(occupant and occupant.isOpponent(piece)):
                    attack.metaData = POSITION_METADATA.ATTACK
                    attackPositions.append(attack)
        if(piece.type == TYPE.K):
            potentialMovements = self.potentialMovementPositionsOf(piece)
            for movement in potentialMovements:
                if(self.emptyPathTo(piece.pos, movement)):
                    #if(self.isPositionSafe(movement, piece.color)):
                    movement.metaData = POSITION_METADATA.MOVEMENT
                    movementPositions.append(movement)
            potentialAttacks = self.potentialAttackPositionsOf(piece)
            for attack in potentialAttacks:
                occupant = self.pieceAt(attack)
                if(occupant and occupant.isOpponent(piece)):
                    #if(self.isPositionSafe(attack, piece.color)):
                    attack.metaData = POSITION_METADATA.ATTACK
                    attackPositions.append(attack)
        finalMovementPositions = []
        for movement in movementPositions:
            canPlace = True
            for attack in attackPositions:
                if(movement.isEqualTo(attack)):canPlace = False
            if(canPlace):
                finalMovementPositions.append(movement)
        retVal = attackPositions + finalMovementPositions
        self.possibleMovementPositionsCache[piece] = retVal
        return retVal

    def isPositionSafe(self, pos, safeColor):
        opponents = []
        if(safeColor == COLOR.WHITE):
            opponents = self.piecesOfColor(COLOR.BLACK)
        elif(safeColor == COLOR.BLACK):
            opponents = self.piecesOfColor(COLOR.WHITE)
        for opponent in opponents:
            opponentPositions = self.possibleMovementPositionsOf(opponent)
            for position in opponentPositions:
                if(position.isEqualTo(pos)):
                    print("position under attack!")
                    return True
        return False

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
                else:
                    emptyCount = emptyCount + 1
            if(emptyCount > 0):
                retVal += str(emptyCount)
            emptyCount = 0
            if(rank != 0):
                retVal += "/"
        retVal += " "
        if(self.activeColor == COLOR.WHITE):
            retVal += "w"
        if(self.activeColor == COLOR.BLACK):
            retVal += "b"
        retVal += " "
        castling = ""
        whiteKing = self.pieceAt(ChessPosition("e1"))
        whiteQueenSideRook = self.pieceAt(ChessPosition("a1"))
        whiteKingSideRook = self.pieceAt(ChessPosition("h1"))
        blackKing = self.pieceAt(ChessPosition("e8"))
        blackQueenSideRook = self.pieceAt(ChessPosition("a8"))
        blackKingSideRook = self.pieceAt(ChessPosition("h8"))
        if((whiteKing is not None and whiteKingSideRook is not None) and (not whiteKing.hasMoved and not whiteKingSideRook.hasMoved)):
            castling += "K"
        if((whiteKing is not None and whiteQueenSideRook is not None) and (not whiteKing.hasMoved and not whiteQueenSideRook.hasMoved)):
            castling += "Q"
        if((blackKing is not None and blackKingSideRook is not None) and (not blackKing.hasMoved and not blackKingSideRook.hasMoved)):
            castling += "k"
        if((blackKing is not None and blackQueenSideRook is not None) and (not blackKing.hasMoved and not blackQueenSideRook.hasMoved)):
            castling += "q"
        if(castling == ""):
            castling += "-"
        retVal += castling
        retVal += " "
        # Oddly enough the En Passant point is the spot 'behind' the moved pawn
        enPassant = ""
        for d in range(0, len(self.pieces)):
            if(self.pieces[d].pawnJustMovedForwardTwice):
                pos = self.pieces[d].pos.copy()
                direction = 1
                if(self.pieces[d].color == COLOR.BLACK):
                    direction = -1
                pos.rank -= direction
                enPassant = pos.toParsableString()
                break
        if(enPassant == ""):
            enPassant = "-"
        retVal += enPassant
        retVal += " "
        retVal += str(self.halfMoves)
        retVal += " "
        retVal += str(self.fullMoves)
        return retVal
