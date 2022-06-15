from datetime import date, timedelta

from flask import Flask, jsonify, request as flask_request
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)

CHORE_DATA = {
    "mow": {
        "months": range(3, 10),  # March through September
        "frequency": 7,
    },
    "weed": {
        "months": None,
        "frequency": 3,
    },
    "pick pears": {"months": [7, 8], "frequency": 4},  # July, August
}

DEFAULT_FREQUENCY = 7


def how_often(chore_name):
    # eventually, this should be looked up from a database, and users should be able to customize it.
    try:
        chore = CHORE_DATA[chore_name]
        if chore["months"] is not None:
            # TODO account for when we are about to start a new month.
            if date.today().month not in chore["months"]:
                return None
        return chore["frequency"]
    except KeyError:
        return DEFAULT_FREQUENCY


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/get-nws-location-data", methods=["GET"])
def get_nws_location_data():
    args = flask_request.args
    geolocator = Nominatim(user_agent="python_weather_app")
    location = None
    # eventually, have several options for getting the location
    if "zip_code" in args:
        location = geolocator.geocode(
            query={
                "postalcode": args["zip_code"],
                "country": "USA",
            }
        )
    else:
        return (
            "Please specify one of the following location identifiers in the GET params: zip_code",
            400,
        )

    nws_url = f"https://api.weather.gov/points/{location.latitude},{location.longitude}"
    res = requests.get(nws_url)
    # TODO handle an error from the NWS API
    properties = res.json()["properties"]
    response = {
        "office": properties["cwa"],
        "x": properties["gridX"],
        "y": properties["gridY"],
    }
    return jsonify(response)


@app.route("/suggest/<location_id>")
def suggest_days(location_id):
    args = flask_request.args
    response = {"location_id": location_id, "chore_days": {}}
    chore_list = args.getlist("chore")
    start_day = date.today() + timedelta(days=1)  # tomorrow (TODO allow to customize)
    # for now, build the chore list for the next 2 weeks ignoring the weather.
    for chore_name in chore_list:
        frequency = how_often(chore_name)
        days_from_start = range(0, 14, frequency)
        chore_dates = [
            (start_day + timedelta(days=num)).isoformat() for num in days_from_start
        ]
        response["chore_days"][chore_name] = chore_dates

    return jsonify(response)
    # TODO eventually: call a function that looks up
    # the weather and suggests days on which to do the activities
