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
BLOCK_SIZE = ((CITY_COUNT * 2) + (TIME_QUBITS * 2) + NUM_FLIGHTS)


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
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, NUM_FLIGHTS):
                    q2 = block + j
                    self.qubo[(q1, q2)] += 2

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
                    q2 = block + i
                    self.qubo[(q1, q2)] += 2

            # Departure time
            block += CITY_COUNT
            for i in range(TIME_QUBITS):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, TIME_QUBITS):
                    q2 = block + i
                    self.qubo[(q1, q2)] += 2

            # Arrival time
            block += TIME_QUBITS
            for i in range(TIME_QUBITS):
                q1 = block + i
                self.qubo[(q1, q1)] += -1
                for j in range(i + 1, TIME_QUBITS):
                    q2 = block + i
                    self.qubo[(q1, q2)] += 2

        # Assert that departure city, departure time, arrival city and arrival time correspond to flight ID.
        with open("data.csv", newline='', mode='r') as file:
            reader = csv.reader(file)
            for id, row in enumerate(reader):
                # Skip the first row (header)
                if id < 1:
                    continue

                # Apply constraint to each flight block
                for f in range(self.flight_count):
                    block = BLOCK_SIZE * f
                    flight_id = id - 1
                    departure_city = row[0]
                    arrival_city = row[1]
                    departure_time = row[2]
                    arrival_time = row[3]

                    q1 = block + flight_id

                    for i in range(CITY_COUNT):
                        # Enforce correct departure city
                        q2 = block + NUM_FLIGHTS + i
                        if i == departure_city:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure city
                        else:
                            self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival city
                        q2 = block + NUM_FLIGHTS + CITY_COUNT + i
                        if i == arrival_city:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure city
                        else:
                            self.qubo[(q1, q2)] += 1

                    for i in range(TIME_QUBITS):
                        # Enforce correct departure time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + i
                        if i == departure_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure time
                        else:
                            self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS + i
                        if i == arrival_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong arrival time
                        else:
                            self.qubo[(q1, q2)] += 1

        # Assert that first flight starts at departure city.

        # Assert that last flight ends at arrival city.

        # Assert that each flight departs from the previous flight's arrival.

        # Assert that each flight departs after the previous flight's arrival.

    # Solve QUBO using either simulated or hybrid annealing
    def solve(self):
        token = input("Enter DWave token: ")
        # sampler = LeapHybridSampler(token=token)
        sampler = SimulatedAnnealingSampler()
        self.results = sampler.sample_qubo(self.qubo, num_reads=10)

    # Analyze and print results
    def analyze_results(self):
        for result in self.results:
            # Get flight ID
            flight_id = -1
            for i in range(NUM_FLIGHTS):
                if result[i] == 1:
                    if flight_id == -1:
                        flight_id = i
                    else:
                        print("Invalid result!")
                        break
            if flight_id == -1:
                print("Invalid result!")
            else:
                print(flight_id)


