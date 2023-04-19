import sys
import time
from TTTAI import *
from TTTGame import *

class Game():
	def __init__(self, caption):
		self.is_play = False
		self.winner = None
		self.player = PLAYER_ONE
		self.AI = TTTAI(BOARDSIZE, TARGET)
		self.TTT = TTTGame(URL, TEAMID, GAMEID, MYTURN, USERID, APIKEY)
	
	def start(self):
		self.is_play = True
		self.AI.reset()
		moves = self.TTT.GetMoves(GAMEID, str(BOARDSIZE*BOARDSIZE))
		print(moves)
		if moves['code'] == 'OK':
			for mv in moves['moves'][::-1]:
				self.checkClick(int(mv['moveX']), int(mv['moveY']))
			if moves['moves'][0]['symbol'] != SYMBOLS[MYTURN]:
				self.player = MYTURN
			else:
				self.player = OPTURN
		else:
			self.player = PLAYER_ONE

	def play(self):
		if self.is_play and not self.isOver():
			if self.player == MYTURN:
				bestmove = self.AI.findBestMove(self.player)
				if bestmove:
					mv = self.TTT.MakeMove(str(bestmove[0])+','+str(bestmove[1]), TEAMID, GAMEID)
					print(mv)
					self.checkClick(bestmove[0], bestmove[1])
				else:
					self.winner = NO_NONE
			else:
				self.checkOPMove()
			
		if self.isOver():
			self.showWinner()

	def checkClick(self, col, row):
		self.AI.makeMove(col, row, self.player)
		self.AI.showBoard()
		win_turn = self.AI.checkMoves()
		if win_turn:
			self.winner = win_turn
		else:	
			if self.player == PLAYER_ONE:
				self.player = PLAYER_TWO
			else:
				self.player = PLAYER_ONE
	
	def checkOPMove(self):
		while True:
			moves = self.TTT.GetMoves(GAMEID, '1')
			print(moves)
			if moves['code'] == 'OK':
				mv = moves['moves'][0]
				if mv['symbol'] != SYMBOLS[MYTURN]:
					self.checkClick(int(mv['moveX']), int(mv['moveY']))
					break
			time.sleep(5)
	
	def isOver(self):
		return self.winner is not None

	def showWinner(self):
		if self.winner == MYTURN:
			str = 'You win!'
		elif self.winner == OPTURN:
			str = 'Opponent win!'
		else:
			str = 'Draw!'
		print(str)
		sys.exit()
	
			
game = Game("Tic Tac Toe: Board Size ({}) and Target ({}) ".format(BOARDSIZE, TARGET))
game.start()
while True:
	game.play()
