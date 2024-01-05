import copy
import glob

import base as base
import random
import os


# Player template for HIVE --- ALP semestral work
# Vojta Vonasek, 2023


# PUT ALL YOUR IMPLEMENTATION INTO THIS FILE
class Player(base.Board):
    def __init__(self, playerName, myIsUpper, size, myPieces, rivalPieces):  # do not change this line
        base.Board.__init__(self, myIsUpper, size, myPieces, rivalPieces)  # do not change this line
        self.playerName = playerName
        self.algorithmName = "💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩"

    def getAllEmptyCells(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if self.isEmpty(p, q, self.board):
                    result.append([p, q])
        return result

    def getAllNonemptyCells(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if not self.isEmpty(p, q, self.board):
                    result.append([p, q])
        return result

    def canFit(self, actPos: list[int], nePos: list[int]) -> bool:
        # TODO do it lol
        return True

    def isCellViable(self, pos: list[int]):
        if isInBoard(self.size, pos[0], pos[1]) and self.board[pos[0]][pos[1]] == "":
            return True
        return False

    def queenMoves(self, pos: list[int]) -> list[list[int]]:
        moves = []
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for direction in directions:
            newPos = [pos[0] + direction[0], pos[1] + direction[1]]
            if self.isCellViable(newPos) and self.canFit(pos, newPos):
                moves.append(newPos)
        return moves

    def bugMoves(self, pos: list[int]) -> list[list[int]]:
        moves = []
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for direction in directions:
            newPos = [pos[0] + direction[0], pos[1] + direction[1]]
            if isInBoard(self.size, newPos[0], newPos[1]) and self.canFit(pos, newPos):
                moves.append(newPos)
        return moves

    def antMoves(self, position: list[int], prevMoves: list[list[int]]) -> list[list[int]]:
        prevMoves.append(position)
        moves = []
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        for direction in directions:
            newPos = [position[0] + direction[0], position[1] + direction[1]]
            if newPos not in prevMoves:
                directionNeighbors = list(filter(lambda x: isOccupied(x, self.board), getAllNeighbor(newPos)))
                if position in directionNeighbors:
                    directionNeighbors.remove(position)
                if len(directionNeighbors) > 0 and self.isCellViable(newPos) and self.canFit(position, newPos):
                    moves += [newPos]
                    moves += self.antMoves(newPos, prevMoves)
        return moves

    def spiderMoves(self, position: list[int], prevMoves: list[list[int]], distance: int) -> list[list[int]]:
        # TODO
        return [position, []]

    def grasshopperMoves(self, position: list[int]) -> list[list[int]]:
        moves = []
        neighbors = list(filter(lambda x: isOccupied(x, self.board), getAllNeighbor(position)))
        for neighbor in neighbors:
            move = self.grasshopperJump(position, neighbor)
            if move is not []:
                moves.append(move)
        return moves

    def grasshopperJump(self, prevPosition: list[int], position: list[int]) -> list[int]:
        moveBy = [position[0] - prevPosition[0], position[1] - prevPosition[1]]
        nextPosition = [position[0] + moveBy[0], position[1] + moveBy[1]]
        if not isInBoard(boardSize, nextPosition[0], nextPosition[1]):
            return []
        if isOccupied(nextPosition, self.board):
            return self.grasshopperJump(position, nextPosition)
        return nextPosition

    def getAllLegalMoves(self) -> dict[tuple[int], list[list[int]]]:
        player = 0
        if self.myColorIsUpper:
            player = 1
        myFigures = getAllFigures(self.board)[player]
        possibleMoves = dict[tuple, list[list[int]]]()
        for figure in myFigures:
            match self.board[figure[0]][figure[1]][-1].lower():
                case "b":
                    possibleMoves[tuple(figure)] = self.bugMoves(figure)
                case "a":
                    possibleMoves[tuple(figure)] = self.antMoves(figure, [])
                case "g":
                    possibleMoves[tuple(figure)] = self.grasshopperMoves(figure)
                case "s":
                    possibleMoves[tuple(figure)] = self.spiderMoves(figure, [], 0)
                case "q":
                    possibleMoves[tuple(figure)] = self.queenMoves(figure)
        output = dict[tuple, list[list[int]]]()
        for possibleMove in possibleMoves.keys():
            for newPosition in possibleMoves[possibleMove]:
                if newPosition != [] and isOnePiece(self.board, list(possibleMove), newPosition):
                    if not tuple(possibleMove) in output:
                        output[tuple(possibleMove)] = []
                    output[tuple(possibleMove)] += [newPosition]

        return output

    def placePiece(self) -> list:
        insect = random.choice(list(self.myPieces.keys()))

        emptyCells = self.getAllEmptyCells()
        usableCells = []

        for emptyCell in emptyCells:
            neighbors = list(filter(lambda x: isOccupied(x, self.board), getAllNeighbor(emptyCell)))
            if (len(neighbors)) > 0:
                usableCells.append(emptyCell)

        coord = random.choice(usableCells)

        return [insect, None, None, coord[0], coord[1]]

    def movePiece(self):
        moves = self.getAllLegalMoves()
        prevPosition = random.choice(list(moves.keys()))
        newPosition = moves[prevPosition][random.randint(0, len(moves[prevPosition]) - 1)]
        insect = self.board[prevPosition[0]][prevPosition[1]]
        return [insect, prevPosition[0], prevPosition[1], newPosition[0], newPosition[1]]

    def move(self):
        """ return [animal, oldP, oldQ, newP, newQ], or [animal, None, None, newP, newQ] or [] """
        allFigures = getAllFigures(self.board)
        if len(allFigures[0] + allFigures[1]) == 0:
            return ["s", None, None, 3, 6]

        if len(self.getAllEmptyCells()) == 0:
            return []

        if len(self.myPieces) > 0:
            return self.placePiece()

        return self.movePiece()


def moveFigure(board: dict[int, dict[int, str]], prevPos: list[int], newPos: list[int]) -> dict[int, dict[int, str]]:
    newBoard = copy.deepcopy(board)
    newBoard[newPos[0]][newPos[1]] = board[prevPos[0]][prevPos[1]]
    newBoard[prevPos[0]][prevPos[1]] = board[prevPos[0]][prevPos[1]][:-1]
    return newBoard


def isOnePiece(board: dict[int, dict[int, str]], prevPos: list[int], newPos: list[int]) -> bool:
    newBoard = moveFigure(board, prevPos, newPos)
    holder = getAllFigures(newBoard)
    cells = holder[0] + holder[1]

    if len(cells) == 0:
        return True

    somethingChanged = True
    frame = [cells[0]]
    cells.pop(0)
    while somethingChanged:
        somethingChanged = False
        for cell in cells:
            neighbors = list(filter(lambda x: isOccupied(x, newBoard), getAllNeighbor(cell)))
            for neighbor in neighbors:
                if neighbor in frame:
                    frame.append(cell)
                    cells.remove(cell)
                    somethingChanged = True
                    break
            if somethingChanged:
                break
    return sorted(holder[1] + holder[0]) == sorted(frame)


def isInBoard(size: int, p: int, q: int) -> bool:
    return (q >= 0) and (q < size) and (p >= -(q // 2)) and (p < (size - q // 2))


def getAllNeighbor(bug: list[int]) -> list[list[int]]:
    output = []
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

    for dq, dr in directions:
        neighbor_q = bug[0] + dq
        neighbor_r = bug[1] + dr
        if isInBoard(boardSize, neighbor_q, neighbor_r): output.append([neighbor_q, neighbor_r])
    return output


def isOccupied(pos: list[int], board: dict[int, dict[int, str]]) -> bool:
    if board[pos[0]][pos[1]] != "":
        return True
    return False


def getAllFigures(board: dict[int, dict[int, str]]) -> list[list[list[int]]]:
    myFigures = []
    enemyFigures = []
    for p in board:
        for q in board[p]:
            if board[p][q] != "":
                if board[p][q][-1].islower():
                    myFigures.append([p, q])
                elif board[p][q][-1].isupper():
                    enemyFigures.append([p, q])
    return [myFigures, enemyFigures]


def updatePlayers(move, activePlayer, passivePlayer):
    """ write move made by activePlayer player
        this method assumes that all moves are correct, no checking is made
    """
    if len(move) == 0:
        return

    animal = move[0]
    p = move[1]
    q = move[2]
    newp = move[3]
    newq = move[4]
    if p is None and q is None:
        # placing new animal
        activePlayer.myPieces[animal] -= 1
        passivePlayer.rivalPieces = activePlayer.myPieces.copy()
    else:
        # just moving animal
        # delete its old position
        activePlayer.board[p][q] = activePlayer.board[p][q][:-1]
        passivePlayer.board[p][q] = passivePlayer.board[p][q][:-1]

    activePlayer.board[newp][newq] += animal
    passivePlayer.board[newp][newq] += animal


if __name__ == "__main__":
    boardSize = 13
    smallFigures = {"q": 1, "a": 2, "b": 2, "s": 2,
                    "g": 2}  # key is animal, value is how many is available for placing
    bigFigures = {figure.upper(): smallFigures[figure] for figure in smallFigures}  # same, but with upper case

    files = glob.glob("moves/*")
    for f in files:
        os.remove(f)

    P1 = Player("player1", False, 13, smallFigures, bigFigures)
    P2 = Player("player2", True, 13, bigFigures, smallFigures)

    P1.board[0][0] = "g"
    P1.board[0][1] = "A"
    P1.board[1][1] = "G"
    P1.board[0][2] = "a"
    P2.board = copy.deepcopy(P1.board)
    filename = "moves/begin.png"

    P1.saveImage(filename)

    moveIdx = 0
    while True:

        move = P1.move()
        print("P1 returned", move)
        updatePlayers(move, P1, P2)  # update P1 and P2 according to the move
        filename = "moves/move-{:03d}-player1.png".format(moveIdx)
        P1.saveImage(filename)

        move = P2.move()
        print("P2 returned", move)
        updatePlayers(move, P2, P1)  # update P2 and P1 according to the move
        filename = "moves/move-{:03d}-player2.png".format(moveIdx)
        P1.saveImage(filename)

        moveIdx += 1
        P1.myMove = moveIdx
        P2.myMove = moveIdx

        if moveIdx > 4:
            print("End of the test game")
            break
