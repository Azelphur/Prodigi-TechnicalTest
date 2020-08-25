# Prodigi technical test

The API accepts HTTP POST requests with a JSON body, such as {"url": "http://example.org/example.jpg"}

The application is up and running at https://prodigi.home.azelphur.com, as such you can run some real world tests against it with the following examples:

This will return {"result": "Black"}

```curl --header "Content-Type: application/json" --request POST --data '{"url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-black.png"}' https://prodigi.home.azelphur.com```

This will return {"result": null} as there is no close color match

```curl --header "Content-Type: application/json" --request POST --data '{"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Waffles_with_Strawberries.jpg/2560px-Waffles_with_Strawberries.jpg"}' https://prodigi.home.azelphur.com```

# Configuration

The config file contains a few variables.

max_file_size - The maximum allowed image file size allowed for checking. Images larger than this size will not be downloaded and a HTTP 400 will be thrown.

max_color_distance - The maximum Euclidean distance allowed from the nearest color before null is returned.

colors - a dict of (r, g, b) keys and color name values.

# Running locally

Clone the repository and run `docker-compose up -d`

# Testing

Run `docker exec -it prodigi-test python3 -m pytest`

# Improvement

If this were to be deployed, running the flask development server probably isn't the best idea. Would deploy on uwsgi or something. Some caching would also be a good idea.

# Evidence of behaviour
Screenshots are in the screenshots directory. Example requests are above.
