import random
import numpy as np

class LogicGate:
    def __init__(self, gate_type, inputs, seq):
        self.gate_type = gate_type
        self.inputs = inputs
        self.error_prob = 1.0
        self.sample_delay = {
            'AND': (280, 360),
            'OR': (300, 350),
            'NAND': (200, 270),
            'NOR': (240, 280),
            'XOR': (400, 460),
            'NOT': (100, 130),
            'BUF': (120, 140)
            }

    def delay(self):
        base_min, base_max = self.sample_delay.get(self.gate_type)
        factor = abs(self.error_prob-1)//(0.12)
        base_min = base_min * (1 + 0.03*factor)
        base_max = base_max * (1 + 0.03*factor)

        return round(random.uniform(base_min, base_max))

    def evaluate(self, signal_values):
        in_vals = [signal_values[inp] for inp in self.inputs]

        if self.gate_type == 'AND':
            result = int(all(in_vals))
        elif self.gate_type == 'OR':
            result = int(any(in_vals))
        elif self.gate_type == 'NAND':
            result = int(not all(in_vals))
        elif self.gate_type == 'NOR':
            result = int(not any(in_vals))
        elif self.gate_type == 'XOR':
            result = int(in_vals[0] ^ in_vals[1])
        elif self.gate_type == 'NOT':
            result = int(not in_vals[0])
        elif self.gate_type == 'BUF':
            result = int(in_vals[0])
        else:
            raise ValueError(f"Unsupported gate type: {self.gate_type}")
        
        random_value = np.random.normal(0.5, 0.1, 1)
        if not(0 <= random_value <= 1):
            random_value = abs(random_value - 1)

        glitch = 0 if random_value <= self.error_prob else 1
        result = result if glitch == 0 else int(not result)

        return result, glitch

    
class Circuit:
    def __init__(self, bench_file, error, seq):
        self.error = error
        self.seq = seq
        self.input_nodes = []
        self.output_nodes = []
        self.gates = {}
        self.signal_values = {}
        self.signal_delay = {}
        self.output_values = {}
        self.output_delay = {}
        self.critical_path_delay = 0
        self.outputs = []
        self.parse_bench(bench_file)
        self.error_prob = 1.0
        self.glitch = 0

    def parse_bench(self, file_path):
        import re
        input_pattern = re.compile(r'INPUT\((\w+)\)')
        output_pattern = re.compile(r'OUTPUT\((\w+)\)')
        gate_pattern = re.compile(r'(\w+)\s*=\s*(\w+)\(([^)]+)\)')

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if m := input_pattern.match(line):
                    self.input_nodes.append(m.group(1))
                elif m := output_pattern.match(line):
                    self.output_nodes.append(m.group(1))
                elif m := gate_pattern.match(line):
                    out, gtype, ins = m.groups()
                    in_list = [i.strip() for i in ins.split(',')]
                    self.gates[out] = LogicGate(gtype, in_list, self.seq)

    def simulate(self, input_data):
         if isinstance(input_data, list):
             if len(input_data) != len(self.input_nodes):
                 raise ValueError(f"Expected {len(self.input_nodes)} inputs, got {len(input_data)}")
             input_values = dict(zip(self.input_nodes, input_data))
         elif isinstance(input_data, dict):
             input_values = input_data
         else:
             raise TypeError("Input must be a list or a dict")

         self.signal_values = dict(input_values)
         self.signal_delay.update({k: 0 for k in self.input_nodes})
         unresolved = list(self.gates.keys())


         while unresolved:
             node = unresolved.pop(0)
             gate = self.gates[node]

             if self.error and (node in self.output_nodes):
                  self.error_prob = 0.85 * (np.exp(-(0.003*self.seq))) + 0.15
             else:
                  self.error_prob = 1.0

             gate.error_prob = self.error_prob

             if all(inp in self.signal_values for inp in gate.inputs):
                  values, glitch = gate.evaluate(self.signal_values)
                  self.signal_values[node] = values
                  max_in_delay = max(self.signal_delay[inp] for inp in gate.inputs)
                  self.signal_delay[node] = max_in_delay + gate.delay()
                  self.glitch = max(self.glitch, glitch)
             else:
                  unresolved.append(node)

         self.output_values =  {out: self.signal_values[out] for out in self.output_nodes if out in self.signal_values}
         self.outputs = [val for val in self.output_values.values()]
         self.output_delay = {out: self.signal_delay.get(out, 0) for out in self.output_nodes}
         self.critical_path_delay = max(self.output_delay.values())

    def get_gate_info(self, gate_id):
        gate = self.gates.get(gate_id)
        return {
            "type": gate.gate_type,
            "inputs": gate.inputs
        } if gate else None

    def get_all_gates(self):
        return list(self.gates.keys())
    
class VECTORS:
    def __init__(self, seed, length, input_len, vector_len):

        self.state = self.initial_lfsr(seed, input_len)
        self.output = []
        self.keep = []
        self.length = length

        for i in range(length):
            self.output.append(self.step(vector_len, input_len))

    def initial_lfsr(self, seed, input_len):
        len = (2**input_len)

        if seed <= 0 or seed >= len:
            raise ValueError(f"Seed must be between 1 and {len}")

        bin_str = format(seed, f'0{input_len}b')

        return [int(b) for b in bin_str]

    def step(self, vector_len, input_len):
        vector = []
        temp = []

        for i in range(vector_len):
            self.keep.append(self.state)
            out_bit = self.state[-1]

            feedback = 0

            for j in range(input_len, 2, -2):
                feedback ^= self.state[j-1]

            temp.append(out_bit)

            if len(temp) == input_len:
                vector.append(temp)
                temp = []

            self.state = [feedback] + self.state[:-1]

        return vector