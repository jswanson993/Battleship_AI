import Board
import Agent
import numpy as np
import random


class Game:

    def __init__(self, human_opponent=False):
        self.player = [[0 for column in range(10)] for row in range(10)]
        self.opponent = [[0 for column in range(10)] for row in range(10)]
        self.carrier = 5, "Carrier"
        self.battleship = 4, "Battleship"
        self.cruiser = 3, "Cruiser"
        self.submarine = 3, "Submarine"
        self.destroyer = 2, "Destroyer"
        self.remainingShips = [self.carrier, self.battleship, self.cruiser, self.submarine,
                               self.destroyer]
        self.shipsPlaced = []
        self.opponentsShipsRemaining = 5
        self.humanOpponent = human_opponent

    def placeShip(self, xCoord, yCoord, ship, up):
        if up:
            if yCoord - ship[0] >= 0 and yCoord < 10:
                for i in range(ship[0]):
                    if self.opponent[yCoord - i][xCoord] == 0:
                        self.opponent[yCoord - i][xCoord] = ship[1]
                    else:
                        #print("Cannot place on top of another ship")
                        return False
            else:
                #print("Invalid y coordinate")
                return False
        else:
            if xCoord + ship[0] < 10 and xCoord < 10:
                for i in range(ship[0]):
                    if self.opponent[yCoord][xCoord + i] == 0:
                        self.opponent[yCoord][xCoord + i] = ship[1]
                    else:
                        #print("Cannot place on top of another ship")
                        return False

            else:
                #print("Invalid x coordinate")
                return False

        if not self.shipsPlaced.__contains__(ship):
            self.shipsPlaced.append(ship)
        return True

    def placeRandomShips(self):
        #for each type of ship, place it in a valid random location
        for ship in self.remainingShips:
            xrand = np.random.randint(0, 9)
            yrand = np.random.randint(0, 9)
            randBit = random.getrandbits(1)
            randBool = bool(randBit)
            while not self.placeShip(xrand, yrand, ship, randBool):
                xrand = random.randint(0, 9)
                yrand = np.random.randint(0, 9)
                randBit = random.getrandbits(1)
                randBool = bool(randBit)

    def update_ship_status(self, ship):
        lship = list(ship)
        lship[0] -= 1
        ship = tuple(lship)
        hitShip = ship
        self.opponent[y][x] = "H"
        return ship

    def fire(self, x, y):
        if self.opponent[y][x] == 0:
            self.player[y][x] = "M"
            return -100, "miss"
        else:
            hitShip = None
            if self.carrier[1] == self.opponent[y][x]:
                self.carrier = self.update_ship_status(self.carrier)
                hitShip = self.carrier

            elif self.battleship[1] == self.opponent[y][x]:
                self.battleship = self.update_ship_status(self.battleship)
                hitShip = self.battleship

            elif self.cruiser[1] == self.opponent[y][x]:
                self.cruiser = self.update_ship_status(self.cruiser)
                hitShip = self.cruiser

            elif self.submarine[1] == self.opponent[y][x]:
                self.submarine = self.update_ship_status(self.submarine)
                hitShip = self.submarine

            elif self.destroyer[1] == self.opponent[y][x]:
                self.destroyer = self.update_ship_status(self.destroyer)
                hitShip = self.destroyer

            if hitShip is None:
                self.player[y][x] = "M"
                return -100, "miss"
            if hitShip[0] == 0:
                self.player[y][x] = "H"
                self.opponentsShipsRemaining -= 1
                return 10000, "sunk"
            else:
                self.player[y][x] = "H"
                return 100, "hit"


if __name__ == '__main__':
    training = True
    if training:
        agent = Agent.QLearningAgent()
        for i in range(0, 100000):
            game = Game(False)
            game.placeRandomShips()
            turnCount = 0
            while game.opponentsShipsRemaining != 0:
                x, y = agent.takeAction(game.player)
                reward, result = game.fire(x, y)
                agent.updateQValue(game.player, (x, y), reward)
                turnCount += 1
            #print("Finished game", i, "in", turnCount, "turns")
        agent.lr = .1
        agent.exploration = 0
        agent.discount = .8
        turnsTaken = []
        for i in range(0, 1000):
            turnCount = 0
            game = Game(False)
            game.placeRandomShips()
            while game.opponentsShipsRemaining != 0:
                x, y = agent.takeAction(game.player)
                reward, result = game.fire(x, y)
                agent.updateQValue(game.player, (x, y), reward)
                turnCount += 1
            turnsTaken.append(turnCount)
        averageTurns = sum(turnsTaken)/len(turnsTaken)
        print("Training Finished. Average amount of turns:", averageTurns)


