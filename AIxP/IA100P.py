import numpy as np
import game.gameNumba as gn
import numba
from numba import jit


@jit(nopython=True)
def _playSimu(B, idMove: int):
    similation = np.copy(B)
    gn.Play(similation, idMove)  # play the move
    gn.Playout(similation)  # random play untail the end of sim
    return similation


@jit(nopython=True)
def play(B, nbSimulation=100) -> int:
    if (B[-1] != 0):
        nbMoves = B[-1]
        player = B[-3]
        scoresMeans = np.zeros(nbMoves)
        for index in range(nbMoves):
            tmpScore = 0
            index = np.intp(index)
            idMove = B[index]
            for i in range(nbSimulation):
                simulation = _playSimu(B, idMove)
                tmpScore += gn.GetScore(simulation)
            scoresMeans[index] = tmpScore/nbSimulation
        if player == 0:
            idBestMove = np.argmax(scoresMeans)
        else:
            idBestMove = np.argmin(scoresMeans)
        bestMove = B[idBestMove]

        gn.Play(B, bestMove)
        return bestMove


@jit(nopython=True)
def Playout(B):
    while not gn.Terminated(B):
        play(B, 100)


@jit(nopython=True, parallel=True)
def ParrallelPlayout(nb, StartingBoard: np.ndarray):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        B = StartingBoard.copy()
        Playout(B)
        Scores[i] = gn.GetScore(B)
    return Scores.mean()


##################################################################
#
#   for demo only - do not use for computation

def PlayoutDebug(B, verbose=False):
    if verbose:
        gn.Print(B)
    while not gn.Terminated(B):
        idMove = play(B)

        if verbose and idMove:
            player, x, y = gn.DecodeIDmove(idMove)
            print("Playing : ", idMove, " -  Player: ",
                  player, "  X:", x, " Y:", y)
            gn.Print(B)
            print("---------------------------------------")
            print()


