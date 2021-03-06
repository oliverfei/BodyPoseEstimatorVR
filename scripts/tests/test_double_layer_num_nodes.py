import sys
sys.path.append("../")

from keras.models import Model
from keras.layers import Input, Dense
from util.parser import Parser
from util.Evaluator import Evaluator
from util.Estimator import Estimator
from numpy import array

import json
import matplotlib.pyplot as plt
import keras.backend as K

def weighted_mean_squared_error(y_true, y_pred):
    difference = y_pred - y_true
    weights = array([20, 20, 20, 20, 1, 1, 1])
    return K.mean(K.square((difference*weights)), axis=-1)

outputFile = open(sys.argv[3],'w')
outputFile.write("Training data: " + sys.argv[1] + "\n")
outputFile.write("Testing data: " + sys.argv[2] + "\n")
outputFile.write("Num nodes 2, Num nodes 1, rot_avg, rot_max,"+"\n")

for num_trial in range(1,4):
    print("Trial " + str(num_trial))
    for num_nodes2 in range(3, 22, 1):
        for num_nodes1 in range(3, num_nodes2,1):
            print(str(num_nodes1) + " node layer...")
            inputLayer = Input(shape=(21,))
            hiddenLayer1 = Dense(num_nodes1)(inputLayer)
            hiddenLayer2 = Dense(num_nodes2)(hiddenLayer1)
            outputLayer = Dense(3)(hiddenLayer2)
            model = Model(inputs=inputLayer, outputs=outputLayer)
            model.compile(optimizer='adam',
                        loss='mean_squared_error',
                        metrics=['accuracy'])

            p = Parser()
            dataFileTrain = sys.argv[1]
            dataFileTest = sys.argv[2]

            inputDataTrain = array(p.Parse(dataFileTrain))
            print(inputDataTrain.shape)
            outputDataTrain = array(p.ParseSpineRotation(dataFileTrain))
            print(outputDataTrain.shape)
            history = model.fit(inputDataTrain, outputDataTrain, 32, 1000)

            inputDataTest = array(p.Parse(dataFileTest))
            print(inputDataTest.shape)
            outputDataTest = array(p.ParseSpineRotation(dataFileTest))
            print(outputDataTest.shape)
            loss_and_metrics = model.evaluate(inputDataTest, outputDataTest)
            print(loss_and_metrics)

            #test the model
            test = model.predict(inputDataTest, 1)

            #calculate differences
            e = Evaluator()
            result, avg, maxdiff = e.Difference(outputDataTest, test)

            print("max: " + str(maxdiff))
            print("avg: " + str(avg))
            
            avg_rot = sum(avg[:3])
            max_rot = sum(maxdiff[:3])

            print("sum avg_rot: " + str(avg_rot))
            print("sum max_rot: " + str(max_rot))
            outputFile.write(str(num_nodes2) + ",")
            outputFile.write(str(num_nodes1) + ",")
            outputFile.write(str(avg_rot) + ",")
            outputFile.write(str(max_rot) + ",")
            outputFile.write("\n")
outputFile.close()
