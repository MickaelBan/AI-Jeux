from IA import *
import game as gn
import time
import numba


@jit(nopython=True, parallel=True)
def ParrallelPlayout(nb, StartingBoard: np.ndarray):
    Scores = np.empty(nb)
    for i in numba.prange(nb):
        B = StartingBoard.copy()
        while not gn.Terminated(B):
            IA100P.play(B)
            IA1KP.play(B)
        Scores[i] = gn.GetScore(B)
    winrate0 = 0
    winrate1 = 0
    for score in Scores:
        if (score == 1):
            winrate0 += 1
        elif (score == -1):
            winrate1 += 1
    return winrate0*100/nb, winrate1*100/nb

@numba.njit
def parallel_code(StartingBoard, nb):
    Scores = np.zeros(nb)
    for i in numba.prange(nb):
        B = StartingBoard.copy()
        mcts.playout(B)
        Scores[i] = gn.GetScore(B)
    return Scores

if __name__ == '__main__':

    # print ("\nTest IA100P")
    # StartingBoard = gn.CreateNewGame()
    # # B = StartingBoard.copy()
    # # IA100P.PlayoutDebug(B, True)
    # # print("Score : ", gn.GetScore(B))
    # # print("")
    # # print("Test perf Numba")

    # nbSimus = 100
    # T0 = time.time()
    # winrate0,winrate1 = ParrallelPlayout(nbSimus,StartingBoard)
    # print("win rate player 0 (IA100P vs IArand):", winrate0)
    # print("win rate player 0 (IA100P vs IArand):", winrate1)
    # print("Time:", time.time()-T0)

    # T0 = time.time()
    # nbSimus = 0
    # while time.time()-T0 < 2:
    #     B = StartingBoard.copy()
    #     IA100P.Plaout(B)
    #     nbSimus += 1
    #     if (gn.GetScore(B)==1):
    #         winCount += 1
    # print("Nb Sims / second:", nbSimus/2)
    # print()
    # print("Test perf Numba + parallélisme")

    # nbSimus = 10 * 100
    # T0 = time.time()
    # MeanScores = IA100P.ParrallelPlayout(nbSimus,gn.StartingBoard.copy())
    # T1 = time.time()
    # dt = T1-T0

    # print("Nb Sims / second:", int(nbSimus / dt))
    # print ("Fin test IA100P")

    print("test mcts")

    Board = gn.CreateNewGame()
    T0 = time.time()
    mcts.playout(Board)
    dt = time.time()-T0
    print("Score:",gn.GetScore(Board))
    print("time:",dt)
    
    valueC = [i for i in np.arange(0.2,2,0.198)]
    
    