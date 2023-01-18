import numpy as np,array
import random
import time
import numba
import gameNumba as gn

@numba.jit(nopython=True)
def playSimu(B:array, idMove:int):
    idMove = B[idMove]
    similation = B.copy()
    gn.Play(similation, idMove)
    return similation


@numba.jit(nopython=True)
def findIndexMaxMean(Scores:array):
    max = Scores[:][0].mean()  
    index = 0
    for i in range (1,3):
        max_ = Scores[:][i].mean() 
        if max < max_ : 
            max = max_
            index = i  
    return index
   

@numba.jit(nopython=True)
def Playout(B:array):
    while not gn.Terminated(B):
        idA = random.randint(0, B[-1]-1)  # select random move
        idB = random.randint(0, B[-1]-1)
        idC = random.randint(0, B[-1]-1)
        nb_simulation = 100
        Scores = np.empty((nb_simulation, 3))
        listId = [idA,idB,idC] 
        for index in range (len(listId)-1) :
            id = listId[index]
            nb_simu = nb_simulation
            while nb_simu > 0:
                simulation = playSimu(B,id)
                Scores[nb_simu-1, index] = gn.GetScore(simulation)
                nb_simu -=1
        index = findIndexMaxMean(Scores)
        idMove =  B[listId[index]]
        gn.Play(B,idMove)
    
def PlayoutDebug(B:array,verbose=False):
    if verbose:
        gn.Print(B)
    while not gn.Terminated(B):
        idA = random.randint(0, B[-1]-1)  # select random move
        idB = random.randint(0, B[-1]-1)
        idC = random.randint(0, B[-1]-1)
        nb_simulation = 100
        Scores = np.empty((nb_simulation, 3))
        listId = [idA,idB,idC] 
        nb_simulation = 100
        for index in range (len(listId)-1) :
            id = listId[index]
            while nb_simulation > 0:
                simulation = playSimu(B,id)
                Scores[nb_simulation-1, index] = gn.GetScore(simulation)
                nb_simulation -=1
        index = findIndexMaxMean(Scores)
        idMove =  B[listId[index]]
        gn.Play(B,idMove)
        if verbose:
            player,x,y = gn.DecodeIDmove(idMove)
            print("Playing : ",idMove, " -  Player: ",player, "  X:",x," Y:",y)
            gn.Print(B)
            print("---------------------------------------")


@numba.jit(nopython=True, parallel=True)
def ParrallelPlayout(nb):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        B = gn.StartingBoard.copy()
        Playout(B)
        Scores[i] = gn.GetScore(B)
    return Scores.mean()



if __name__ == '__main__':
    ################################################################
    #
    #  Version Debug Demo pour affichage et test

    B = gn.StartingBoard.copy()
    PlayoutDebug(B,True)
    print("Score : ",gn.GetScore(B))
    print("")


    ################################################################
    #
    #   utilisation de numba => 100 000 parties par seconde

    print("Test perf Numba")

    T0 = time.time()
    nbSimus = 0
    while time.time()-T0 < 2:
        B = gn.StartingBoard.copy()
        Playout(B)
        nbSimus+=1
    print("Nb Sims / second:",nbSimus/2)

    
    # # ###############################################################
    # # 
    # #   utilisation de numba +  multiprocess => 1 000 000 parties par seconde

    print()
    print("Test perf Numba + parallélisme")

    nbSimus = 10 * 1000 * 1000
    T0 = time.time()
    MeanScores = ParrallelPlayout(nbSimus)
    T1 = time.time()
    dt = T1-T0

    print("Nb Sims / second:", int(nbSimus / dt ))
