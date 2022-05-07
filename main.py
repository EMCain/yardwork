from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get-location-id", methods=['GET'])
def get_location_id():
    args = request.args
    return f"This will eventually return a location identifier corresponding to the weather forecast API. {args}"

@app.route("/suggest/<location_id>")
def suggest_days(location_id):
    args = request.args
    response = {
        "location_id": location_id,
        "chores": args.getlist("chore")
    }
    return jsonify(response)
    # get the location from the URL params ()
    # get the activities from the URL params
    # TODO eventually: call a function that looks up 
    # the weather and suggests days on which to do the activities 
