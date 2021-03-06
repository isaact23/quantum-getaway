# Quantum Unconstrained Binary Optimization

# Flight ID [100], Departure City [20], Arrival City [20], Departure Time [288], Arrival Time [288]

import csv
import sys

from dwave.cloud.exceptions import SolverNotFoundError

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
    def __init__(self, flight_count, departure_city, arrival_city, app):
        self.app = app
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
        with self.app.open_resource("data.csv", mode='r') as file:
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
                            # self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival city
                        q2 = block + NUM_FLIGHTS + CITY_COUNT + i
                        if i == arrival_city:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure city
                        else:
                            pass
                            # self.qubo[(q1, q2)] += 1

                    for i in range(TIME_QUBITS):
                        # Enforce correct departure time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + i
                        if i == departure_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong departure time
                        else:
                            pass
                            # self.qubo[(q1, q2)] += 1

                        # Enforce correct arrival time
                        q2 = block + NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS + i
                        if i == arrival_time:
                            self.qubo[(q1, q1)] += 1
                            self.qubo[(q1, q2)] += -1
                        # Penalize wrong arrival time
                        else:
                            pass
                            # self.qubo[(q1, q2)] += 1

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

    # Analyze and return valid results
    def analyze_results(self):
        results = []
        if self.results is None:
            return None
        for datum in self.results.data(fields=['sample', 'energy']):
            valid = True
            result = {}
            for flight in range(self.flight_count):
                result[flight] = {"id": None, "departure_city": None, "arrival_city": None, "departure_time": None,
                                  "arrival_time": None}
                if not valid:
                    break
                block = flight * BLOCK_SIZE
                for i in range(BLOCK_SIZE):
                    if not valid:
                        break
                    if datum.sample[i + block] == 1:
                        if i < NUM_FLIGHTS:
                            if result[flight]["id"] is None:
                                result[flight]["id"] = i
                            else:
                                valid = False
                                break
                        elif i < NUM_FLIGHTS + CITY_COUNT:
                            if result[flight]["departure_city"] is None:
                                result[flight]["departure_city"] = i - NUM_FLIGHTS
                            else:
                                valid = False
                                break
                        elif i < NUM_FLIGHTS + (CITY_COUNT * 2):
                            if result[flight]["arrival_city"] is None:
                                result[flight]["arrival_city"] = i - NUM_FLIGHTS - CITY_COUNT
                            else:
                                valid = False
                                break
                        elif i < NUM_FLIGHTS + (CITY_COUNT * 2) + TIME_QUBITS:
                            if result[flight]["departure_time"] is None:
                                result[flight]["departure_time"] = i - NUM_FLIGHTS - (CITY_COUNT * 2)
                            else:
                                valid = False
                                break
                        else:
                            if result[flight]["arrival_time"] is None:
                                result[flight]["arrival_time"] = i - NUM_FLIGHTS - (CITY_COUNT * 2) - TIME_QUBITS
                            else:
                                valid = False
                                break
                # Ensure all fields are filled
                for field in result:
                    if result[field] is None:
                        valid = False
                        break
            if valid:
                results.append(result)

        return results

    # Solve QUBO using either simulated or hybrid annealing
    def solve(self, token=None):
        try:
            if token is None or len(token) < 1:
                print("Using simulated annealing.")
                sampler = SimulatedAnnealingSampler()
                self.results = sampler.sample_qubo(self.qubo, num_reads=10)
            else:
                print("Using quantum annealing.")
                sampler = LeapHybridSampler(token=token)
                self.results = sampler.sample_qubo(self.qubo)
        except SolverNotFoundError:
            print("Error: Solver not found.")
            self.results = None
        except:
            self.results = None
