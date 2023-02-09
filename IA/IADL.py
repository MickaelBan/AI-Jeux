import keras
from keras import layers
import numpy as np


def createModel():
    inputs = keras.Input(shape=(3,64))
    x = layers.Reshape((3,64,1))(inputs)
    
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)

    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([x, inputs])
        
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([x, inputs])

    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([x, inputs])

    x = layers.GlobalAveragePooling2D()(x)

    nbAllPossibleMoves = 7*8*2
    outputs = layers.Dense(nbAllPossibleMoves, activation='softmax')(x)

    return keras.Model(inputs, outputs)


def setData(datafile:str):
    data = []
    import os.path as path
    if path.exists(datafile):
        with open(datafile, "r") as file:
            for line in file.readlines():
                line = line.strip().split(';')
                data.append(line)
    else : raise FileNotFoundError(datafile)   
    
    
    x = []
    y = []
    for move in data:
        
        board = [ int(i) for i in move[1].replace('[','').replace(']','').replace(' ','').split(',') ]
        negativeBoard = [ int(i) for i in move[2].replace('[','').replace(']','').replace(' ','').split(',') ]
        playerBoard = [ int(i) for i in move[3].replace('[','').replace(']','').replace(' ','').split(',') ]
        
        x.append((board,negativeBoard,playerBoard)) #input
        y.append(move[0])                         #label
        
    x = np.array(x)
    y = np.array(y)
    
    
    return x,y

