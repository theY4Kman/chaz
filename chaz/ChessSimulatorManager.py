from ChessBoard import *

class ChessSimulatorManager:
	def __init__(self):
		self.board = ChessBoard()
	def run(self):
		self.board.render()