# Quantum Unconstrained Binary Optimization

# Flight ID [100], Departure City [20], Departure Time [288], Arrival City [20], Arrival Time [288]

from cities import CITIES

CITY_COUNT = len(CITIES)
TIME_QUBITS = 288
NUM_FLIGHTS = 100  # TODO: Harvest this number from data.csv
BLOCK_SIZE = ((CITY_COUNT * 2) + (TIME_QUBITS * 2) + NUM_FLIGHTS)

class Qubo:
    def __init__(self, flight_count, departure_city, arrival_city):
        self.flight_count = flight_count
        self.departure_city = departure_city
        self.arrival_city = arrival_city

        # Calculate number of qubits
        self.size = BLOCK_SIZE * flight_count

        # Initialize empty qubo
        self.qubo = {}
        for i in range(self.size):
            self.qubo[i] = {}
            for j in range(i, self.size):
                self.qubo[i][j] = 0

    # Add constraints to the QUBO to generate the problem.
    def gen_constraints(self):
        # Assert that exactly one qubit within each category is enabled.

        # Assert that departure city, departure time, arrival city and arrival time correspond to flight ID.

        # Assert that first flight starts at departure city.

        # Assert that last flight ends at arrival city.

        # Assert that each flight departs from the previous flight's arrival.

        # Assert that each flight departs after the previous flight's arrival.


    # Solve QUBO using either simulated or hybrid annealing
    def solve_qubo(self):
        pass

    # Analyze and print results
    def analyze_results(self):
        pass