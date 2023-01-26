from .IA100P import play as playK
from numba import jit
import numba
import numpy as np
import game as gn

@jit(nopython=True)
def play(B):
    return playK(B,10000)

@jit(nopython=True)
def Playout(B):
    while not gn.Terminated(B):
        play(B)
     
@jit(nopython=True, parallel=True)
def ParrallelPlayout(nb,StartingBoard:np.ndarray):
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
        if verbose:
            player, x, y = gn.DecodeIDmove(idMove)
            print("Playing : ", idMove, " -  Player: ",
                  player, "  X:", x, " Y:", y)
            gn.Print(B)
            print("---------------------------------------")
            
