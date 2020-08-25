import config


def test_color_match(app, client, requests_mock):
    url = "https://example.org"
    with open("images/teal.png", "rb") as f:
        requests_mock.get(url, headers={"Content-Length": "100"}, content=f.read())
    res = client.post("/", json={"url": url})
    assert res.status_code == 200
    expected = {"result": "Teal"}
    assert expected == res.get_json()


def test_color_distance_fail(app, client, requests_mock):
    url = "https://example.org"
    with open("images/redsquare.png", "rb") as f:
        requests_mock.get(url, headers={"Content-Length": "100"}, content=f.read())
    res = client.post("/", json={"url": url})
    assert res.status_code == 200
    expected = {"result": None}
    assert expected == res.get_json()


def test_color_distance_succeed(app, client, requests_mock):
    url = "https://example.org"
    with open("images/navy.png", "rb") as f:
        requests_mock.get(url, headers={"Content-Length": "100"}, content=f.read())
    res = client.post("/", json={"url": url})
    assert res.status_code == 200
    expected = {"result": None}
    assert expected == res.get_json()


def test_invalid_schema(app, client):
    res = client.post("/", json={"url": "waffles://example.org"})
    assert res.status_code == 400
    expected = {"message": "URL has an invalid schema"}
    assert expected == res.get_json()


def test_unreachable_url(app, client):
    res = client.post("/", json={"url": "https://badurl"})
    assert res.status_code == 422
    expected = {"message": "Unable to connect to URL"}
    assert expected == res.get_json()


def test_not_image(app, client, requests_mock):
    url = "https://example.org"
    requests_mock.get(url, headers={"Content-Length": "100"}, text="not an image")
    res = client.post("/", json={"url": url})
    assert res.status_code == 400
    expected = {"message": "URL is not an image"}
    assert expected == res.get_json()


def test_bad_json(app, client):
    res = client.post("/", json={"badkey": "badvalue"})
    assert res.status_code == 400
    expected = {"message": "URL key missing from JSON post data"}
    assert expected == res.get_json()


def test_too_large(app, client, requests_mock):
    url = "https://example.org/"
    requests_mock.get(
        url,
        headers={"Content-Length": str(config.max_file_size + 1)},
        text="hello world",
    )
    res = client.post("/", json={"url": url})
    assert res.status_code == 400
    expected = {
        "message": "File larger than allowed maximum ({})".format(config.max_file_size)
    }
    assert expected == res.get_json()
