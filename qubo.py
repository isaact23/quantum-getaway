# Quantum Unconstrained Binary Optimization

# Flight ID [100], Departure City [20], Arrival City [20], Departure Time [288], Arrival Time [288]

import csv, sys
from cities import CITIES

try:
    from dwave.system.samplers import LeapHybridSampler
    from neal.sampler import SimulatedAnnealingSampler
except:
    print("Failed to import DWave samplers")
    sys.exit()

CITY_COUNT = len(CITIES)
TIME_QUBITS = 288
NUM_FLIGHTS = 100
BLOCK_SIZE = (CITY_COUNT * 2) + (TIME_QUBITS * 2) + NUM_FLIGHTS

class Qubo:
    def __init__(self, flight_count, departure_city, arrival_city):
        self.flight_count = flight_count
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.results = None

        # Calculate number of qubits
        self.size = BLOCK_SIZE * flight_count

        # Initialize empty qubo
        self.qubo = {}
        for i in range(self.size):
            for j in range(i, self.size):
                self.qubo[(i, j)] = 0

        self.gen_constraints()

    # Add constraints to the QUBO to generate the problem.
    def gen_constraints(self):
        # Assert that exactly one qubit within each category is enabled.
        for f in range(self.flight_count):
            # Flight ID
            block = BLOCK_SIZE * f
            for i in range(NUM_FLIGHTS):
                q1 = block + i
                self.qubo[(q1, q1)] += -4
                for j in range(i + 1, NUM_FLIGHTS):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 8

            # Departure city
            block += NUM_FLIGHTS
            for i in range(CITY_COUNT):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, CITY_COUNT):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 2

            # Arrival city
            block += CITY_COUNT
            for i in range(CITY_COUNT):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, CITY_COUNT):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 2

            # Departure time
            block += CITY_COUNT
            for i in range(TIME_QUBITS):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, TIME_QUBITS):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 2

            # Arrival time
            block += TIME_QUBITS
            for i in range(TIME_QUBITS):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, TIME_QUBITS):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 2

        # Assert that departure city, departure time, arrival city and arrival time correspond to flight ID.
        with open("data.csv", newline='', mode='r') as file:
            reader = csv.reader(file)
            for id, row in enumerate(reader):  # TODO: Comply with NUM_FLIGHTS
                # Skip the first row (header)
                if id < 1:
                    continue

                # Apply constraint to each flight block
                for f in range(self.flight_count):
                    block = BLOCK_SIZE * f
                    flight_id = id - 1
                    departure_city = int(row[0])
                    arrival_city = int(row[1])
                    departure_time = int(row[2])
                    arrival_time = int(row[3])

                    q1 = block + flight_id

                    for i in range(CITY_COUNT):
                        # Enforce correct departure city
                        q2 = block + NUM_FLIGHTS + i
                        if i == departure_city:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure city
                        else:
                            pass
                            #self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival city
                        q2 = block + NUM_FLIGHTS + CITY_COUNT + i
                        if i == arrival_city:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure city
                        else:
                            pass
                            #self.qubo[(q1, q2)] += 1

                    for i in range(TIME_QUBITS):
                        # Enforce correct departure time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + i
                        if i == departure_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure time
                        else:
                            pass
                            #self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS + i
                        if i == arrival_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong arrival time
                        else:
                            pass
                            #self.qubo[(q1, q2)] += 1

        # Assert that first flight starts at departure city.
        for i in range(CITY_COUNT):
            q = NUM_FLIGHTS + i
            if i == self.departure_city:
                self.qubo[(q, q)] -= 1
            else:
                self.qubo[(q, q)] += 1

        # Assert that last flight ends at arrival city.
        for i in range(CITY_COUNT):
            q = (BLOCK_SIZE * (self.flight_count - 1)) + NUM_FLIGHTS + CITY_COUNT + i
            if i == self.arrival_city:
                self.qubo[(q, q)] -= 1
            else:
                self.qubo[(q, q)] += 1


        # Assert that each flight departs from the previous flight's arrival.
        for f in range(self.flight_count - 1):
            for i in range(CITY_COUNT):
                q1 = (BLOCK_SIZE * f) + NUM_FLIGHTS + CITY_COUNT + i
                q2 = (BLOCK_SIZE * (f + 1)) + NUM_FLIGHTS + i
                self.qubo[(q1, q1)] += 1
                self.qubo[(q2, q2)] += 1
                self.qubo[(q1, q2)] -= 2

        # Assert that each flight departs after the previous flight's arrival.
        for f in range(self.flight_count - 1):
            for i in range(TIME_QUBITS):
                for j in range(i):
                    q1 = (BLOCK_SIZE * f) + NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS + i
                    q2 = (BLOCK_SIZE * (f + 1)) + NUM_FLIGHTS + (CITY_COUNT * 2) + j
                    self.qubo[(q1, q2)] += 1

    # Analyze and print results
    def analyze_results(self):
        for datum in self.results.data(fields=['sample', 'energy']):
            print("Result:")
            print("Energy", datum.energy)
            for flight in range(self.flight_count):
                block = flight * BLOCK_SIZE
                for i in range(BLOCK_SIZE):
                    if datum.sample[i + block] == 1:
                        if i < NUM_FLIGHTS:
                            print("Flight ID", i)
                        elif i < NUM_FLIGHTS + CITY_COUNT:
                            print("Departure city", i - NUM_FLIGHTS)
                        elif i < NUM_FLIGHTS + (CITY_COUNT * 2):
                            print("Arrival city", i - NUM_FLIGHTS - CITY_COUNT)
                        elif i < NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS:
                            print("Departure time", i - NUM_FLIGHTS - (CITY_COUNT * 2))
                        else:
                            print("Arrival time", i - NUM_FLIGHTS - (CITY_COUNT * 2) - TIME_QUBITS)

    # Solve QUBO using either simulated or hybrid annealing
    def solve(self):
        # Normalize QUBO
        """max = 0
        for i in range(self.size):
            for j in range(i, self.size):
                val = self.qubo[(i, j)]
                if val > max:
                    max = val
        for i in range(self.size):
            for j in range(i, self.size):
                self.qubo[(i, j)] /= max"""

        token = input("Enter DWave token: ")
        sampler = LeapHybridSampler(token=token)
        # sampler = SimulatedAnnealingSampler()
        self.results = sampler.sample_qubo(self.qubo)

# 6, 4, 55
# 6, 4, 30