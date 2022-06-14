from datetime import date, datetime, timedelta

from flask import Flask, jsonify, request

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


@app.route("/get-location-id", methods=["GET"])
def get_location_id():
    args = request.args
    return f"This will eventually return a location identifier corresponding to the weather forecast API. {args}"


@app.route("/suggest/<location_id>")
def suggest_days(location_id):
    args = request.args
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
