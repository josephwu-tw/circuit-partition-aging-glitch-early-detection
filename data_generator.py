import pandas as pd
from data_gen_classes import *
from config import *
from error_index import *

# functions
def get_GS(vector_len, dut_len, circuit_number):

    goldens = []
    gs = [("0"*(dut_len+4)) for _ in range(circuit_number)]
    dut_gs = [[0 for _ in range(dut_len)] for _ in range(circuit_number)]

    for i in range(vector_len):
        temp = []
        for n in range(circuit_number):
            input = get_input(i,n, dut_gs)
            circuit.error = 0
            circuit.simulate(input)
            dut_out = circuit.outputs
            gs[n] = MISR_update(gs[n], dut_out)
            dut_gs[n] = dut_out
            temp.append(gs[n])
        goldens.append(temp)

    return goldens

def MISR_update(state, DUT_output):
    new_state = ""

    for i in range(len(state)):
        if i < len(DUT_output):
            feed = str(int(state[i-1])^int(DUT_output[i]))
            if i == (len(DUT_output)-1):
                feed = str(int(feed)^int(state[-1]))
        else:
            feed = str(int(state[i-1])^0)

        new_state += feed

    return new_state

def get_input(seq, idx, dut):
    if idx in CONNECTION:
        previous = []
        for inp in range(len(dut[0])):
             for p in range(len(CONNECTION[idx])):
                 previous.append(dut[inp][p])

        input = []
        i = (idx+1)%(len(previous))
        while len(input) < len(vectors[seq][idx]):
            if i == len(previous): i = 0
            input.append(previous[i])
            i += 1

    else:
        input = vectors[seq][idx]

    return input

def get_misr_delay(seq, idx, error):
    global circuit
    input = get_input(seq, idx, DUT)
    circuit.seq = seq
    circuit.error = error
    circuit.glitch = 0
    circuit.simulate(input)
    dut_out = circuit.outputs
    delay = circuit.critical_path_delay

    if idx in CONNECTION:
        delay += max([DELAY[p] for p in CONNECTION[idx]])

    MISR[idx] = MISR_update(MISR[idx], dut_out)
    DUT[idx] = dut_out
    DELAY[idx] = delay

    return MISR[idx], delay


# setting
bench_file = f"./bench_file/{CIRCUIT_TYPE}.bench"
circuit = Circuit(bench_file = bench_file, error = 0, seq = 0)

dut_len = len(circuit.output_nodes)
input_len = len(circuit.input_nodes)

# get groups
g_vectors = []
g_goldens = []

seed_max = 2**input_len-1
for i in range(G_LEN):
    seed = i%(seed_max) + 1
    vectors = VECTORS(seed = seed,
                      length = G_LEN,
                      input_len = input_len,
                      vector_len = input_len*CIRCUIT_NUM).output
    goldens = get_GS(G_LEN, dut_len, CIRCUIT_NUM)
    g_vectors.append(vectors)
    g_goldens.append(goldens)

# generate data
data = []
for g in range(G_NUM):
    vectors = g_vectors[g]
    goldens = g_goldens[g]

    MISR = [("0"*(dut_len+4)) for _ in range(CIRCUIT_NUM)]
    DUT = [[0 for _ in range(dut_len)] for _ in range(CIRCUIT_NUM)]
    DELAY = [0 for _ in range(CIRCUIT_NUM)]
    error_index = [1,1,1,0,0,0,0,0,0]
    random.shuffle(error_index)
    while error_index[g%9] != 1:
        random.shuffle(error_index)

    for i in range(G_LEN):
        row = []
        row.append(i//15)
        y_prob = []
        y_glitch = []

        for n in range(CIRCUIT_NUM):
            error_flag = error_index[n]
            misr, delay = get_misr_delay(i, n, error_flag)
            gs = goldens[i][n]
            y_prob.append(circuit.error_prob)

            y_glitch.append(circuit.glitch)

            if n in SELECTION:
                row.append(delay)
                row.append(misr)
                row.append(gs)
                row.append(int(misr, 2))
                row.append(sum(int(misr[b])^int(gs[b]) for b in range(len(misr))))

        row.append(min(y_prob))
        row.append(max(y_glitch))

        data.append(row)

columns = []
columns.append("period")
for select in SELECTION:
    columns.append(f"Delay_{select+1}")
    columns.append(f"MISR_{select+1}")
    columns.append(f"GS_{select+1}")
    columns.append(f"MISR D_{select+1}")
    columns.append(f"vs GS_{select+1}")


columns.append("Y_prob")
columns.append("Y_glitch")

df = pd.DataFrame(data, columns = columns)

df.to_csv(f'./data/{CIRCUIT_TYPE}_partition{PARTITION_TYPE}_rawdata.csv', index = False)

