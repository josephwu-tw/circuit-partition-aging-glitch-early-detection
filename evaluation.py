import numpy as np
import pandas as pd
import keras
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from config import *
from model_func import generate_X_Y

def run_evaluation(Y_test, y_pred):
    mse  = mean_squared_error(Y_test, y_pred)
    rmse = np.sqrt(mse)
    mae  = mean_absolute_error(Y_test, y_pred)
    r2   = r2_score(Y_test, y_pred)

    print("")
    print("Classification Report")
    print(classification_report(Y_test, (y_pred > 0.5).astype(int)))
    print("")
    print("Model Score")
    print(f"MSE : {mse:.8f}")
    print(f"RMSE: {rmse:.8f}")
    print(f"MAE : {mae:.8f}")
    print(f"R2  : {r2:.8f}")

    test_len = G_LEN - WINDOW_SIZE
    track_len = 10
    threshold = 7

    idx_keep = []

    for grp in range(len(y_pred)//test_len):
        Y_test_g = Y_test[grp*test_len:(grp+1)*test_len]
        y_pred_g = y_pred[grp*test_len:(grp+1)*test_len]
        real_idx = len(Y_test_g)
        pred_idx = len(y_pred_g)

        for j in range(track_len, len(y_pred_g)):
            test_track = Y_test_g[j-10:j]
            pred_track = y_pred_g[j-10:j]

            if sum(test_track) >= threshold:
                real_idx = min(j, real_idx)
            if sum(pred_track) >= threshold:
                pred_idx = min(j, pred_idx)

        idx_keep.append((pred_idx, real_idx))

    # counting rating (- means ahead prediction, + means late prediction)
    total_rating = 0
    best_earlest = test_len
    for i in range(len(idx_keep)):
        pred_idx, real_idx = idx_keep[i]
        curr_rating = pred_idx - real_idx
        total_rating += curr_rating
        best_earlest = min(best_earlest, curr_rating)

    avg_rating = total_rating / len(idx_keep)

    print("")
    print("Model Rating")
    print(f"Total rating: {total_rating}")
    print(f"Avg   rating: {avg_rating}")
    print(f"Best  early : {best_earlest}")
    print("")

# get data and model
if __name__ == "__main__":
    data = generate_X_Y(
        group_num = G_NUM,
        group_len = G_LEN,
        window_size = WINDOW_SIZE
        )
    X_test = data[1]
    Y_test = data[4]

    keras.backend.clear_session()
    model = keras.models.load_model(f"./models/{CIRCUIT_TYPE} partition{PARTITION_TYPE}.keras")

    y_pred = model.predict(X_test)
    y_pred = y_pred[:, 0].round().astype(int)

    run_evaluation(Y_test, y_pred)