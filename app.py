from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import exceptions
from math import sqrt
import numpy
import config
import requests

app = Flask(__name__)


def color_distance(rgb1, rgb2):
    """
    Calculate the Euclidean distance between two RGB values.
    This works because Euclidean distance is l2 norm and the default value
    of ord parameter in numpy.linalg.norm is 2.
    https://stackoverflow.com/a/1401828/1043727
    """
    rgb1 = numpy.array(rgb1)
    rgb2 = numpy.array(rgb2)
    distance = numpy.linalg.norm(rgb2 - rgb1)
    return distance


def find_closest(color):
    """
    Find the closest color name given a (r, g, b) tuple
    """
    distance = float("inf")
    color_name = None
    for rgb, name in config.colors.items():
        new_distance = color_distance(color, rgb)
        if new_distance < distance:
            distance = new_distance
            color_name = name
    return distance, color_name


@app.route("/", methods=["POST"])
def detect_common_color():
    request_json = request.get_json()

    if "url" not in request_json:
        raise exceptions.InvalidUsage("URL key missing from JSON post data")

    try:
        r = requests.get(request_json["url"], stream=True)
    except requests.exceptions.InvalidSchema:
        raise exceptions.InvalidUsage("URL has an invalid schema")
    except requests.exceptions.ConnectionError as e:
        raise exceptions.ConnectionError("Unable to connect to URL")
    except requests.exceptions.MissingSchema:
        raise exceptions.InvalidUsage(
            "No schema supplied. Perhaps you meant http://{}?".format(
                request_json["url"]
            )
        )

    if int(r.headers["Content-length"]) > config.max_file_size:
        raise exceptions.InvalidUsage(
            "File larger than allowed maximum ({})".format(config.max_file_size)
        )

    try:
        im = Image.open(r.raw)
    except UnidentifiedImageError:
        raise exceptions.InvalidUsage("URL is not an image")

    count, rgb = max(im.getcolors(im.size[0] * im.size[1]))
    distance, color_name = find_closest(rgb)
    if distance > config.max_color_distance:
        return jsonify({"result": None})
    return jsonify({"result": color_name})


@app.errorhandler(exceptions.InvalidUsage)
@app.errorhandler(exceptions.ConnectionError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
