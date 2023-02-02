import numpy as np
import game.gameNumba as gn
import math
import random
import time
import numba
from numba import jit


class Node():
    def __init__(self, gameState: np.ndarray, parent=None):
        self.gameState = gameState

        # init parent
        self.parent = parent

        # init the number of node visits
        self.visits = 0

        # init the total score of the node
        self.score = 0

        # init current node's children
        # contains all possible moves for exemple: {00:game, ...}, the in game the move 00 was played
        self.children = {}

        # init is node is a leaf or not
        if gn.Terminated(self.gameState):
            self.isTerminal = True
            # is a leaf
        else:
            self.isTerminal = False

        self.isFullyExpanded = self.isTerminal


class MCTS():
    # MCTS for one move
    def search(self, initialState, explorationC=1):
        # Current node, can be in starting game or a mid game
        self.root = Node(initialState)

        
        T0 = time.time()
        while time.time() - T0 < initialState[-1]*4/56:
            # select & expand
            node = self.select(self.root)

            # simulation
            score = self.rollout(node.gameState, nbSimulation=100)

            # backpropagate
            self.backpropagate(node, score)

        node, idMove = self.getBestMove(self.root, explorationC)
        #print(self.root.visits,'timer:', time.time()-T0,'value:',initialState[-1]*1/56, "moves:",initialState[-1], 'score',gn.GetScore(node.gameState) )

        return idMove

    def select(self, node: Node) -> Node:
        while not node.isTerminal:

            # case where the node is fully expanded
            if node.isFullyExpanded:
                # Favor exploration during selection
                node = self.getBestMove(node, 2)[0]

            # case where the node is not fully expanded
            else:
                return self.expand(node)

        return node

    def expand(self, node: Node) -> Node:
        # generate legal states (moves) for the given node
        states = []
        for i in range(node.gameState[-1]):
            newState = node.gameState.copy()
            gn.Play(newState, node.gameState[i])
            states.append(newState)

        # loop over generated states (moves)
        for idMove in range(len(states)):
            state = states[idMove]
            idMove = node.gameState[idMove]

            # make sure that current state (move) is not present in child nodes
            if str(idMove) not in node.children:
                newNode = Node(gameState=state, parent=node)

                # add child node to parent's node children list (dict)
                node.children[str(idMove)] = newNode

                # case when node is fully expanded
                if len(states) == len(node.children):
                    node.isFullyExpanded = True

                return newNode

        # debugging
        raise ('Should not get here!!!')

    def rollout(self, gameState: np.ndarray, nbSimulation=100) -> float:
        # make random moves for both sides until terminal state of the game is reached 'nbSimulation' times and return a score mean
        scoreMean = self._simulateGame(gameState, nbSimulation)

        return scoreMean

    def _simulateGame(self, gameState: np.ndarray, nbSimulation):
        tmpScore = 0
        for i in range(nbSimulation):
            simulation = gameState.copy()
            gn.Playout(simulation)
            tmpScore += gn.GetScore(simulation)
        return tmpScore/nbSimulation

    def backpropagate(self, node: Node, score: int):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def getBestMove(self, node: Node, explorationConstant) -> Node:
        bestScore = float('-inf')
        bestMoves = []

        for key in node.children.keys():
            childNode: Node = node.children[key]
            idMove = int(key)

            if childNode.gameState[-3] == 0:
                player = 1
            else:
                player = -1
            mean = childNode.score / childNode.visits

            # UCT formula
            moveScore = player * mean + explorationConstant * \
                math.sqrt(math.log(node.visits / childNode.visits))

            # better move has been found
            if moveScore > bestScore:
                bestScore = moveScore
                bestMoves = [(childNode, idMove)]

            # found as good move as already available
            elif abs(moveScore - bestScore) <= 1e-09:
                bestMoves.append((childNode, idMove))

        return random.choice(bestMoves)


def play(B: np.ndarray, C = None):
    if B[-1] != 0:
        mcts = MCTS()
        idMove = mcts.search(B,C)
        gn.Play(B, idMove)
        return idMove


def playout(B: np.ndarray,C = None):
    while not gn.Terminated(B):
        play(B,C)


def playout_debug(B: np.ndarray, verbose=True):
    if verbose:
        gn.Print(B)
    while not gn.Terminated(B):
        T0 = time.time()
        play(B)
        dt = time.time() - T0
        if verbose:
            player = B[-3]
            print("Player: ", player, "time:", dt)
            gn.Print(B)
            print("\n---------------------------------------\n")
