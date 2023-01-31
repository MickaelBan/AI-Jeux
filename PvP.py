from game import gameNumba as gn
from AIxP import * 
import numba
from numba import jit
import numpy as np
import time


@jit(nopython=True)
def  playout_IARand_vs_IARand(B):
    while not gn.Terminated(B):        
        # player 0
        gn.PlayPvP(B) # play one time
        
        # player 1
        gn.PlayPvP(B) # play one time
        
    return gn.GetScore(B)


@jit(nopython=True)
def  playout_IA100P_vs_IARand(B):
    while not gn.Terminated(B):        
        # player 0
        IA100P.play(B) # play one time
        
        # player 1
        gn.PlayPvP(B) # play one time
        
    return gn.GetScore(B)

@jit(nopython=True)
def  playout_IA1KP_vs_IA100P(B):
    while not gn.Terminated(B):        
        # player 0
        IA1KP.play(B) # play one time
        
        # player 1
        IA100P.play(B) # play one time
    return gn.GetScore(B)    

@jit(nopython=True)
def  playout_IA10KP_vs_IA1KP(B):
    while not gn.Terminated(B):        
        # player 0
        IA10KP.play(B) # play one time
        
        # player 1
        IA1KP.play(B) # play one time
    return gn.GetScore(B)   
      
# @jit(nopython=True, parallel=True)
# def Parrallel_playout_IA100P_vs_IARand(nb,StartingBoard:np.ndarray):
#     Scores = np.empty(nb)
#     for i in numba.prange(nb):
#         Scores[i] = playout_IA100P_vs_IARand(StartingBoard.copy())
#     return Scores

# @jit(nopython=True, parallel=True)
# def Parrallel_playout_IA1KP_vs_IA100P(nb,StartingBoard:np.ndarray):
#     Scores = np.empty(nb)
#     for i in numba.prange(nb):
#         Scores[i] = playout_IA1KP_vs_IA100P(StartingBoard.copy())
#     return Scores

@jit(nopython=True, parallel=True)
def Parrallel_playout_IA10KP_vs_IA1KP(nb,StartingBoard:np.ndarray):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        Scores[i] = playout_IA10KP_vs_IA1KP(StartingBoard.copy())
    return Scores


if __name__ == '__main__':
    
    ##################################################################################
    #           play IARand vs IARand
    #
    print("\nIA100P vs IARand")
    nbSims = 10 * 100
    winCountP0 = 0
    winCountP1 = 0
    StartingBoard = gn.CreateNewGame()
    T0 = time.time()
    for i in range (nbSims):
        score = playout_IARand_vs_IARand(StartingBoard.copy())
        if (score == 1):
            winCountP0 += 1
        elif (score == -1): 
            winCountP1 += 1
        elif (score == 0):
            raise Exception("Error in the score")
    dt = time.time() - T0
    print ("IA100P:",winCountP0/nbSims*100,"\nIARand:",winCountP1/nbSims*100)
    print ("time:",dt)
    print ("nbsim/s:",nbSims/dt)
    
    ##################################################################################
    #           play IA100P vs IARand
    #
    print("\nIA100P vs IARand")
    nbSims = 10 * 100
    winCountP0 = 0
    winCountP1 = 0
    StartingBoard = gn.CreateNewGame()
    T0 = time.time()
    for i in range (nbSims):
        score = playout_IA100P_vs_IARand(StartingBoard.copy())
        if (score == 1):
            winCountP0 += 1
        elif (score == -1): 
            winCountP1 += 1
        elif (score == 0):
            raise Exception("Error in the score")
    dt = time.time() - T0
    print ("IA100P:",winCountP0/nbSims*100,"\nIARand:",winCountP1/nbSims*100)
    print ("time:",dt)
    print ("nbsim/s:",nbSims/dt)

    # # #####################
    # #  Paralle mode
    # # 
    
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
    # print ("nbsim/s:",nbSims/dt)
    
    ##################################################################################
    #           play IA1KP vs IA100P
    #
    # print("\nIA1KP vs IA100P")
    # nbSims = 10 * 100
    # winCountP0 = 0
    # winCountP1 = 0
    # StartingBoard = gn.CreateNewGame()
    # T0 = time.time()
    # for i in range (nbSims):
    #     score = playout_IA1KP_vs_IA100P(StartingBoard.copy())
    #     if (score == 1):
    #         winCountP0 += 1
    #     elif (score == -1): 
    #         winCountP1 += 1
    #     elif (score == 0):
    #         raise Exception("Error in the score")
    # dt = time.time() - T0
    # print ("IA1kP:",winCountP0/nbSims*100,"\nIA100P:",winCountP1/nbSims*100)
    # print ("time:",dt)
    # print ("nbsim/s:",nbSims/dt)
    
    ##################################################################################
    #           play IA10KP vs IA1KP
    #
    # print("\nIA10KP vs IA1KP")
    # nbSims = 10 * 100
    # winCountP0 = 0
    # winCountP1 = 0
    # StartingBoard = gn.CreateNewGame()
    # T0 = time.time()
    # for i in range (nbSims):
    #     score = playout_IA10KP_vs_IA1KP(StartingBoard.copy())
    #     if (score == 1):
    #         winCountP0 += 1
    #     elif (score == -1): 
    #         winCountP1 += 1
    #     elif (score == 0):
    #         raise Exception("Error in the score")
    # dt = time.time() - T0
    # print ("IA1kP:",winCountP0/nbSims*100,"\nIA100P:",winCountP1/nbSims*100)
    # print ("time:",dt)
    # print ("nbsim/s:",nbSims/dt)

    