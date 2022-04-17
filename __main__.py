# Determine the best way to get from point A to point B, optimizing for cost, travel time or number of flights.

from cities import CITIES
from qubo import Qubo

DEPARTURE = 0
ARRIVAL = 1


def main():
    qubo = Qubo(3, 0, 1)
    qubo.solve()
    qubo.analyze_results()

if __name__ == "__main__":
    main()