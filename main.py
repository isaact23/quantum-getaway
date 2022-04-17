from flask import Flask, render_template, request
import csv
import flight_solver
from cities import CITIES

app = Flask(__name__)


@app.route('/')
def form():
    return render_template("form.html")

@app.route('/flights')
def flights():
    # Read flight data from file
    flight_data = {}
    with app.open_resource("data.csv", mode='r') as file:
        reader = csv.reader(file)
        for id, row in enumerate(reader):
            if id < 1:
                continue
            flight = {}
            flight['id'] = id - 1
            flight['departure_city'] = CITIES[int(row[0])][0]
            flight['arrival_city'] = CITIES[int(row[1])][0]
            departure_minutes = int(row[2]) * 5
            flight['departure_time'] = '{:02d}'.format(departure_minutes // 60) + ":" + '{:02d}'.format(
                departure_minutes % 60)
            arrival_minutes = int(row[3]) * 5
            flight['arrival_time'] = '{:02d}'.format(arrival_minutes // 60) + ":" + '{:02d}'.format(
                arrival_minutes % 60)

            flight_data[id - 1] = flight
    return render_template("flights.html", flights=flight_data)

def make_flight_readable(flight):
    flight['departure_city'] = CITIES[flight['departure_city']][0]
    flight['arrival_city'] = CITIES[flight['arrival_city']][0]
    departure_minutes = flight['departure_time'] * 5
    flight['departure_time'] = '{:02d}'.format(departure_minutes // 60) + ":" + '{:02d}'.format(
        departure_minutes % 60)
    arrival_minutes = flight['arrival_time'] * 5
    flight['arrival_time'] = '{:02d}'.format(arrival_minutes // 60) + ":" + '{:02d}'.format(
        arrival_minutes % 60)
    return flight

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        return f"/results is not intended to be accessed directly - please submit the form and try again."
    if request.method == 'POST':
        form_data = request.form
        origin = int(form_data['Origin'])
        destination = int(form_data['Destination'])
        token = form_data['Key']
        flight_results = flight_solver.get_flights(origin, destination, token, app)
        # flight_results = [{0: {'id': 84, 'departure_city': 0, 'arrival_city': 7, 'departure_time': 52, 'arrival_time': 62}, 1: {'id': 63, 'departure_city': 7, 'arrival_city': 17, 'departure_time': 81, 'arrival_time': 112}, 2: {'id': 91, 'departure_city': 17, 'arrival_city': 19, 'departure_time': 194, 'arrival_time': 215}}, {0: {'id': 87, 'departure_city': 0, 'arrival_city': 8, 'departure_time': 54, 'arrival_time': 79}, 1: {'id': 45, 'departure_city': 8, 'arrival_city': 18, 'departure_time': 287, 'arrival_time': 80}, 2: {'id': 12, 'departure_city': 18, 'arrival_city': 19, 'departure_time': 191, 'arrival_time': 212}}, {0: {'id': 45, 'departure_city': 0, 'arrival_city': 18, 'departure_time': 59, 'arrival_time': 80}, 1: {'id': 18, 'departure_city': 18, 'arrival_city': 18, 'departure_time': 115, 'arrival_time': 139}, 2: {'id': 12, 'departure_city': 18, 'arrival_city': 19, 'departure_time': 191, 'arrival_time': 212}}, {0: {'id': 6, 'departure_city': 0, 'arrival_city': 11, 'departure_time': 32, 'arrival_time': 58}, 1: {'id': 8, 'departure_city': 11, 'arrival_city': 4, 'departure_time': 113, 'arrival_time': 143}, 2: {'id': 84, 'departure_city': 4, 'arrival_city': 19, 'departure_time': 265, 'arrival_time': 62}}, {0: {'id': 6, 'departure_city': 0, 'arrival_city': 2, 'departure_time': 32, 'arrival_time': 58}, 1: {'id': 49, 'departure_city': 2, 'arrival_city': 10, 'departure_time': 108, 'arrival_time': 139}, 2: {'id': 86, 'departure_city': 10, 'arrival_city': 19, 'departure_time': 151, 'arrival_time': 110}}, {0: {'id': 48, 'departure_city': 0, 'arrival_city': 15, 'departure_time': 62, 'arrival_time': 81}, 1: {'id': 9, 'departure_city': 15, 'arrival_city': 3, 'departure_time': 258, 'arrival_time': 39}, 2: {'id': 31, 'departure_city': 3, 'arrival_city': 19, 'departure_time': 44, 'arrival_time': 56}}, {0: {'id': 76, 'departure_city': 0, 'arrival_city': 17, 'departure_time': 37, 'arrival_time': 68}, 1: {'id': 91, 'departure_city': 17, 'arrival_city': 9, 'departure_time': 194, 'arrival_time': 215}, 2: {'id': 31, 'departure_city': 9, 'arrival_city': 19, 'departure_time': 244, 'arrival_time': 56}}, {0: {'id': 6, 'departure_city': 0, 'arrival_city': 11, 'departure_time': 32, 'arrival_time': 58}, 1: {'id': 26, 'departure_city': 11, 'arrival_city': 10, 'departure_time': 84, 'arrival_time': 113}, 2: {'id': 86, 'departure_city': 10, 'arrival_city': 19, 'departure_time': 138, 'arrival_time': 110}}, {0: {'id': 82, 'departure_city': 0, 'arrival_city': 6, 'departure_time': 96, 'arrival_time': 133}, 1: {'id': 57, 'departure_city': 6, 'arrival_city': 18, 'departure_time': 243, 'arrival_time': 146}, 2: {'id': 13, 'departure_city': 18, 'arrival_city': 19, 'departure_time': 263, 'arrival_time': 152}}, {0: {'id': 23, 'departure_city': 0, 'arrival_city': 12, 'departure_time': 26, 'arrival_time': 58}, 1: {'id': 82, 'departure_city': 12, 'arrival_city': 2, 'departure_time': 96, 'arrival_time': 133}, 2: {'id': 89, 'departure_city': 2, 'arrival_city': 19, 'departure_time': 254, 'arrival_time': 72}}]

        if flight_results is None:
            return render_template('error.html')
        else:
            # Make flight results readable
            for result in flight_results:
                for flight in result:
                    result[flight] = make_flight_readable(result[flight])

            print(flight_results)
            return render_template('results.html', results=flight_results)
