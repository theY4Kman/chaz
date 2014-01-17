from __future__ import print_function

from ChessBoard import *
from ChessSimulatorStream import *

class ChessSimulatorManager:
	def __init__(self):
		self.board = ChessBoard()
		self.whiteSimulatorStream = None
		self.blackSimulatorStream = None
		print("SimulatorManager loaded, no simulator streams locked")
	def run(self):
		self.board.render()
	def lockSimulatorStream(self, simulatorStream, color):
		if(color == COLOR.WHITE):
			self.whiteSimulatorStream = simulatorStream
			print("White simulator stream locked")
		else:
			self.blackSimulatorStream = simulatorStream
			print("Black simulator stream locked")
		if(self.bothSimulatorStreamsLocked()):
			print("Both simulator streams are locked, SimulatorManager primed")
	def bothSimulatorStreamsLocked(self):
		if(self.whiteSimulatorStream and self.blackSimulatorStream):return True
		return False
