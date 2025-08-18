import random
import pandas as pd
import numpy as np
from config import *

ERROR_DATA = []

for i in range(G_NUM):
    cir_idx = [1,1,1,0,0,0,0,0,0]
    random.shuffle(cir_idx)
    for j in range(G_LEN):
        row = []
        rate = 0.85 * (np.exp(-(0.03*j))) + 0.15
        err = 1 if random.random() > rate else 0
        row.append(err)
        for k in range(len(cir_idx)):
            row.append(cir_idx[k])
        ERROR_DATA.append(row)

ERROR_DF = pd.DataFrame(ERROR_DATA, columns = ["error", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
