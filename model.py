import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras import optimizers
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from config import *
from model_func import *
from evaluation import run_evaluation



# Get X,Y
X_train, X_test, X_val, Y_train, Y_test, Y_val = generate_X_Y(
    group_num = G_NUM,
    group_len = G_LEN,
    window_size = WINDOW_SIZE
    )

# built model
keras.backend.clear_session()
lstm_model = Sequential()

lstm_model.add(keras.Input(shape = (X_train.shape[1], X_train.shape[2])))
lstm_model.add(LSTM(units = 32, return_sequences = True))
lstm_model.add(Dropout(0.1))
lstm_model.add(LSTM(units = 16))
lstm_model.add(Dense(units = 1, activation = 'sigmoid'))

lstm_model.compile(optimizer = optimizers.Adam(learning_rate = 0.0001),
                   loss = "binary_crossentropy",
                   metrics = ['accuracy'])

print("")
lstm_model.summary()
print("")

# training
history = lstm_model.fit(X_train, Y_train,
                         validation_data = (X_val, Y_val),
                         verbose = 1,
                         epochs = 10,
                         batch_size = 64,
                         shuffle = True)
print("")

# plot train history
plt.figure(figsize = (8,8))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title(f'Train History - LSTM, {CIRCUIT_TYPE} partition{PARTITION_TYPE}')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.legend(['train', 'validation'], loc = 'upper left')
traing_fig = plt.gcf()
plt.show()

save_fig(traing_fig, CIRCUIT_TYPE, PARTITION_TYPE)

# Prediction
print("")
y_pred = lstm_model.predict(X_test)
y_pred = y_pred[:, 0].round().astype(int)

# Model evaluation
while True:
    try:
        run_flag = str(input("Run evaluation? (Y/N): "))
        run_flag = run_flag.upper()
        print("")

        if run_flag == "Y":
          
          print("Evaluating ...")
          print("")
          run_evaluation(Y_test, y_pred)
        else:
          print("Evaluation skipped.")
          print("")
        
        break

    except ValueError:
        print("Invalid input. Please enter an Y or N.")


# save model
save_model(lstm_model, CIRCUIT_TYPE, PARTITION_TYPE)


