import pandas as pd

CIRCUIT_NUM = 9
MAX_NUM = 3
G_LEN = 300
G_NUM = 90
WINDOW_SIZE = 5

CIRCUIT_TYPES = ["c17", "c432"]

while True:
    
    try:
        CIRCUIT_TYPE = str(input("Enter Circuit type: ")).lower()

        if CIRCUIT_TYPE in CIRCUIT_TYPES:
          print(f"Select {CIRCUIT_TYPE}")
     
        else:
          print("Unknown circuit type, loading c17 as default")
          CIRCUIT_TYPE = "c17"

        print("")
        break

    except ValueError:
        print("Invalid input. Please enter valid value.")


while True:
    
    try:
        PARTITION_TYPE = int(input("Enter Partition type (0-5): "))

        if 0 <= PARTITION_TYPE <= 5:
          print(f"Partition type is {PARTITION_TYPE}")
          print("Proceeding...")
          break
        else:
          print("Invalid type. Please enter a number between 0 and 5.")  

    except ValueError:
        print("Invalid input. Please enter an integer.")


PARTITION_DICT = {}

PARTITION_DICT[0] = ({ # no partition
     3:[0,1],
     4:[0,1],
     5:[2],
     6:[3],
     7:[4],
     8:[5],
}, [6,7,8])

PARTITION_DICT[1] = ({
     3:[0,1],
     4:[0,1],
     5:[2],
     6:[3],
     7:[4],
     8:[5],
}, [6,7,8])

PARTITION_DICT[2] = ({
     3:[0,1],
     4:[0,1],
     5:[2],
     8:[5],
}, [3,4,6,7,8])

PARTITION_DICT[3] = ({
     3:[0,1],
     4:[0,1],
     5:[2],
}, [3,4,5,6,7,8])

PARTITION_DICT[4] = ({
     3:[0,1],
     4:[0,1],
     8:[5],
}, [2,3,4,6,7,8])

PARTITION_DICT[5] = ({
     3:[0,1],
     4:[0,1],
}, [2,3,4,5,6,7,8])

CONNECTION, SELECTION = PARTITION_DICT[PARTITION_TYPE]
CONNECTION = dict(sorted(CONNECTION.items()))
SELECTION = sorted(SELECTION)

def read_data_df():
    raw_df = pd.read_csv(f'./data/{CIRCUIT_TYPE}_partition{PARTITION_TYPE}_rawdata.csv')

    data_df = raw_df.copy()

    columns = data_df.columns

    for index in SELECTION:
        if f"MISR_{index}" in columns and f"GS_{index}" in columns:
            data_df.drop(columns = [f"MISR_{index}", f"GS_{index}"], axis = 1, inplace = True)

    return data_df