# Determine the best way to get from point A to point B, optimizing for cost, travel time or number of flights.

from cities import CITIES
from qubo import Qubo

def get_flights(origin, destination, token, app):
    qubo = Qubo(3, origin, destination, app)
    qubo.solve(token=token)
    results = qubo.analyze_results()
    return results
