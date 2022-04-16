# Generate the travel itineraries from scratch.

import csv, os, random
from cities import CITIES

ROWS = 100
AIRLINES = 4
LAST_DEPARTURE = 216  # 6 pm

OUTPUT = "data.csv"


# Estimate distance between cities
def get_dist(city1, city2):
    lat1 = CITIES[city1][1]
    long1 = CITIES[city1][2]
    lat2 = CITIES[city2][1]
    long2 = CITIES[city2][2]
    return (((lat2 - lat1) ** 2) + ((long2 - long1) ** 2)) ** 0.5


# Get random city index
def rand_city():
    return random.randint(0, len(CITIES) - 1)


def main():
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
    with open(OUTPUT, newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(["Departure City", "Departure Time", "Arrival City", "Arrival Time", "Cost", "Airline"])

        # Generate random entries for travel
        for i in range(ROWS):
            dep = 0
            arr = 1
            # Flights cannot span too far of a distance.
            dist = 0
            while dep == arr or dist < 5 or dist > 20:
                dep = rand_city()
                arr = rand_city()
                dist = get_dist(dep, arr)

            dep_time = random.randint(0, LAST_DEPARTURE)
            cost = round(dist * 8, 2)
            time = round(dist * 2)
            arr_time = dep_time + time

            # Make sure the flight arrives before midnight
            if arr_time > 287:
                dep_time -= arr_time - 287
                arr_time = 287

            airline = random.randint(0, AIRLINES - 1)

            writer.writerow([dep, dep_time, arr, arr_time, cost, airline])


if __name__ == "__main__":
    main()
