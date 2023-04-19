import time

from TTTGame import *
from TTTHeader import *


CHESS_TYPE_NUM = 8

LIVE_TARGET = 7         # TARGET
LIVE_TARGET_1 = 6       # LIVE TARGET - 1
SLEEP_TARGET_1 = 5      # SLEEP TARGET - 1
LIVE_TARGET_2 = 4       # LIVE TARGET - 2
SLEEP_TARGET_2 = 3      # SLEEP TARGET - 2
LIVE_TARGET_3 = 2       # LIVE TARGET - 3
SLEEP_TARGET_3 = 1      # SLEEP TARGET - 3

SCORE_MAX = 0x7fffffff
SCORE_MIN = -1 * SCORE_MAX
SCORE_LIVE_TARGET = 10000


class TTTAI():
	def __init__(self, boardSize=20, target=10):
		self.len = boardSize
		self.target = target
		self.fixlen = 2*target-1
		# [horizon, vertical, left diagonal, right diagonal]
		self.board = [[0 for col in range(boardSize)] for row in range(boardSize)]
		self.moves = {}
		self.record = [[[0,0,0,0] for col in range(boardSize)] for row in range(boardSize)]
		self.count = [[0 for col in range(CHESS_TYPE_NUM)] for i in range(2)]
		halflen = boardSize // 2
		self.pos_score = [[(halflen - max(abs(col - halflen), abs(row - halflen))) for col in range(boardSize)] for row in range(boardSize)]

	def reset(self):
		for row in range(self.len):
			for col in range(self.len):
				self.board[row][col] = EMPTY
		self.moves = {}

	def recordReset(self):
		for row in range(self.len):
			for col in range(self.len):
				for i in range(4):
					self.record[row][col][i] = 0

		for i in range(len(self.count)):
			for j in range(len(self.count[0])):
				self.count[i][j] = 0

	def showBoard(self):
		print(' ', end='')
		print('-' * (2*self.len-1))
		for row in range(self.len):
			print('|', end='')
			for col in range(self.len):
			    print(SYMBOLS[self.board[row][col]], end='')
			    print('|', end='')
			print('')
			print(' ', end='')
			print('-' * (2*self.len-1))

	def makeMove(self, col, row, turn):
		self.board[row][col] = turn
		self.moves[(col,row)] = turn
		
	def clearMove(self, col, row):
		self.board[row][col] = EMPTY
		del self.moves[(col,row)]
		
##	def click(self, map, col, row, turn):
##		map.click(col, row, turn)
		
##	def isWin(self, turn):
##		return self.evaluate(turn, True)

	def checkBoard(self):
		dir_offset = [(1, 0), (0, 1), (1, 1), (-1, 1)] # direction from left to right
		not_over = False
		for row in range(self.len):
			for col in range(self.len):
				turn = self.board[row][col]
				if turn != EMPTY:
					for d in dir_offset:
						has_won = True
						new_row, new_col = row, col
						for i in range(1,self.target):
							new_row += d[1]
							new_col += d[0]
							if (new_row < 0 or new_row >= self.len or
							    new_col < 0 or new_col >= self.len or
							    self.board[new_row][new_col] != turn):
								has_won = False
								break
						if has_won:
							return turn
				else:
					not_over = True
		if not_over:
			return None
		else:
			return NO_ONE

	def checkMoves(self):
		dir_offset = [(1, 0), (0, 1), (1, 1), (-1, 1)] # direction from left to right
		for move in self.moves:
			(col, row) = move
			turn = self.moves[move]
			for d in dir_offset:
				has_won = True
				new_col, new_row = col, row
				for i in range(1,self.target):
					new_col += d[0]
					new_row += d[1]
					if ((new_col, new_row) not in self.moves or self.moves[(new_col,new_row)] != turn):
						has_won = False
						break
				if has_won:
					return turn
		if len(self.moves) < self.len*self.len:
			return None
		else:
			return NO_ONE

	# check if has a none EMPTY position in it's radius range
	def hasNeighbor(self, col, row, radius):
		start_col, end_col = (col - radius), (col + radius)
		start_row, end_row = (row - radius), (row + radius)

		for i in range(start_row, end_row+1):
			for j in range(start_col, end_col+1):
				if i >= 0 and i < self.len and j >= 0 and j < self.len:
					if self.board[i][j] != EMPTY:
						return True
		return False

	# get all positions near chess
	def genmove(self, turn):
		moves = []
		if len(self.moves) > 0:
			radius = 1

			for row in range(self.len):
				for col in range(self.len):
					if self.board[row][col] == EMPTY and self.hasNeighbor(col, row, radius):
						score = self.pos_score[row][col]
						moves.append((score, col, row))

			moves.sort(reverse=True)
		else:
			moves.append((0,self.len//2,self.len//2))

		return moves
	
	def minimax(self, turn, depth, alpha = SCORE_MIN, beta = SCORE_MAX):
##		score = self.evaluate(turn)
##		if depth <= 0 or abs(score) >= SCORE_LIVE_TARGET:
##			return score
		
##		win_turn = self.checkBoard()
		win_turn = self.checkMoves()
		if win_turn:
			if win_turn == turn:                    # turn win
				return SCORE_LIVE_TARGET
			elif win_turn == NO_ONE:                # Draw
				return 0
			else:                                   # op_turn win
				return -SCORE_LIVE_TARGET

		if depth <= 0:
			return self.evaluate(turn)

		moves = self.genmove(turn)
		bestmove = None
		self.alpha += len(moves)
		
		# if there are no moves, just return the score, a tie game
		if len(moves) == 0:
			return 0

		for _, col, row in moves:
##			self.board[row][col] = turn
			self.makeMove(col, row, turn)
			
			if turn == PLAYER_ONE:
				op_turn = PLAYER_TWO
			else:
				op_turn = PLAYER_ONE

			score = - self.minimax(op_turn, depth - 1, -beta, -alpha)

##			self.board[row][col] = EMPTY
			self.clearMove(col, row)

			self.belta += 1

			# alpha/beta pruning
			if score > alpha:
				alpha = score
				bestmove = (col, row)
				if alpha >= beta:
					break

		if depth == self.maxdepth: # and bestmove:
			self.bestmove = bestmove
				
		return alpha

	def search(self, turn, depth = 4):
		self.maxdepth = depth
		self.bestmove = None
		score = self.minimax(turn, depth)
		return score, self.bestmove
		
	def findBestMove(self, turn):
		starttime = time.time()
		self.alpha = 0
		self.belta = 0
		score, bestmove = self.search(turn, AI_SEARCH_DEPTH)
		endtime = time.time()
		if bestmove:
			print('time[%.2f] (%d, %d), score[%d] alpha[%d] belta[%d]' %
			      ((endtime-starttime), bestmove[0] , bestmove[1], score, self.alpha, self.belta))
		return bestmove

	# calculate score, FIXME: May Be Improved
	def getScore(self, mine_count, opponent_count):
		mscore, oscore = 0, 0
		if mine_count[LIVE_TARGET] > 0:
			return (SCORE_LIVE_TARGET, 0)
		if opponent_count[LIVE_TARGET] > 0:
			return (0, SCORE_LIVE_TARGET)
				
		if mine_count[SLEEP_TARGET_1] >= 2:
			mine_count[LIVE_TARGET_1] += 1
		if opponent_count[SLEEP_TARGET_1] >= 2:
			opponent_count[LIVE_TARGET_1] += 1
				
		if mine_count[LIVE_TARGET_1] > 0:
			return (9050, 0)
		if mine_count[SLEEP_TARGET_1] > 0:
			return (9040, 0)
			
		if opponent_count[LIVE_TARGET_1] > 0:
			return (0, 9030)
		if opponent_count[SLEEP_TARGET_1] > 0 and opponent_count[LIVE_TARGET_2] > 0:
			return (0, 9020)
			
		if mine_count[LIVE_TARGET_2] > 0 and opponent_count[SLEEP_TARGET_1] == 0:
			return (9010, 0)
			
		if (opponent_count[LIVE_TARGET_2] > 1 and mine_count[LIVE_TARGET_2] == 0 and mine_count[SLEEP_TARGET_2] == 0):
			return (0, 9000)

		if opponent_count[SLEEP_TARGET_1] > 0:
			oscore += 400

		if mine_count[LIVE_TARGET_2] > 1:
			mscore += 500
		elif mine_count[LIVE_TARGET_2] > 0:
			mscore += 100
			
		if opponent_count[LIVE_TARGET_2] > 1:
			oscore += 2000
		elif opponent_count[LIVE_TARGET_2] > 0:
			oscore += 400

		if mine_count[SLEEP_TARGET_2] > 0:
			mscore += mine_count[SLEEP_TARGET_2] * 10
		if opponent_count[SLEEP_TARGET_2] > 0:
			oscore += opponent_count[SLEEP_TARGET_2] * 10
			
		if mine_count[LIVE_TARGET_3] > 0:
			mscore += mine_count[LIVE_TARGET_3] * 6
		if opponent_count[LIVE_TARGET_3] > 0:
			oscore += opponent_count[LIVE_TARGET_3] * 6
				
		if mine_count[SLEEP_TARGET_3] > 0:
			mscore += mine_count[SLEEP_TARGET_3] * 2
		if opponent_count[SLEEP_TARGET_3] > 0:
			oscore += opponent_count[SLEEP_TARGET_3] * 2
		
		return (mscore, oscore)

	def evaluate(self, turn, checkWin=False):
		self.recordReset()
		
		if turn == PLAYER_ONE:
			mine = PLAYER_ONE
			opponent = PLAYER_TWO
		else:
			mine = PLAYER_TWO
			opponent = PLAYER_ONE
		
		for row in range(self.len):
			for col in range(self.len):
				if self.board[row][col] == mine:
					self.evaluatePoint(col, row, mine, opponent)
				elif self.board[row][col] == opponent:
					self.evaluatePoint(col, row, opponent, mine)
		
		mine_count = self.count[mine-1]
		opponent_count = self.count[opponent-1]
		if checkWin:
			return mine_count[LIVE_TARGET] > 0
		else:	
			mscore, oscore = self.getScore(mine_count, opponent_count)
			return (mscore - oscore)
	
	def evaluatePoint(self, col, row, mine, opponent, count=None):
		dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)] # direction from left to right
		ignore_record = True
		if count is None:
			count = self.count[mine-1]
			ignore_record = False
		for i in range(4):
			if self.record[row][col][i] == 0 or ignore_record:
				self.analysisLine(col, row, i, dir_offset[i], mine, opponent, count)

	
	# line is fixed len 9: XXXXMXXXX
	def getLine(self, col, row, dir_offset, mine, opponent):
		line = [0 for i in range(self.fixlen)]
		
		tmp_col = col + (-self.target * dir_offset[0])
		tmp_row = row + (-self.target * dir_offset[1])
		for i in range(self.fixlen):
			tmp_col += dir_offset[0]
			tmp_row += dir_offset[1]
			if (tmp_col < 0 or tmp_col >= self.len or 
				tmp_row < 0 or tmp_row >= self.len):
				line[i] = opponent # set out of range as opponent chess
			else:
				line[i] = self.board[tmp_row][tmp_col]
						
		return line
		
	def analysisLine(self, col, row, dir_index, dir, mine, opponent, count):
		# record line range[left, right] as analysized
		def setRecord(self, col, row, left, right, dir_index, dir_offset):
			tmp_col = col + (-self.target + left) * dir_offset[0]
			tmp_row = row + (-self.target + left) * dir_offset[1]
			for i in range(left, right+1):
				tmp_col += dir_offset[0]
				tmp_row += dir_offset[1]
				self.record[tmp_row][tmp_col][dir_index] = 1
	
##		empty = EMPTY
		left_idx, right_idx = self.target-1, self.target-1
		
		line = self.getLine(col, row, dir, mine, opponent)

		while right_idx < self.fixlen -1:
			if line[right_idx+1] != mine:
				break
			right_idx += 1
		while left_idx > 0:
			if line[left_idx-1] != mine:
				break
			left_idx -= 1
		
		left_range, right_range = left_idx, right_idx
		while right_range < self.fixlen - 1:
			if line[right_range+1] == opponent:
				break
			right_range += 1
		while left_range > 0:
			if line[left_range-1] == opponent:
				break
			left_range -= 1
		
		chess_range = right_range - left_range + 1
		if chess_range < self.target:
			setRecord(self, col, row, left_range, right_range, dir_index, dir)
			return
		
		setRecord(self, col, row, left_idx, right_idx, dir_index, dir)
		
		m_range = right_idx - left_idx + 1
		
		# M:mine chess, P:opponent chess or out of range, X: EMPTY
		if m_range >= self.target:
			count[LIVE_TARGET] += 1
		
		# Live Four : XMMMMX 
		# Chong Four : XMMMMP, PMMMMX
		if m_range == self.target-1:
			left_empty = right_empty = False
			if line[left_idx-1] == EMPTY:
				left_empty = True			
			if line[right_idx+1] == EMPTY:
				right_empty = True
			if left_empty and right_empty:
				count[LIVE_TARGET_1] += 1
			elif left_empty or right_empty:
				count[SLEEP_TARGET_1] += 1
		
		# Chong Four : MXMMM, MMMXM, the two types can both exist
		# Live Three : XMMMXX, XXMMMX
		# Sleep Three : PMMMX, XMMMP, PXMMMXP
		if m_range == self.target-2:
			left_empty = right_empty = False
			left_four = right_four = False
			if line[left_idx-1] == EMPTY:
				if line[left_idx-2] == mine: # MXMMM
					setRecord(self, col, row, left_idx-2, left_idx-1, dir_index, dir)
					count[SLEEP_TARGET_1] += 1
					left_four = True
				left_empty = True
				
			if line[right_idx+1] == EMPTY:
				if line[right_idx+2] == mine: # MMMXM
					setRecord(self, col, row, right_idx+1, right_idx+2, dir_index, dir)
					count[SLEEP_TARGET_1] += 1
					right_four = True 
				right_empty = True
			
			if left_four or right_four:
				pass
			elif left_empty and right_empty:
				if chess_range > self.target: # XMMMXX, XXMMMX
					count[LIVE_TARGET_2] += 1
				else: # PXMMMXP
					count[SLEEP_TARGET_2] += 1
			elif left_empty or right_empty: # PMMMX, XMMMP
				count[SLEEP_TARGET_2] += 1
		
		# Chong Four: MMXMM, only check right direction
		# Live Three: XMXMMX, XMMXMX the two types can both exist
		# Sleep Three: PMXMMX, XMXMMP, PMMXMX, XMMXMP
		# Live Two: XMMX
		# Sleep Two: PMMX, XMMP
		if m_range == self.target-3:
			left_empty = right_empty = False
			left_three = right_three = False
			if line[left_idx-1] == EMPTY:
				if line[left_idx-2] == mine:
					setRecord(self, col, row, left_idx-2, left_idx-1, dir_index, dir)
					if line[left_idx-3] == EMPTY:
						if line[right_idx+1] == EMPTY: # XMXMMX
							count[LIVE_TARGET_2] += 1
						else: # XMXMMP
							count[SLEEP_TARGET_2] += 1
						left_three = True
					elif line[left_idx-3] == opponent: # PMXMMX
						if line[right_idx+1] == EMPTY:
							count[SLEEP_TARGET_2] += 1
							left_three = True
						
				left_empty = True
				
			if line[right_idx+1] == EMPTY:
				if line[right_idx+2] == mine:
					if line[right_idx+3] == mine:  # MMXMM
						setRecord(self, col, row, right_idx+1, right_idx+2, dir_index, dir)
						count[SLEEP_TARGET_1] += 1
						right_three = True
					elif line[right_idx+3] == EMPTY:
						#setRecord(self, col, row, right_idx+1, right_idx+2, dir_index, dir)
						if left_empty:  # XMMXMX
							count[LIVE_TARGET_2] += 1
						else:  # PMMXMX
							count[SLEEP_TARGET_2] += 1
						right_three = True
					elif left_empty: # XMMXMP
						count[SLEEP_TARGET_2] += 1
						right_three = True
						
				right_empty = True
			
			if left_three or right_three:
				pass
			elif left_empty and right_empty: # XMMX
				count[LIVE_TARGET_3] += 1
			elif left_empty or right_empty: # PMMX, XMMP
				count[SLEEP_TARGET_3] += 1
		
		# Live Two: XMXMX, XMXXMX only check right direction
		# Sleep Two: PMXMX, XMXMP
		if m_range == self.target-4:
			left_empty = right_empty = False
			if line[left_idx-1] == EMPTY:
				if line[left_idx-2] == mine:
					if line[left_idx-3] == EMPTY:
						if line[right_idx+1] == opponent: # XMXMP
							count[SLEEP_TARGET_3] += 1
				left_empty = True

			if line[right_idx+1] == EMPTY:
				if line[right_idx+2] == mine:
					if line[right_idx+3] == EMPTY:
						if left_empty: # XMXMX
							#setRecord(self, col, row, left_idx, right_idx+2, dir_index, dir)
							count[LIVE_TARGET_3] += 1
						else: # PMXMX
							count[SLEEP_TARGET_3] += 1
				elif line[right_idx+2] == EMPTY:
					if line[right_idx+3] == mine and line[right_idx+4] == EMPTY: # XMXXMX
						count[LIVE_TARGET_3] += 1
