#player1 = []
#opponent = []
import numpy as np

class Board:

    def __init__(self):
        self.player = [[0 for column in range(10)] for row in range(10)]
        self.opponent = [[0 for column in range(10)] for row in range(10)]
        self.playerCarrier = 5, "Carrier"
        self.playerBattleship = 4, "Battleship"
        self.playerCruiser = 3, "Cruiser"
        self.playerSubmarine = 3, "Submarine"
        self.playerDestroyer = 2, "Destroyer"
        self.remainingShips = [self.playerCarrier, self.playerBattleship, self.playerCruiser, self.playerSubmarine,
                               self.playerDestroyer]
        self.shipsPlaced = []
        self.opponentsShipsRemaining = 5

    def placeShip(self, xCoord, yCoord, ship, up):
        xCoord -= 1
        yCoord -= 1
        if up == True:
            if yCoord - ship[0] >= 0 and yCoord < 10:
                for i in range(ship[0]):
                    if self.player[yCoord - i][xCoord] == 0:
                        self.player[yCoord - i][xCoord] = ship[1]
                    else:
                        print("Cannot place on top of another ship")
                        return False
            else:
                print("Invalid y coordinate")
                return False
        else:
            if xCoord - ship[0] >= 0 and xCoord < 10:
                for i in range(ship[0]):
                    if self.player[yCoord][xCoord + i] == 0:
                        self.player[yCoord][xCoord + i] = ship[1]
                    else:
                        print("Cannot place on top of another ship")
                        return False

            else:
                print("Invalid x coordinate")
                return False

        if not self.shipsPlaced.__contains__(ship):
            self.shipsPlaced.append(ship)
        return True

    def evaluateShot(self, xCoord, yCoord):
        if self.player[yCoord][xCoord] == 0:
            return "miss"
        else:
            hitShip = None
            for ship in self.remainingShips:
                if ship[1] == self.player[yCoord][xCoord]:
                    ship[0] -= 1
                    hitShip = ship
                    self.player[yCoord][xCoord] = "H"
                    break
            if hitShip == None:
                return "miss"
            if hitShip[0] == 0:
                return "sunk"
            else:
                return "hit"

    def updateOpponentBoard(self, response, x, y):
        reward = 0
        if response == "hit" or response == "miss":
            self.opponent[y][x] = response
            if response == "hit":
                reward = 100
            elif response == "miss":
                reward = -100
        else:
            self.opponent[y][x] = "hit"
            self.opponentsShipsRemaining -= 1
            reward = 1000
        return reward
