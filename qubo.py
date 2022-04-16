# Quantum Unconstrained Binary Optimization

from cities import CITIES

TIME_QUBITS = 576
NUM_FLIGHTS = 100  # TODO: Harvest this number from data.csv

class Qubo:
    def __init__(self, flight_count):
        # Calculate number of qubits
        self.size = (len(CITIES) * 2) + TIME_QUBITS + NUM_FLIGHTS

        self.qubo = {}
        for i in range(self.size):
            self.qubo[i] = {}
