from AIxP import *
import game as gn
import time

if __name__ == '__main__':
################################################################
#           IA100P
#  Version Debug Demo pour affichage et test 
    print ("Test IA100P")
    B = gn.StartingBoard.copy()
    IA100P.PlayoutDebug(B, False)
    print("Score : ", gn.GetScore(B))
    print("")

    print("Test perf Numba")

    T0 = time.time()
    nbSimus = 0
    while time.time()-T0 < 2:
        B = gn.StartingBoard.copy()
        IA100P.Playout(B)
        nbSimus += 1
    print("Nb Sims / second:", nbSimus/2)

    print()
    print("Test perf Numba + parallélisme")

    nbSimus = 10 * 100
    T0 = time.time()
    MeanScores = IA100P.ParrallelPlayout(nbSimus,gn.StartingBoard.copy())
    T1 = time.time()
    dt = T1-T0

    print("Nb Sims / second:", int(nbSimus / dt))
    print ("Fin test IA100P")


################################################################
#           IA1KP
#  Version Debug Demo pour affichage et test 
    # print("Test IA1KP")
    # B = gn.StartingBoard.copy()
    # IA1KP.PlayoutDebug(B, True)
    # print("Score : ", gn.GetScore(B))
    # print("")

    # print("Test perf Numba")

    # T0 = time.time()
    # nbSimus = 0
    # while time.time()-T0 < 2:
    #     B = gn.StartingBoard.copy()
    #     IA1KP.Playout(B)
    #     nbSimus += 1
    # print("Nb Sims / second:", nbSimus/2)

    # print()
    # print("Test perf Numba + parallélisme")

    # nbSimus = 10 * 100 #* 1000
    # T0 = time.time()
    # MeanScores = IA1KP.ParrallelPlayout(nbSimus,gn.StartingBoard.copy())
    # T1 = time.time()
    # dt = T1-T0

    # print("Nb Sims / second:", int(nbSimus / dt))
    # print("fin test AI1KP")