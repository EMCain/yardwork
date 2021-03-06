# yardwork
Find out when you should do yard work based on the local weather. 


Based on [Flask Quickstart](https://flask.palletsprojects.com/en/2.1.x/quickstart/).


## Initial setup:

Create a virtual environment using Python 3. I had to do it like this:

```sh
python3 -m venv venv
```

Activate the environment. Set up with [pip-tools](https://alysivji.github.io/python-managing-dependencies-with-pip-tools.html).
```sh
pip install pip-tools
pip-compile --output-file=requirements.txt requirements.in
```

## Run app
Activate the virtual environment if you haven't already.

```sh
export FLASK_APP=main
export FLASK_ENV=development
flask run
 * Running on http://127.0.0.1:5000/
```

# APIs and libraries used

[National Weather Service](https://www.weather.gov/documentation/services-web-api#/default/gridpoint)

[GeoCode](https://geopy.readthedocs.io/en/latest/index.html)

[Nominatim](https://nominatim.org/release-docs/develop/api/Search/)