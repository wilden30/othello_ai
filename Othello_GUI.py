import turtle
s = turtle.Screen()
t = turtle.Turtle()
gameBoard = []
playerTurn = 'black'
gameOver = False
import copy
import time

'''
t = turtle.Turtle()
t.penup()
t.pendown()
t.goto(-256,-256)
t.shape('turtle')
t.shapesize(2.5,2.5,2.5)
t.stamp()
t.write('Let\'s play')
'''

def drawSquare(size):
	for i in [*range(0,4)]:
		t.forward(size)
		t.right(90)

def drawBoard(n):
	s.setup(1200,650)
	s.bgcolor('green')
	t.speed(0)
	t.ht()
	t.penup()
	t.goto(-300, 300)
	s.tracer(500,0)
	increment = 600/n
	for i in [*range(0,n)]:
		t.penup()
		t.goto(-300,300-i*increment)
		t.pendown()
		for j in [*range(0,n)]:
			cornerDots(i,j)
			drawSquare(increment)
			t.forward(increment)
	t.penup()
	t.goto(-450,200)
	t.color('black')
	t.write('BLACK SCORE:', align='center',font=('Arial', 35, 'normal'))
	t.penup()
	t.goto(450,200)
	t.color('white')
	t.pendown()
	t.write('WHITE SCORE:', align='center',font=('Arial', 35, 'normal'))

def cornerDots(row, col):
	t.color('black')
	t.shape('circle')
	t.shapesize(.5,.5,1)
	if row == 2 and col == 2:
		t.stamp()
	if row == 2 and col == 6:
		t.stamp()
	if row == 6 and col == 2:
		t.stamp()
	if row == 6 and col == 6:
		t.stamp()
	t.shape('arrow')
	t.shapesize(1,1,1)

def whichRow(y):
	for i in [*range(0,8)]:
		if y<300-i*75 and y>300-(i+1)*75:
			return i+1
	return False

def whichColumn(x):
	#print(x)
	for i in [*range(0,8)]:
		if x>-300+i*75 and x<-300+(i+1)*75:
			return i+1
	return False

def xFromColumn(column):
	return -300+column*75-37.5

def yFromRow(row):
	return 300-row*75+37.5

def stampPlayer(row, column, player):
	t.penup()
	t.goto(xFromColumn(column),yFromRow(row))
	if player == 'black':
		t.color('black')
	elif player == 'white':
		t.color('white')
	t.shape('circle')
	t.shapesize(3.5,3.5,1)
	t.stamp()
	t.shape('arrow')
	t.shapesize(1,1,1)


def updateBoard(board, player, row, col):
	board[row-1][col-1] = player
	#return board

def calculateScore(board, player):
	score = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == player:
				score = score + 1
	return score

def updateScore():
	global gameBoard
	t.penup()
	t.goto(-450,100)
	t.color('green')
	t.shape('circle')
	t.shapesize(4,4,1)
	t.stamp()
	t.shape('arrow')
	t.shapesize(1,1,1)
	t.color('black')
	blackScore = calculateScore(gameBoard, 'black')
	#print(calculateScore(gameBoard, 'black'))
	#print(blackScore)
	t.write(str(blackScore), align='center',font=('Arial', 35, 'normal'))
	t.penup()
	t.goto(450,100)
	t.color('green')
	t.shape('circle')
	t.shapesize(4,4,1)
	t.stamp()
	t.shape('arrow')
	t.shapesize(1,1,1)
	t.color('white')
	t.pendown()
	whiteScore = calculateScore(gameBoard, 'white')
	#print(calculateScore(gameBoard, 'white'))
	#print(whiteScore)
	t.write(str(whiteScore), align='center',font=('Arial', 35, 'normal'))

def oppositePlayer(player):
	if player=='white':
		return 'black'
	if player=='black':
		return'white'

def testDirection(board, player, row, column, verticalChange, horizontalChange):
	if row+verticalChange < 1 or row+verticalChange > 8 or column+horizontalChange > 8 or column+horizontalChange < 1:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-1+verticalChange][column-1+horizontalChange] == oppositePlayer(player):
			return testDirection(board,player,row+verticalChange, column+horizontalChange, verticalChange, horizontalChange)
		elif board[row-1+verticalChange][column-1+horizontalChange] == 0:
			return False
		elif board[row-1+verticalChange][column-1+horizontalChange] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-1+verticalChange][column-1+horizontalChange] == player:
			return True
		elif board[row-1+verticalChange][column-1+horizontalChange] == 0:
			return False
		elif board[row-1+verticalChange][column-1+horizontalChange] == oppositePlayer(player):
			return testDirection(board,player,row+verticalChange, column+horizontalChange, verticalChange, horizontalChange)
	else:
		return False

def validMove(board, player, row, column):
	isValidMove = False
	for directions in [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]:
		if testDirection(board, player, row, column, directions[1], directions[0]) and board[row-1][column-1]==0:
			isValidMove = True
	return isValidMove

def allMoves(board, player):
	possibleMoves = []
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == 0:
				if validMove(board, player, row+1, col+1):
					possibleMoves.append([row+1, col+1])
	return possibleMoves

def lightStamp(row, column):
	t.penup()
	t.goto(xFromColumn(column),yFromRow(row)-30)
	t.color('grey')
	t.pendown()
	t.circle(30)
	t.shape('arrow')
	t.shapesize(1,1,1)

def showProspectiveMoves(board, player):
	for pair in allMoves(board, player):
		lightStamp(pair[0], pair[1])

def eraseProspectiveMoves(board, player):
	for pair in allMoves(board, player):
		t.penup()
		t.goto(xFromColumn(pair[1]),yFromRow(pair[0]))
		t.color('green')
		t.shape('circle')
		t.shapesize(3.5,3.5,1)
		t.stamp()
		t.shape('arrow')
		t.shapesize(1,1,1)

def flipPiecesDirection(board, player, row, column, verticalChange, horizontalChange):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPiecesDirection(board, player, row+verticalChange, column+horizontalChange, verticalChange, horizontalChange)


def nextBoard(board, player, move):
	potentialNextBoard = copy.deepcopy(board)
	row = move[0]
	column = move[1]
	for directions in [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]:
		if testDirection(potentialNextBoard, player, row+directions[1], column+directions[0], directions[1], directions[0]):
			flipPiecesDirection(potentialNextBoard, player, row+directions[1], column+directions[0], directions[1], directions[0])
	#print(potentialNextBoard)
	#print(board)
	potentialNextBoard[move[0]-1][move[1]-1] = player
	return potentialNextBoard

def updateNextBoard(board, player, move):
	global gameBoard
	gameBoard = nextBoard(board, player, move)
	#print('during update' + str(board))
	for row in [*range(1,9)]:
		for column in [*range(1,9)]:
			if not(gameBoard[row-1][column-1]==0):
				if not(board[row-1][column-1]==gameBoard[row-1][column-1]):
					stampPlayer(row, column, gameBoard[row-1][column-1])
	
def endGame():
	global gameBoard
	global gameOver
	print('ending game')
	winner = ''
	t.penup()
	t.goto(0,0)
	t.shapesize(1,1,1)
	t.color('red')
	t.pendown()
	if calculateScore(gameBoard, 'black')>calculateScore(gameBoard, 'white'):
		winner = 'Black'
		t.write(winner + ' won!', align='center',font=('Arial', 80, 'normal'))
	elif calculateScore(gameBoard, 'black')<calculateScore(gameBoard, 'white'):
		winner = 'White'
		t.write(winner + ' won!', align='center',font=('Arial', 80, 'normal'))
	else:
		winner = 'tie'
		t.write('It\'s a tie!', align='center',font=('Arial', 80, 'normal'))
	gameOver = True

def showTurn(player):
	if player == 'white':
		t.penup()
		t.color('green')
		t.shape('square')
		t.shapesize(3,3,1)
		for i in [*range(1,6)]:
			t.goto(-600+50*i,270)
			t.stamp()
		t.penup()
		t.goto(450,250)
		t.pendown()
		t.color('red')
		t.write('WHITE TURN', align='center',font=('Arial', 35, 'normal'))
	if player == 'black':
		t.penup()
		t.color('green')
		t.shape('square')
		t.shapesize(3,3,1)
		for i in [*range(1,6)]:
			t.goto(600-50*i,270)
			t.stamp()
		t.penup()
		t.goto(-450,250)
		t.pendown()
		t.color('red')
		t.write('BLACK TURN', align='center',font=('Arial', 35, 'normal'))

def computeScoreOfBoard(board, player, positionScoreDictionary):
	scoreOfBoard = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == player:
				scoreOfBoard += positionScoreDictionary[tuple([row+1,col+1])]
				#if positionScoreDictionary[tuple([row+1,col+1])] == -20:
	return scoreOfBoard

def findBestMove(board, player):
	highestScore = -10000000
	bestMove = []
	positionScoreDictionary = {}
	#figure out a filled to corner function to assign higher values to regular moves that fill a color to a corner (ie can't be flipped)
	cornerMoves = [[1,1],[1,8],[8,1],[8,8]] #use compute score of board, for each corner add 1000, and then compare to current board
	for move in cornerMoves:
		positionScoreDictionary[tuple(move)] = 30
	aroundCornerMoves = {tuple([1,1]):[[2,1],[2,2],[1,2]], tuple([1,8]):[[2,8],[2,7],[1,7]], tuple([8,1]):[[7,1],[7,2],[8,2]], tuple([8,8]):[[7,7],[7,8],[8,7]]} #maybe define with dictionary, where key is corner, value is list of moves around
	for corner in aroundCornerMoves:
		for aroundCornerMove in aroundCornerMoves[corner]:
			if board[list(corner)[0]-1][list(corner)[1]-1] == player:
				positionScoreDictionary[tuple(aroundCornerMove)] = 2
			else:
				positionScoreDictionary[tuple(aroundCornerMove)] = -40
	beforeAroundCornerMoves = [[3,1],[3,2],[3,3],[2,3],[1,3],[1,6],[2,6],[3,6],[3,7],[3,8],[6,1],[6,2],[6,3],[7,3],[8,3],[6,6],[7,6],[8,6],[6,7],[6,8]]
	for move in beforeAroundCornerMoves:
		positionScoreDictionary[tuple(move)] = 3
	remainingMoves = [[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[4,8],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[5,7],[5,8],[1,4],[2,4],[3,4],[1,5],[2,5],[3,5],[6,4],[7,4],[8,4],[6,5],[7,5],[8,5]]
	for move in remainingMoves:
		positionScoreDictionary[tuple(move)] = 1
	print(positionScoreDictionary)
	for move in allMoves(board, player):
		currentScore = computeScoreOfBoard(nextBoard(board, player, move), player, positionScoreDictionary)
		if currentScore>highestScore:
			print(str(bestMove) + str(highestScore))
			bestMove = move
			highestScore = currentScore
	print(str(bestMove) + str(highestScore))
	return bestMove

def evaluate(board, maximizingPlayer, positionScoreDictionary):
	#white is color w/ aroundcorners value
	'''
	scoreOfBoard = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == maximizingPlayer:
				scoreOfBoard += positionScoreDictionary[tuple([row+1,col+1])]
			elif board[row][col] == oppositePlayer(maximizingPlayer):
				scoreOfBoard -= positionScoreDictionary[tuple([row+1,col+1])]
	return scoreOfBoard
	'''
	coinParity = 0
	maxCoins = 0
	minCoins = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == maximizingPlayer:
				maxCoins += 1
			elif board[row][col] == oppositePlayer(maximizingPlayer):
				minCoins += 1
	coinParity = 100*((maxCoins-minCoins)/(minCoins+maxCoins))
	mobility = 0
	maxPlayerMoves = len(allMoves(board, maximizingPlayer))
	minPlayerMoves = len(allMoves(board, oppositePlayer(maximizingPlayer)))
	if (maxPlayerMoves+minPlayerMoves != 0):
		mobility = 100*(maxPlayerMoves-minPlayerMoves)/(maxPlayerMoves+minPlayerMoves)
	cornersValue = 0
	maxPlayerCorners = 0
	minPlayerCorners = 0
	for corner in [[0,0],[0,7],[7,0],[7,7]]:
		if board[corner[0]][corner[1]] == maximizingPlayer:
			maxPlayerCorners += 1
		elif board[corner[0]][corner[1]] == oppositePlayer(maximizingPlayer):
			minPlayerCorners += 1
	if (maxPlayerCorners + minPlayerCorners != 0):
		cornersValue = 100*(maxPlayerCorners-minPlayerCorners)/(maxPlayerCorners+minPlayerCorners)
	maxStablePieces = 0
	minStablePieces = 0
	stablePiecesValue = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			stableBoolean = False
			if board[row][col] == maximizingPlayer:
				for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
					if isStable(board, [row,col], maximizingPlayer, direction):
						stableBoolean = True
				if stableBoolean:
					maxStablePieces += 1
			elif board[row][col] == oppositePlayer(maximizingPlayer):
				for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
					if isStable(board, [row,col], oppositePlayer(maximizingPlayer), direction):
						stableBoolean = True
				if stableBoolean:
					minStablePieces += 1
	if (maxStablePieces + minStablePieces != 0):
		stablePiecesValue = 100*(maxStablePieces-minStablePieces)/(maxStablePieces+minStablePieces)
	aroundCornersValue = 0
	maxAroundCornerValue = 0
	minAroundCornerValue = 0
	aroundCornerMoves = {tuple([1,1]):[[2,1],[2,2],[1,2]], tuple([1,8]):[[2,8],[2,7],[1,7]], tuple([8,1]):[[7,1],[7,2],[8,2]], tuple([8,8]):[[7,7],[7,8],[8,7]]} #maybe define with dictionary, where key is corner, value is list of moves around
	for corner in aroundCornerMoves:
		for aroundCornerMove in aroundCornerMoves[corner]:
			if board[aroundCornerMove[0]-1][aroundCornerMove[1]-1] == maximizingPlayer:	
				if not (board[list(corner)[0]-1][list(corner)[1]-1] == maximizingPlayer):
					maxAroundCornerValue += 1
			elif board[aroundCornerMove[0]-1][aroundCornerMove[1]-1] == oppositePlayer(maximizingPlayer):	
				if not (board[list(corner)[0]-1][list(corner)[1]-1] == oppositePlayer(maximizingPlayer)):
					minAroundCornerValue += 1
	if (minAroundCornerValue + maxAroundCornerValue != 0):
		aroundCornersValue = 100*(minAroundCornerValue-maxAroundCornerValue)/(minAroundCornerValue+maxAroundCornerValue) 
	return 1*coinParity + 2*mobility + 10*cornersValue + 8*stablePiecesValue + 1*aroundCornersValue #add aroundCornersValue if want

def findScore(board, player):
	scorelist = []
	for item in board:
		for item2 in item:
			if item2 == player:
				scorelist.append(item2)
	score = len(scorelist)
	return score

def isStable(board, piece, player, direction):
	rowchange = direction[0]
	colchange = direction[1]
	if piece[0]<0 or piece[1]<0 or piece[0]>7 or piece[1]>7:
		return True
	elif board[piece[0]][piece[1]] != player: 
		return False
	if board[piece[0]][piece[1]] == player:
		return isStable(board,[piece[0]+rowchange,piece[1]+colchange], player, direction) and isStable(board,[piece[0],piece[1]+colchange], player, direction) and isStable(board,[piece[0]+rowchange,piece[1]], player, direction)

def fancyEvaluate(board, maximizingPlayer):
	coinParity = 0
	maxCoins = 0
	minCoins = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			if board[row][col] == maximizingPlayer:
				maxCoins += 1
			elif board[row][col] == oppositePlayer(maximizingPlayer):
				minCoins += 1
	coinParity = 100*((maxCoins-minCoins)/(minCoins+maxCoins))
	mobility = 0
	maxPlayerMoves = len(allMoves(board, maximizingPlayer))
	minPlayerMoves = len(allMoves(board, oppositePlayer(maximizingPlayer)))
	if (maxPlayerMoves+minPlayerMoves != 0):
		mobility = 100*(maxPlayerMoves-minPlayerMoves)/(maxPlayerMoves+minPlayerMoves)
	cornersValue = 0
	maxPlayerCorners = 0
	minPlayerCorners = 0
	for corner in [[0,0],[0,7],[7,0],[7,7]]:
		if board[corner[0]][corner[1]] == maximizingPlayer:
			maxPlayerCorners += 1
		elif board[corner[0]][corner[1]] == oppositePlayer(maximizingPlayer):
			minPlayerCorners += 1
	if (maxPlayerCorners + minPlayerCorners != 0):
		cornersValue = 100*(maxPlayerCorners-minPlayerCorners)/(maxPlayerCorners+minPlayerCorners)
	maxStablePieces = 0
	minStablePieces = 0
	stablePiecesValue = 0
	for row in [*range(0,len(board))]:
		for col in [*range(0,len(board[0]))]:
			stableBoolean = False
			if board[row][col] == maximizingPlayer:
				for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
					if isStable(board, [row,col], maximizingPlayer, direction):
						stableBoolean = True
				if stableBoolean:
					maxStablePieces += 1
			elif board[row][col] == oppositePlayer(maximizingPlayer):
				for direction in [[1,1],[-1,1],[1,-1],[-1,-1]]:
					if isStable(board, [row,col], oppositePlayer(maximizingPlayer), direction):
						stableBoolean = True
				if stableBoolean:
					minStablePieces += 1
	if (maxStablePieces + minStablePieces != 0):
		stablePiecesValue = 100*(maxStablePieces-minStablePieces)/(maxStablePieces+minStablePieces)
	aroundCornersValue = 0
	maxAroundCornerValue = 0
	minAroundCornerValue = 0
	aroundCornerMoves = {tuple([1,1]):[[2,1],[2,2],[1,2]], tuple([1,8]):[[2,8],[2,7],[1,7]], tuple([8,1]):[[7,1],[7,2],[8,2]], tuple([8,8]):[[7,7],[7,8],[8,7]]} #maybe define with dictionary, where key is corner, value is list of moves around
	for corner in aroundCornerMoves:
		for aroundCornerMove in aroundCornerMoves[corner]:
			if board[aroundCornerMove[0]-1][aroundCornerMove[1]-1] == maximizingPlayer:	
				if not (board[list(corner)[0]-1][list(corner)[1]-1] == maximizingPlayer):
					maxAroundCornerValue += 1
			elif board[aroundCornerMove[0]-1][aroundCornerMove[1]-1] == oppositePlayer(maximizingPlayer):	
				if not (board[list(corner)[0]-1][list(corner)[1]-1] == oppositePlayer(maximizingPlayer)):
					minAroundCornerValue += 1
	if (minAroundCornerValue + maxAroundCornerValue != 0):
		aroundCornersValue = 100*(minAroundCornerValue-maxAroundCornerValue)/(minAroundCornerValue+maxAroundCornerValue) 
	#return 1*coinParity + 2*mobility + 10*cornersValue + 8*stablePiecesValue #add aroundCornersValue if want
	return 1*coinParity + 2*mobility + 10*cornersValue + 8*stablePiecesValue + 1*aroundCornersValue


def highestValue(board, player, positionScoreDictionary, maximizingPlayer):
	highestScore = -1000000
	if len(allMoves(board, player))==0:
		return evaluate(board, maximizingPlayer, positionScoreDictionary)
	for move in allMoves(board, player):
		currentScore = evaluate(nextBoard(board, player, move), maximizingPlayer, positionScoreDictionary)
		if currentScore>highestScore:
			highestScore = currentScore
	return highestScore

def lowestValue(board, player, positionScoreDictionary, maximizingPlayer):
	lowestScore = 1000000
	if len(allMoves(board, player))==0:
		return evaluate(board, maximizingPlayer, positionScoreDictionary)
	for move in allMoves(board, player):
		currentScore = evaluate(nextBoard(board, player, move), maximizingPlayer, positionScoreDictionary)
		if currentScore<lowestScore:
			lowestScore = currentScore
	return lowestScore

def minimax(board, depth, isMaximizingPlayer, player, positionScoreDictionary, maximizingPlayer):
	if len(allMoves(board, player))==0 and len(allMoves(board, oppositePlayer(player)))==0:
		return evaluate(board, maximizingPlayer, positionScoreDictionary)
	if len(allMoves(board, player))==0:
		return minimax(board, depth+1, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, maximizingPlayer)
	if depth == 3:
		if isMaximizingPlayer:
			return highestValue(board, player, positionScoreDictionary, maximizingPlayer)
		else:
			return lowestValue(board, player, positionScoreDictionary, maximizingPlayer)
	else:
		if isMaximizingPlayer:
			highestScore = -1000000
			for move in allMoves(board, player):
				currentScore = minimax(nextBoard(board, player, move), depth+1, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, maximizingPlayer)
				if currentScore>highestScore:
					highestScore = currentScore
			return highestScore
		else:
			lowestScore = 1000000
			for move in allMoves(board, player):
				currentScore = minimax(nextBoard(board, player, move), depth+1, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, maximizingPlayer)
				if currentScore<lowestScore:
					lowestScore = currentScore
			return lowestScore

def minimaxMove(board, player):
	start = time.time()
	positionScoreDictionary = {}
	for row in [*range(1,9)]:
		for col in [*range(1,9)]:
			if [row, col] in [[1,1],[1,8],[8,1],[8,8]]:
				positionScoreDictionary[tuple([row,col])] = 35
			elif [row, col] in [[2,1],[2,2],[1,2],[2,8],[2,7],[1,7],[7,1],[7,2],[8,2],[7,7],[7,8],[8,7]]:
				positionScoreDictionary[tuple([row,col])] = -3
			elif row == 8 or row == 1 or col == 8 or col == 1:
				positionScoreDictionary[tuple([row,col])] = 3
			else:
				positionScoreDictionary[tuple([row,col])] = 1
	highestScore = -10000000
	bestMove = []
	for move in allMoves(board, player):
		currentScore = minimax(nextBoard(board, player, move), 1, False, oppositePlayer(player), positionScoreDictionary, player)
		if currentScore>highestScore:
			highestScore = currentScore
			bestMove = move
	print('traditional time ' + str(time.time()-start))
	return bestMove

def alphaBetaMinimax(board, depth, isMaximizingPlayer, player, positionScoreDictionary, alpha, beta, maxDepth, isFancy):
	#print(time.time())
	if isMaximizingPlayer:
		maximizingPlayer = player
	elif not isMaximizingPlayer:
		maximizingPlayer = oppositePlayer(player)
	if len(allMoves(board, player))==0 and len(allMoves(board, oppositePlayer(player)))==0:
		#print('trouble')
		if isFancy:
			return fancyEvaluate(board, maximizingPlayer)
		else:
			return evaluate(board, maximizingPlayer, positionScoreDictionary)
	elif len(allMoves(board, player))==0 and len(allMoves(board, oppositePlayer(player)))!=0:
		#print('double trouble')
		return alphaBetaMinimax(board, depth, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, alpha, beta, maxDepth, isFancy)
	if depth == maxDepth:
		if isFancy:
			return fancyEvaluate(board, maximizingPlayer)
		else:
			return evaluate(board, maximizingPlayer, positionScoreDictionary)
	else:
		if isMaximizingPlayer:
			highestScore = -1000000
			for move in allMoves(board, player):
				if alpha < beta:
					currentScore = alphaBetaMinimax(nextBoard(board, player, move), depth+1, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, alpha, beta, maxDepth, isFancy)
					if currentScore>highestScore:
						highestScore = currentScore
						alpha = highestScore
			return highestScore
		else:
			lowestScore = 1000000
			for move in allMoves(board, player):
				if beta > alpha:
					currentScore = alphaBetaMinimax(nextBoard(board, player, move), depth+1, not(isMaximizingPlayer), oppositePlayer(player), positionScoreDictionary, alpha, beta, maxDepth, isFancy)
					if currentScore<lowestScore:
						lowestScore = currentScore
						beta = lowestScore
			return lowestScore

def alphaBetaMove(board, player):
	start = time.time()
	positionScoreDictionary = {}
	for row in [*range(1,9)]:
		for col in [*range(1,9)]:
			if [row, col] in [[1,1],[1,8],[8,1],[8,8]]:
				positionScoreDictionary[tuple([row,col])] = 35
			elif [row, col] in [[2,1],[2,2],[1,2],[2,8],[2,7],[1,7],[7,1],[7,2],[8,2],[7,7],[7,8],[8,7]]:
				positionScoreDictionary[tuple([row,col])] = -3
			elif row == 8 or row == 1 or col == 8 or col == 1:
				positionScoreDictionary[tuple([row,col])] = 3
			else:
				positionScoreDictionary[tuple([row,col])] = 1
	highestScore = -10000000
	bestMove = []
	alpha = -100000000
	beta = 1000000
	for move in allMoves(board, player):
		currentScore = alphaBetaMinimax(nextBoard(board, player, move), 1, False, oppositePlayer(player), positionScoreDictionary, alpha, beta, 4, False)
		if currentScore>highestScore:
			highestScore = currentScore
			alpha = highestScore
			bestMove = move
	print('contemporary time ' + str(time.time()-start))
	print(bestMove)
	return bestMove

def fancyAlphaBetaMove(board, player):
	print('I am ' + str(player))
	start = time.time()
	positionScoreDictionary = {}
	'''
	for row in [*range(1,9)]:
		for col in [*range(1,9)]:
			if [row, col] in [[1,1],[1,8],[8,1],[8,8]]:
				positionScoreDictionary[tuple([row,col])] = 35
			elif [row, col] in [[2,1],[2,2],[1,2],[2,8],[2,7],[1,7],[7,1],[7,2],[8,2],[7,7],[7,8],[8,7]]:
				positionScoreDictionary[tuple([row,col])] = -3
			elif row == 8 or row == 1 or col == 8 or col == 1:
				positionScoreDictionary[tuple([row,col])] = 3
			else:
				positionScoreDictionary[tuple([row,col])] = 1
	'''
	highestScore = -10000000
	bestMove = []
	alpha = -100000000
	beta = 1000000
	for move in allMoves(board, player):
		currentScore = alphaBetaMinimax(nextBoard(board, player, move), 1, False, oppositePlayer(player), positionScoreDictionary, alpha, beta, 4, True)
		if currentScore>highestScore:
			highestScore = currentScore
			alpha = highestScore
			bestMove = move
	print('fancy time ' + str(time.time()-start))
	#print(bestMove)
	return bestMove


def enemyMove(board, player):
	#print(board)
	#print(player)
	#call whatever their code is to get a move here
	
	boardCopy = copy.deepcopy(board)
	for row in range(0,8):
		for col in range(0,8):
			if boardCopy[row][col] == 'white':
				boardCopy[row][col] = 2
			elif boardCopy[row][col] == 'black':
				boardCopy[row][col] = 1
	if player == 'white':
		playerFormat = 2
	else:
		playerFormat = 1
	
	
	#move = minimaxH(board, 4, player)
	#move = alphaBetaMove(board, player)
	#print(boardCopy)
	#print(playerFormat)
	#move = maximin(boardCopy,0,3,True,playerFormat)
	#move = minimaxN(boardCopy, 0, 4, float('-inf'), float('inf'),playerFormat,2)
	#move = select_move_alphabeta(boardCopy, playerFormat)
	print('enemy move is' + str(move))
	return [move[0], move[1]]

def playMoveWithOtherAI(Hometurn): #pass in true or false for hometurn)
	#print(move)
	global gameBoard
	global playerTurn
	if Hometurn:
		print('hometurn is ' + playerTurn)
		move = fancyAlphaBetaMove(gameBoard, playerTurn)
	elif not Hometurn:
		move = enemyMove(gameBoard, playerTurn)
	row = move[0]
	column = move[1]
	if validMove(gameBoard, playerTurn, row, column):
		eraseProspectiveMoves(gameBoard, playerTurn)
		updateBoard(gameBoard, playerTurn, row, column)
		stampPlayer(row, column, playerTurn)
		updateNextBoard(gameBoard, playerTurn, [row, column])
		#gameBoard = nextBoard(gameBoard, playerTurn, [row, column])
		#print('after update' + str(gameBoard))
		updateScore()
		playerTurn = oppositePlayer(playerTurn)
		if len(allMoves(gameBoard, playerTurn))==0 and len(allMoves(gameBoard, oppositePlayer(playerTurn)))==0:
			endGame()
		else: 
			if len(allMoves(gameBoard, playerTurn))==0:
				playerTurn = oppositePlayer(playerTurn)
				print('no moves')
				showProspectiveMoves(gameBoard, playerTurn)
				showTurn(playerTurn)
				playMoveWithOtherAI(Hometurn)
			else:
				showProspectiveMoves(gameBoard, playerTurn)
				#print(allMoves(gameBoard, playerTurn))
				showTurn(playerTurn)
				playMoveWithOtherAI(not(Hometurn))

def playMove(move):
	#print(move)
	global gameBoard
	global playerTurn
	row = move[0]
	column = move[1]
	if validMove(gameBoard, playerTurn, row, column):
		eraseProspectiveMoves(gameBoard, playerTurn)
		updateBoard(gameBoard, playerTurn, row, column)
		stampPlayer(row, column, playerTurn)
		updateNextBoard(gameBoard, playerTurn, [row, column])
		#gameBoard = nextBoard(gameBoard, playerTurn, [row, column])
		#print('after update' + str(gameBoard))
		updateScore()
		playerTurn = oppositePlayer(playerTurn)
		if len(allMoves(gameBoard, playerTurn))==0 and len(allMoves(gameBoard, oppositePlayer(playerTurn)))==0:
			endGame()
		else: 
			if len(allMoves(gameBoard, playerTurn))==0:
				playerTurn = oppositePlayer(playerTurn)
				print('no moves')
				showProspectiveMoves(gameBoard, playerTurn)
				showTurn(playerTurn)
				playMove(fancyAlphaBetaMove(gameBoard, playerTurn))
			else:
				showProspectiveMoves(gameBoard, playerTurn)
				#print(allMoves(gameBoard, playerTurn))
				showTurn(playerTurn)
	print(gameBoard)


def clickFunction(xcoord, ycoord):
	global gameBoard
	global playerTurn
	global gameOver
	if gameOver:
		playerTurn = 'black'
		s.resetscreen()
		gameOver = False
		t.reset()
		initialize()
	else:
		go = True
		if whichRow(ycoord) == False or whichColumn(xcoord) == False or len(allMoves(gameBoard, playerTurn))==0 or not(validMove(gameBoard, playerTurn, whichRow(ycoord), whichColumn(xcoord))):
			go = False
		if go:
			playMove([whichRow(ycoord), whichColumn(xcoord)])
			if not(len(allMoves(gameBoard, playerTurn))==0):
				playMove(fancyAlphaBetaMove(gameBoard, playerTurn))

def initialize():
	global gameBoard
	global playerTurn
	gameBoard = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
	drawBoard(8)
	updateBoard(gameBoard,'white',4,4)
	stampPlayer(4,4,'white')
	updateBoard(gameBoard,'black',4,5)
	stampPlayer(4,5,'black')
	updateBoard(gameBoard,'black',5,4)
	stampPlayer(5,4,'black')
	updateBoard(gameBoard,'white',5,5)
	stampPlayer(5,5,'white')
	updateScore()
	showTurn(playerTurn)
	showProspectiveMoves(gameBoard, playerTurn)

#put in pauses after computer puts in moves

#drawBoard(8)
#stampPlayer(1,1,'black')
#stampPlayer(8,8,'black')
'''
drawBoard(8)
print(gameBoard)
print(updatedBoard(gameBoard, 'white', 8, 8))
print(gameBoard)
updateScore()
'''


initialize()
s.onclick(clickFunction)
#playMoveWithOtherAI(True)
s.mainloop()


#old code
'''
def flipPieces12clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces12clock(board, player, row-1, column)

def flipPieces130clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces130clock(board, player, row-1, column+1)

def flipPieces3clock(board, player, row, column):
	if board[row-1][column-1] == Player(player):
		updateBoard(board, player, row, column)
		flipPieces3clock(board, player, row, column+1)

def flipPieces430clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces430clock(board, player, row+1, column+1)

def flipPieces6clock(input_board, player, row, column):
	if input_board[row-1][column-1] == oppositePlayer(player):
		updateBoard(input_board, player, row, column)
		flipPieces6clock(input_board, player, row+1, column)

def flipPieces730clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces730clock(board, player, row+1, column-1)

def flipPieces9clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces9clock(board, player, row, column-1)

def flipPieces1030clock(board, player, row, column):
	if board[row-1][column-1] == oppositePlayer(player):
		updateBoard(board, player, row, column)
		flipPieces1030clock(board, player, row-1, column-1)

def test12clock(board, player, row, column):
	if row <= 1:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-2][column-1] == oppositePlayer(player):
			return test12clock(board,player,row-1, column)
		elif board[row-2][column-1] == 0:
			return False
		elif board[row-2][column-1] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-2][column-1] == player:
			return True
		elif board[row-2][column-1] == 0:
			return False
		elif board[row-2][column-1] == oppositePlayer(player):
			return test12clock(board,player,row-1, column)
	else:
		return False

def test130clock(board, player, row, column):
	if column >= 8 or row <= 1:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-2][column] == oppositePlayer(player):
			return test130clock(board,player,row-1, column+1)
		elif board[row-2][column] == 0:
			return False
		elif board[row-2][column] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-2][column] == player:
			return True
		elif board[row-2][column] == 0:
			return False
		elif board[row-2][column] == oppositePlayer(player):
			return test130clock(board,player,row-1, column+1)
	else:
		return False

def test3clock(board, player, row, column):
	if column >= 8:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-1][column] == oppositePlayer(player):
			return test3clock(board,player,row, column+1)
		elif board[row-1][column] == 0:
			return False
		elif board[row-1][column] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-1][column] == player:
			return True
		elif board[row-1][column] == 0:
			return False
		elif board[row-1][column] == oppositePlayer(player):
			return test3clock(board,player,row, column+1)
	else:
		return False

def test430clock(board, player, row, column):
	if column >= 8 or row >= 8:
		return False
	elif board[row-1][column-1] == 0:
		if board[row][column] == oppositePlayer(player):
			return test430clock(board,player,row+1, column+1)
		elif board[row][column] == 0:
			return False
		elif board[row][column] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row][column] == player:
			return True
		elif board[row][column] == 0:
			return False
		elif board[row][column] == oppositePlayer(player):
			return test430clock(board,player,row+1, column+1)
	else:
		return False

def test6clock(board, player, row, column):
	if row >= 8:
		return False
	elif board[row-1][column-1] == 0:
		if board[row][column-1] == oppositePlayer(player):
			return test6clock(board,player,row+1, column)
		elif board[row][column-1] == 0:
			return False
		elif board[row][column-1] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row][column-1] == player:
			return True
		elif board[row][column-1] == 0:
			return False
		elif board[row][column-1] == oppositePlayer(player):
			return test6clock(board,player,row+1, column)
	else:
		return False

def test730clock(board, player, row, column):
	if column <= 1 or row >= 8:
		return False
	elif board[row-1][column-1] == 0:
		if board[row][column-2] == oppositePlayer(player):
			return test730clock(board,player,row+1, column-1)
		elif board[row][column-2] == 0:
			return False
		elif board[row][column-2] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row][column-2] == player:
			return True
		elif board[row][column-2] == 0:
			return False
		elif board[row][column-2] == oppositePlayer(player):
			return test730clock(board,player,row+1, column-1)
	else:
		return False

def test9clock(board, player, row, column):
	if column <= 1:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-1][column-2] == oppositePlayer(player):
			return test9clock(board,player,row, column-1)
		elif board[row-1][column-2] == 0:
			return False
		elif board[row-1][column-2] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-1][column-2] == player:
			return True
		elif board[row-1][column-2] == 0:
			return False
		elif board[row-1][column-2] == oppositePlayer(player):
			return test9clock(board,player,row, column-1)
	else:
		return False

def test1030clock(board, player, row, column):
	if column <= 1 or row <= 1:
		return False
	elif board[row-1][column-1] == 0:
		if board[row-2][column-2] == oppositePlayer(player):
			return test1030clock(board,player,row-1, column-1)
		elif board[row-2][column-2] == 0:
			return False
		elif board[row-2][column-2] == player:
			return False
	elif board[row-1][column-1] == oppositePlayer(player):
		if board[row-2][column-2] == player:
			return True
		elif board[row-2][column-2] == 0:
			return False
		elif board[row-2][column-2] == oppositePlayer(player):
			return test1030clock(board,player,row-1, column-1)
	else:
		return False
	
def oldCode(): #from next board
	if test12clock(potentialNextBoard, player, row-1, column):
		flipPieces12clock(potentialNextBoard, player, row-1, column)
	if test130clock(potentialNextBoard, player, row-1, column+1):
		flipPieces130clock(potentialNextBoard, player, row-1, column+1)
	if test3clock(potentialNextBoard, player, row, column+1):
		flipPieces3clock(potentialNextBoard, player, row, column+1)
	if test430clock(potentialNextBoard, player, row+1, column+1):
		flipPieces430clock(potentialNextBoard, player, row+1, column+1)
	if test6clock(potentialNextBoard, player, row+1, column):
		flipPieces6clock(potentialNextBoard, player, row+1, column)
	if test730clock(potentialNextBoard, player, row+1, column-1):
		flipPieces730clock(potentialNextBoard, player, row+1, column-1)
	if test9clock(potentialNextBoard, player, row, column-1):
		flipPieces9clock(potentialNextBoard, player, row, column-1)
	if test1030clock(potentialNextBoard, player, row-1, column-1):
		flipPieces1030clock(potentialNextBoard, player, row-1, column-1)
	#from isvalidMove
	if board[row-1][column-1]==0:
		if test12clock(board, player, row, column) or test130clock(board, player, row, column) or test3clock(board, player, row, column) or test430clock(board, player, row, column) or test6clock(board, player, row, column) or test730clock(board, player, row, column) or test9clock(board, player, row, column) or test1030clock(board, player, row, column):
			return True
	else:
		return False
'''

