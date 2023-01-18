import numpy as np,array
import random
import time
import gameNumba as gn
import numba
from numba import jit

@jit(nopython=True)
def _playSimu(B:array, id:int):
    idMove = B[id]
    similation = np.copy(B)
    gn.Play(similation, idMove)
    return similation


@jit(nopython=True)
def _findIndexMaxMean(Scores:array):
    max = np.mean(Scores[:][0])
    index = 0
    for i in range (1,3):
        max_ = np.mean(Scores[:][i]) 
        if max < max_ : 
            max = max_
            index = i  
    return index
   

@jit(nopython=True)
def Playout(B:array):
    nbMovesSim = 3
    while not gn.Terminated(B):
        nb_simulation = 100
        Scores = np.empty((nb_simulation, nbMovesSim))  
        idMovesList = [random.randint(0, B[-1]-1) for i in range (nbMovesSim)]       
        for index in range (nbMovesSim) :
            id = idMovesList[index]
            while nb_simulation > 0:
                simulation = _playSimu(B,id)
                Scores[nb_simulation-1, index] = gn.GetScore(simulation)
                nb_simulation -=1
        idBeestMove = idMovesList[_findIndexMaxMean(Scores)]
        idMove =  B[idBeestMove]
        gn.Play(B,idMove)
 

def PlayoutDebug(B:array,verbose=False):
    if verbose:
        gn.Print(B)
    nbMovesSim = 3
    while not gn.Terminated(B):
        nb_simulation = 100
        Scores = np.empty((nb_simulation, nbMovesSim))  
        idMovesList = [random.randint(0, B[-1]-1) for i in range (nbMovesSim)]       
        for index in range (nbMovesSim) :
            id = idMovesList[index]
            while nb_simulation > 0:
                simulation = _playSimu(B,id)
                Scores[nb_simulation-1, index] = gn.GetScore(simulation)
                nb_simulation -=1
        idBeestMove = idMovesList[_findIndexMaxMean(Scores)]
        idMove =  B[idBeestMove]
        gn.Play(B,idMove)
        if verbose:
            player,x,y = gn.DecodeIDmove(idMove)
            print("Playing : ",idMove, " -  Player: ",player, "  X:",x," Y:",y)
            gn.Print(B)
            print("---------------------------------------")


@jit(nopython=True, parallel=True)
def ParrallelPlayout(nb):
    Scores = np.empty(nb)
    StartingBoard  = np.zeros(144,dtype=np.uint8)
    for i in numba.prange(nb):
        B = StartingBoard.copy()
        # Playout(B)
        # Scores[i] = gn.GetScore(B)
        pass
    return Scores.mean()



if __name__ == '__main__':
    ################################################################
    #
    #  Version Debug Demo pour affichage et test

    # B = gn.StartingBoard.copy()
    # PlayoutDebug(B,True)
    # print("Score : ",gn.GetScore(B))
    # print("")

    # print("Test perf Numba")

    # T0 = time.time()
    # nbSimus = 0
    # while time.time()-T0 < 2:
    #     B = gn.StartingBoard.copy()
    #     Playout(B)
    #     nbSimus+=1
    # print("Nb Sims / second:",nbSimus/2)

    print()
    print("Test perf Numba + parallélisme")

    nbSimus = 10 
    T0 = time.time()
    MeanScores = ParrallelPlayout(nbSimus)
    T1 = time.time()
    dt = T1-T0

    print("Nb Sims / second:", int(nbSimus / dt ))
