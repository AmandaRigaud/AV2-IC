# -*- coding: utf-8 -*-
"""Atividade2.2 - AV2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1voB7EqdpVktL0P5ydRYvI2ypzEnDRl3F
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Carregar os dados
data = pd.read_csv('all_stocks_5yr.csv')
data.head()

train_open = data.loc[:, ['open']].values
train_open

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0, 1))
train_scaled = scaler.fit_transform(train_open)
train_scaled

x_train = []
y_train = []
timesteps = 50

for i in range(timesteps, 1250):
  x_train.append(train_scaled[i - timesteps: i, 0])
  y_train.append(train_scaled[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

X_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

"""# Modelo RNN"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import SimpleRNN
from keras.layers import Dropout

regressor = Sequential()

#Adding the first RNN layer and some Dropout regularization
regressor.add(SimpleRNN(units = 50, activation='tanh', return_sequences=True, input_shape= (X_train.shape[1],1)))
regressor.add(Dropout(0.2))

#Adding the second RNN layer and some Dropout regularization
regressor.add(SimpleRNN(units = 50, activation='tanh', return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(SimpleRNN(units = 50, activation='tanh', return_sequences=True))
regressor.add(Dropout(0.2))

#Adding the fourth RNN layer and some Dropout regularization
regressor.add(SimpleRNN(units = 50))
regressor.add(Dropout(0.2))

#Adding the output layer
regressor.add(Dense(units = 1))

#Compile the RNN
regressor.compile(optimizer='adam', loss='mean_squared_error', metrics = ["accuracy"])

#Fitting the RNN to the Training set
x=regressor.fit(x_train, y_train, epochs=100, batch_size=32)

"""# Resultados do treinamento"""

x.history["loss"]

"""# Modelo de Predição RNN"""

y_predictions = regressor.predict(x_train)
y_predictions = scaler.inverse_transform(y_predictions)
y_predictions.shape

y_train = np.reshape(y_train, (y_train.shape[0],1))
y_train = scaler.inverse_transform(y_train)
y_train.shape

"""# Testes de Validação"""

length_data = len(data)
split_ratio = 0.7
length_train = round(length_data * split_ratio)
length_validation = length_data - length_train

valid_data = data[length_train:].iloc[:,:2]
valid_data['date'] = pd.to_datetime(valid_data['date'])
valid_data

dataset_validation = valid_data.values
dataset_validation = np.reshape(dataset_validation, (-1,1))
scaled_dataset_validation =  scaler.fit_transform(train_open)
print("Shape of scaled validation dataset :",scaled_dataset_validation.shape)

X_test = []
y_test = []

for i in range(timesteps, length_validation):
    X_test.append(scaled_dataset_validation[i-timesteps:i,0])
    y_test.append(scaled_dataset_validation[i,0])

X_test, y_test = np.array(X_test), np.array(y_test)

X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
y_test = np.reshape(y_test, (-1,1))

print("Shape of X_test after reshape :",X_test.shape)
print("Shape of y_test after reshape :",y_test.shape)

y_pred_of_test = regressor.predict(y_test)
y_pred_of_test = scaler.inverse_transform(y_pred_of_test)
print("Shape of y_pred_of_test :",y_pred_of_test.shape)

"""# Modelo LSTM"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

testX, testy = np.array(x_train), np.array(y_train)
trainX, trainy = np.array(x_train), np.array(y_train)

trainX.shape

trainX = np.reshape(trainX, (trainX.shape[0],1,  trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0],1,  testX.shape[1]))

trainy.shape

testX.shape

model_lstm = Sequential()
model_lstm.add(
    LSTM(64,return_sequences=True,input_shape = (X_train.shape[1],1))) #64 lstm neuron block
model_lstm.add(
    LSTM(64, return_sequences= False))
model_lstm.add(Dense(32))
model_lstm.add(Dense(1))
model_lstm.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["accuracy"])
history2 = model_lstm.fit(X_train, y_train, epochs = 100, batch_size = 10)

"""#Predição"""

y_train = scaler.fit_transform(y_train)

trainPredict = model_lstm.predict(X_train)
testPredict = model_lstm.predict(testX)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainy = scaler.inverse_transform([trainy])
testPredict = scaler.inverse_transform(testPredict)
testy = scaler.inverse_transform([testy])

import math
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainy[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testy[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

"""# GRU

"""

tf.keras.backend.clear_session()
model=Sequential()
model.add(GRU(32,return_sequences=True,input_shape=(10,1)))
model.add(GRU(32,return_sequences=True))
model.add(GRU(32))
model.add(Dropout(0.20))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam',  metrics = ["accuracy"])

model.summary()

X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

print("X_train: ", X_train.shape)
print("X_test: ", X_test.shape)

y_train.shape

history = model.fit(X_train,testX,validation_data=(y_train,testy), epochs=100,batch_size=32,verbose=1)

train_predict=model.predict(X_train)
test_predict=model.predict(X_test)
train_predict.shape, test_predict.shape

train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
original_ytrain = scaler.inverse_transform(y_train.reshape(-1,1))
original_ytest = scaler.inverse_transform(y_test.reshape(-1,1))

"""--------------------------------------------------------------------------------------"""

y_train = scaler.fit_transform(y_train)

model_lstm = Sequential()
model_lstm.add(
    LSTM(64,return_sequences=True,input_shape = (X_train.shape[1],1))) #64 lstm neuron block
model_lstm.add(
    LSTM(64, return_sequences= False))
model_lstm.add(Dense(32))
model_lstm.add(Dense(1))
model_lstm.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["accuracy"])
history2 = model_lstm.fit(X_train, y_train, epochs = 10, batch_size = 10)

data.iloc[-1]

X_input = data.iloc[-timesteps:].values
#X_input = np.reshape(X_input, (-1,1))
#X_input = scaler.fit_transform(X_input)
X_input = np.reshape(X_input, (1,50,1))
print("Shape of X_input :", X_input.shape)
X_input



simple_RNN_prediction = scaler.inverse_transform(regressor.predict(X_train))
LSTM_prediction = scaler.inverse_transform(model_lstm.predict(X_train))
print("Simple RNN, Open price prediction for 3/18/2017      :", simple_RNN_prediction[0,0])
print("LSTM prediction, Open price prediction for 3/18/2017 :", LSTM_prediction[0,0])