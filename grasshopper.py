def boardLoader(path: str) -> list[list[int]]:
    board = open(path, "r").read().split("\n")
    output = []

    for i in board:
        holder = i.split(" ")
        if holder[2] != "0":
            output.append([int(holder[0]), int(holder[1]), int(holder[2])])
    return output


Bboard = open("../python-/HIVE/hw9/stones.txt", "r").read().split("\n")

Ooccupied = boardLoader("../python-/HIVE/hw9/stones.txt")


def isInBounds(x: int, y: int) -> bool:
    minMaxY = [0, int(Bboard[0].split(" ")[1])]
    minMaxX = [0 - y // 2, int(Bboard[0].split(" ")[1]) - y // 2]
    return minMaxX[0] <= x <= minMaxX[1] and minMaxY[0] <= y <= minMaxY[1]


def findJump(position: list[int], occupied: list[list[int]], actPosition: list[int]) -> list[int]:
    moveMatrix = [(actPosition[0] - position[0]) * -1, position[1] - actPosition[1]]
    newPosPosition = [position[0] + moveMatrix[0], position[1] + moveMatrix[1], 1]
    if newPosPosition not in occupied and isInBounds(newPosPosition[0], newPosPosition[1]):
        return newPosPosition
    if newPosPosition in occupied and isInBounds(newPosPosition[0], newPosPosition[1]):
        return findJump(newPosPosition, occupied, position)
    return []


def notBroken(newGrasshopperPosition: list[int], input: list[list[int]]) -> bool:
    newInput = input + [newGrasshopperPosition]
    vertices = dict[int, list[int]]()
    neighbors = dict[int, set[int]]()
    for i in range(len(newInput)):
        vertices[i] = newInput[i]
        neighbors[i] = set()

    for i in vertices:
        for j in vertices:
            if i != j and isNeighbor(vertices[i], vertices[j]):
                neighbors[i].add(j)

    somethingChanged = True
    while somethingChanged:
        somethingChanged = False
        for i in range(len(neighbors)):
            for j in range(len(neighbors)):
                for k in neighbors[j]:
                    if i != j and k in neighbors[i]:
                        neighbors[i] = set(list(neighbors[i]) + list(neighbors[j]))
                        neighbors[j].clear()
                        somethingChanged = True
                        break

    for i in range(len(neighbors)):
        if list(vertices.keys()) == list(set(neighbors[i])):
            return True
    return False


def possibleJumps(occupied: list[list[int]]) -> list[list[int]]:
    output = []
    grasshopper = list(filter(lambda x: x[2] == 2, occupied))[0]
    occupied.remove(grasshopper)
    neighbors = [x for x in occupied if isNeighbor(grasshopper, x)]
    for i in neighbors:
        jump = findJump(i, occupied, grasshopper)
        if len(jump) > 0 and notBroken(jump, occupied):
            output.append(jump)
    return output


def isNeighbor(bug: list[int], stone: list[int]) -> bool:
    if bug[1] - stone[1] == 1:
        if bug[0] == stone[0] or bug[0] + 1 == stone[0]:
            return True
    elif bug[1] - stone[1] == -1:
        if bug[0] == stone[0] or bug[0] - 1 == stone[0]:
            return True
    elif bug[1] - stone[1] == 0:
        if bug[0] - 1 == stone[0] or bug[0] + 1 == stone[0]:
            return True
    return False


print(possibleJumps(Ooccupied))
