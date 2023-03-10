from IA import *
import game as gn
import time
import numba
import multiprocessing as mp


# @jit(nopython=True, parallel=True)
# def ParrallelPlayout(nb, StartingBoard: np.ndarray):
#     Scores = np.empty(nb)
#     for i in numba.prange(nb):
#         B = StartingBoard.copy()
#         while not gn.Terminated(B):
#             IA100P.play(B)
#             IA1KP.play(B)
#         Scores[i] = gn.GetScore(B)
#     winrate0 = 0
#     winrate1 = 0
#     for score in Scores:
#         if (score == 1):
#             winrate0 += 1
#         elif (score == -1):
#             winrate1 += 1
#     return winrate0*100/nb, winrate1*100/nb

# def task(C,start,end):
#     mcts = MCTS()
#     dt = 0
#     score = 0
#     for sim in range(start,end):
#         Board = gn.CreateNewGame()
#         T0 = time.time()
#         while not gn.Terminated(Board):
#             idmove = mcts.search(Board,C)
#             gn.Play(Board,idmove)
#         dt += time.time() - T0
#         if gn.GetScore(Board) == 1 :
#             score += 1
#     return (dt,score)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    import sys
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))


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
    # print("Test perf Numba + parall??lisme")

    # nbSimus = 10 * 100
    # T0 = time.time()
    # MeanScores = IA100P.ParrallelPlayout(nbSimus,gn.StartingBoard.copy())
    # T1 = time.time()
    # dt = T1-T0

    # print("Nb Sims / second:", int(nbSimus / dt))
    # print ("Fin test IA100P")

    # print("test mcts")

    # Board = gn.CreateNewGame()
    # T0 = time.time()
    # mcts.playout(Board)
    # dt = time.time()-T0
    # print("Score:",gn.GetScore(Board))
    # print("time:",dt)

    # valuesC = np.arange(0.2,2,0.198)
    # nbSimulation = 200
    # tmps = []
    # winrates = []
    # nbProcess = mp.cpu_count()-1
    # print()
    # for i in range (len(valuesC)):
    #     C = valuesC[i]
    #     progress(i,valuesC.size)
    #     chunkSize = nbSimulation // nbProcess
    #     chunks = [(C, chunkSize * i, chunkSize * (i + 1)) for i in range(nbProcess)]
    #     chunks[-1] = (C, chunkSize * (nbProcess - 1), nbSimulation)

    #     with mp.Pool() as pool:
    #         results = pool.starmap(task,chunks)

    #     dts    = [result[0] for result in results]
    #     scores = [result[1] for result in results]
    #     tmps.append(sum(dts)/nbSimulation)
    #     winrates.append(sum(scores)*100/nbSimulation)

    # print(tmps,winrates)

    # import matplotlib.pyplot as plt

    # plt.figure()
    # plt.subplot(211)
    # plt.plot(valuesC,tmps)
    # plt.xlabel("Coefficient d'exploration")
    # plt.ylabel("temps")
    # plt.title("Temps moyen d'une partie mcts vs mcts en fonction de C")

    # plt.subplot(212)
    # plt.plot(valuesC,winrates)
    # plt.xlabel("Coefficient d'exploration")
    # plt.title("winrates moyen d'une partie mcts vs mcts en fonction de C")
    # plt.ylabel("winrate")

    # plt.subplots_adjust(hspace=1)
    # plt.show()

    ######################################
    # training IA
    ###

    from sklearn.model_selection import train_test_split
    from IA.IADL import *

    try:
        x, y = setData("./data_treated.txt")
    except FileExistsError:
        from database_generator import shedulData
        shedulData(mp.cpu_count())  # parallelis?? car trop long
        x, y = setData("./data_treated.txt")

    model = createModel()

    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)  # validation 20%

    print(x_train.shape(), y_train.shape())
    
    #entrainement
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        batch_size=32,
                        epochs=10,
                        validation_data=(x_val, y_val))

    
    # save le mode
    model.save('model.h5') 
    
    # # charge le model
    # loaded_model = keras.models.load_model('model.h5')

    
