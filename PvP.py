import gameNumba as gn
import IA100P
import numba
import numpy as np


def  playout_AI100P_vs_AIRand():
    B = gn.StartingBoard.copy()
    while not gn.Terminated(B):        
        # player 0
        IA100P.PlayPvP(B) # play one time
        
        # player 1
        gn.PlayPvP(B) # play one time
        
    return gn.GetScore(B)
    

if __name__ == '__main__':
    nbSims = 10 * 100
    winCountP0 = 0
    winCountP1 = 0
    for i in range (nbSims):
        if (playout_AI100P_vs_AIRand() == 1):
            winCountP0 += 1
        else: 
            winCountP1 += 1
    print ("Player0:",winCountP0/nbSims*100,"\nPlayer1:",winCountP1/nbSims*100)
