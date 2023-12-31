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


def getAllFigures(board: dict[int, dict[int, str]]) -> list[list[list[int]]]:
    output = []
    myFigures = []
    enemyFigures = []
    for p in range(len(board)):
        for q in range(len(board[p])):
            if board[p][q] != "":
                if board[p][q].islower():
                    myFigures.append([p, q])
                elif board[p][q].isupper():
                    enemyFigures.append([p, q])
    return output


def isInBoard(size: int, p: int, q: int):
    return (q >= 0) and (q < size) and (p >= -(q // 2)) and (p < (size - q // 2))


def getAllNeighbor(bug: list[int]) -> list[list[int]]:
    output = []
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

    for dq, dr in directions:
        neighbor_q = bug[0] + dq
        neighbor_r = bug[1] + dr
        if isInBoard(boardSize, neighbor_q, neighbor_r): output.append([neighbor_q, neighbor_r])
    return output


def placeFigure() -> list[int]:
    pass


def updatePlayers(move, activePlayer, passivePlayer):
    """ write move made by activePlayer player
        this method assumes that all moves are correct, no checking is made
    """
    if len(move) == 0:
        return

    animal, p, q, newp, newq = move
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


def queenMoves(board: dict[int, dict[int, str]], pos: list[int]) -> list[list[int]]:
    output = []
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

    for dp, dq in directions:
        neighbor_p = pos[0] + dp
        neighbor_q = pos[1] + dq
        if isInBoard(boardSize, neighbor_p, neighbor_q) and board[dq][dq] == "": output.append([neighbor_q, neighbor_q])
    print(output)
    return output


def bugMoves(board: dict[int, dict[int, str]], pos: list[int]) -> list[list[int]]:
    output = []
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

    for dp, dq in directions:
        neighbor_p = pos[0] + dp
        neighbor_q = pos[1] + dq
        if isInBoard(boardSize, neighbor_p, neighbor_q) and board[dq][dq]: output.append([neighbor_q, neighbor_q])
    return output


def antMoves(board: dict[int, dict[int, str]], position: list[int]) -> list[list[int]]:
    pass


def spiderMoves(board: dict[int, dict[int, str]], position: list[int]) -> list[list[int]]:
    pass


def grasshopperMoves(board: dict[int, dict[int, str]], position: list[int]) -> list[list[int]]:
    pass


if __name__ == "__main__":
    boardSize = 13
    smallFigures = {"q": 1, "a": 2, "b": 2, "s": 2, "g": 2}  # key is animal, value is how many is available for placing
    bigFigures = {figure.upper(): smallFigures[figure] for figure in smallFigures}  # same, but with upper case

    P1 = Player("player1", False, 13, smallFigures, bigFigures)
    P2 = Player("player2", True, 13, bigFigures, smallFigures)

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

        if moveIdx > 0:
            print("End of the test game")
            break
