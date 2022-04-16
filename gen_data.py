# Generate the travel itineraries from scratch.

import csv, os, random

ROWS = 100
AIRLINES = 4
LAST_DEPARTURE = 216  # 6 pm

OUTPUT = "data.csv"

CITIES = [("New York", 40.66, 73.93),
          ("Los Angeles", 34.01, 118.41),
          ("Chicago", 41.83, 87.68),
          ("Houston", 29.78, 95.39),
          ("Phoenix", 33.57, 112.09),
          ("Philadelphia", 40.00, 75.13),
          ("San Antonio", 29.47, 98.52),
          ("San Diego", 32.81, 117.13),
          ("Dallas", 32.79, 96.76),
          ("San Jose", 37.29, 121.81),
          ("Austin", 30.30, 97.75),
          ("Jacksonville", 30.33, 81.66),
          ("Fort Worth", 32.78, 97.34),
          ("Columbus", 39.98, 82.98),
          ("Indianapolis", 39.77, 86.14),
          ("Charlotte", 35.20, 80.83),
          ("San Francisco", 37.72, 123.03),
          ("Seattle", 47.62, 122.35),
          ("Denver", 39.76, 104.88),
          ("Washington D.C.", 38.90, 77.01)]


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
            dep = rand_city()
            arr = rand_city()
            while dep == arr:
                arr = rand_city()
            dep_time = random.randint(0, LAST_DEPARTURE)
            dist = get_dist(dep, arr)
            cost = round(dist * 3, 2)
            time = round(dist * 1.5)
            arr_time = dep_time + time

            # Make sure the flight arrives before midnight
            if arr_time > 287:
                dep_time -= arr_time - 287
                arr_time = 287

            airline = random.randint(0, AIRLINES - 1)

            writer.writerow([dep, dep_time, arr, arr_time, cost, airline])


if __name__ == "__main__":
    main()
