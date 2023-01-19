from game import gameNumba as gn
from AIxP import * 
import numba
from numba import jit
import numpy as np
import time

@jit(nopython=True)
def  playout_IA100P_vs_AIRand(B):
    while not gn.Terminated(B):        
        # player 0
        IA100P.play(B) # play one time
        
        # player 1
        gn.PlayPvP(B) # play one time
        
    return gn.GetScore(B)

def  playout_IA1KP_vs_IA100P(B):
    while not gn.Terminated(B):        
        # player 0
        IA1KP.play(B) # play one time
        
        # player 1
        IA100P.play(B) # play one time
    return gn.GetScore(B)    

      
@jit(nopython=True, parallel=True)
def Parrallel_playout_IA100P_vs_AIRand(nb,StartingBoard:np.ndarray):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        Scores[i] = playout_IA100P_vs_AIRand(StartingBoard.copy())
    return Scores

@jit(nopython=True, parallel=True)
def Parrallel_playout_IA1KP_vs_IA100P(nb,StartingBoard:np.ndarray):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        Scores[i] = playout_IA1KP_vs_IA100P(StartingBoard.copy())
    return Scores


if __name__ == '__main__':
    
    
    ##################################################################################
    #           play IA100P vs IARand
    #
    # nbSims = 10 * 100
    # winCountP0 = 0
    # winCountP1 = 0
    # StartingBoard = np.zeros(144,dtype=np.uint8)
    # gn._PossibleMoves(0,StartingBoard)
    # T0 = time.time()
    # for i in range (nbSims):
    #     if (playout_IA100P_vs_AIRand(StartingBoard.copy()) == 1):
    #         winCountP0 += 1
    #     else: 
    #         winCountP1 += 1
    # dt = time.time() - T0
    # print ("IA100P:",winCountP0/nbSims*100,"\IARand:",winCountP1/nbSims*100)
    # print ("time:",dt)

    ######################
    #  Paralle mode
    #
    
    # B = gn.CreateNewGame()
    # winCountP0 = 0
    # winCountP1 = 0
    # T0 = time.time()
    # Scores = ParrallelPlayout(nbSims,B)
    # for i in Scores:
    #     if (i == 1):
    #         winCountP0 += 1
    #     else: 
    #         winCountP1 += 1
    # dt = time.time() - T0
    # print ("IA100P:",winCountP0/nbSims*100,"\nIARand:",winCountP1/nbSims*100)
    # print ("time:",dt)
    # print ("nbsim/s:",int(nbSims/dt))
    
    ##################################################################################
    #           play IA1KP vs IA100P
    #
    nbSims = 10 * 100
    winCountP0 = 0
    winCountP1 = 0
    B = gn.CreateNewGame()
    T0 = time.time()
    for i in range (nbSims):
        if (playout_IA100P_vs_AIRand(B) == 1):
            winCountP0 += 1
        else: 
            winCountP1 += 1
    dt = time.time() - T0
    print ("IA1KP:",winCountP0/nbSims*100,"\IA100P:",winCountP1/nbSims*100)
    print ("time:",dt)

    ######################
    #  Paralle mode
    #
    
    B = gn.CreateNewGame()
    winCountP0 = 0
    winCountP1 = 0
    T0 = time.time()
    Scores = ParrallelPlayout(nbSims,B)
    for i in Scores:
        if (i == 1):
            winCountP0 += 1
        else: 
            winCountP1 += 1
    dt = time.time() - T0
    print ("IA1KP:",winCountP0/nbSims*100,"\nIA100P:",winCountP1/nbSims*100)
    print ("time:",dt)
    print ("nbsim/s:",int(nbSims/dt))