import base
import base as Base
import copy, random, time, math
from PIL import Image, ImageDraw


# Player template for HIVE --- ALP semestral work
# Vojta Vonasek, 2023


# PUT ALL YOUR IMPLEMENTATION INTO THIS FILE
class Player(Base.Board):
    def __init__(self, playerName, myIsUpper, size, myPieces, rivalPieces):  # do not change this line
        Base.Board.__init__(self, myIsUpper, size, myPieces, rivalPieces)  # do not change this line
        self.playerName = playerName
        self.algorithmName = "UngusBongus"

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

    def isOnePiece(self) -> bool:
        holder = self.getAllFigures()
        cells = holder[0] + holder[1]

        if len(cells) == 0:
            return True

        somethingChanged = True
        frame = [cells[0]]
        cells.pop(0)
        while somethingChanged:
            somethingChanged = False
            for cell in cells:
                neighbors = list(filter(lambda x: isOccupied(x, self.board), getAllNeighbor(cell)))
                for neighbor in neighbors:
                    if neighbor in frame:
                        frame.append(cell)
                        cells.remove(cell)
                        somethingChanged = True
                        break
                if somethingChanged:
                    break
        return sorted(holder[1] + holder[0]) == sorted(frame)

    def canFit(self, actPos: list[int], nePos: list[int]) -> bool:
        # TODO do it lol
        return True

    def queenMoves(self, pos: list[int]) -> list[list[int]]:
        moves = []
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for direction in directions:
            newPos = [pos[0] + direction[0], pos[1] + direction[1]]
            if isInBoard(self.size, newPos[0],
                         newPos[1]) and self.board[newPos[0]][newPos[1]] == "" and self.canFit(pos, newPos):
                moves.append(newPos)
        return moves

    def bugMoves(self, position: list[int]) -> list[list[int]]:
        pass

    def antMoves(self, position: list[int]) -> list[list[int]]:
        moves = []
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

        for direction in directions:
            newPos = [position[0] + direction[0], position[1] + direction[1]]
            directionNeighbors = getAllNeighbor(newPos)
            if list(direction) in directionNeighbors:
                directionNeighbors.remove(list(direction))
            if self.isCellViable(newPos) and self.canFit(position, newPos):
                pass

        return moves

    def isCellViable(self, newPos: list[int]):
        return isInBoard(self.size, newPos[0], newPos[1]) and self.board[newPos[0]][newPos[1]][-1] == ""

    def spiderMoves(self, position: list[int]) -> list[list[int]]:
        pass

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

    def getAllFigures(self) -> list[list[list[int]]]:
        myFigures = []
        enemyFigures = []
        for p in self.board:
            for q in self.board[p]:
                if self.board[p][q] != "":
                    if self.board[p][q][-1].islower():
                        myFigures.append([p, q])
                    elif self.board[p][q][-1].isupper():
                        enemyFigures.append([p, q])
        return [myFigures, enemyFigures]

    def getAllLegalMoves(self) -> list[list[list[int]]]:
        myFigures = self.getAllFigures()[0]
        possibleMoves = []
        for figure in myFigures:
            match self.board[figure[0]][figure[1]][-1]:
                case "b":
                    possibleMoves.append([figure, self.bugMoves(figure)])
                case "a":
                    possibleMoves.append([figure, self.antMoves(figure)])
                case "g":
                    possibleMoves.append([figure, self.grasshopperMoves(figure)])
                case "s":
                    possibleMoves.append([figure, self.spiderMoves(figure)])
                case "q":
                    possibleMoves.append([figure, self.queenMoves(figure)])
        # TODO check if OnePiece
        for i in possibleMoves:
            for j in i:
                if [] in j:
                    possibleMoves.remove(i)
                    break
        print(possibleMoves)
        return possibleMoves

    def move(self):
        """ return [animal, oldP, oldQ, newP, newQ], or [animal, None, None, newP, newQ] or [] """

        # the following code just randomly places (ignoring all the rules) some random figure at the board
        emptyCells = self.getAllEmptyCells()

        if len(emptyCells) == 0:
            return []

        randomCell = emptyCells[random.randint(0, len(emptyCells) - 1)]
        randomP, randomQ = randomCell

        for animal in self.myPieces:
            if self.myPieces[animal] > 0:  # is this animal still available? if so, let's place it
                return [animal, None, None, randomP, randomQ]

        # all animals are places, let's move some randomly (again, while ignoring all rules)
        allFigures = self.getAllNonemptyCells()
        randomCell = allFigures[random.randint(0, len(allFigures) - 1)]
        randomFigureP, randomFigureQ = randomCell
        # determine which animal is at randomFigureP, randomFigureQ
        animal = self.board[randomFigureP][randomFigureQ][-1]  # [-1] means the last letter
        return [animal, randomFigureP, randomFigureQ, randomP, randomQ]


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

    P1 = Player("player1", False, 13, smallFigures, bigFigures)
    P2 = Player("player2", True, 13, bigFigures, smallFigures)

    filename = "moves/begin.png"

    P1.board[3][6] = "q"

    P1.getAllLegalMoves()
    P1.saveImage(filename)

    """moveIdx = 0
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

        if moveIdx > 0:
            print("End of the test game")
            break"""
