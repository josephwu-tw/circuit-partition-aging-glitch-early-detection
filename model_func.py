import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from config import read_data_df


def generate_X_Y(group_num, group_len, window_size):
    df = read_data_df()
    raw_X = df.iloc[:,:].values
    raw_Y = df.iloc[:,-1].values

    scaler = MinMaxScaler()
    raw_X = scaler.fit_transform(raw_X)

    X = []
    Y = []

    for i in range(group_num):
        temp_X = raw_X[i*group_len:(i+1)*group_len]
        temp_Y = raw_Y[i*group_len:(i+1)*group_len]
        for j in range(group_len-window_size):
            Y.append(temp_Y[j+window_size])
            X.append(temp_X[j:j+window_size])

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42, shuffle = False)

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    Y_train = np.array(Y_train)
    Y_test = np.array(Y_test)

    X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.2, random_state = 42, shuffle = True)

    X_val = np.array(X_val)
    Y_val = np.array(Y_val)

    return X_train, X_test, X_val, Y_train, Y_test, Y_val

def save_model(model, circuit_type, partition_type):
    try:
        save_flag = str(input("Save model? (Y/N): "))
        save_flag = save_flag.upper()

        if save_flag == "Y":
          print("Saving model ...")
          model.save(f"./models/{circuit_type} partition{partition_type}.keras")
          print("Model saved.")
        else:
          print("Model discard.")

    except ValueError:
        print("Invalid input. Please enter an Y or N.")

def save_fig(fig, circuit_type, partition_type):
    try:
        save_flag = str(input("Save figure? (Y/N): "))
        save_flag = save_flag.upper()

        if save_flag == "Y":
          print("Saving figure ...")
          fig.savefig(f"./figs/Training History_{circuit_type} partition{partition_type}")
          print("Figure saved.")
        else:
          print("Figure discard.")

    except ValueError:
        print("Invalid input. Please enter an Y or N.")