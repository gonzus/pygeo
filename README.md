To install all dependencies:
```
mise install
```

To run tests:
```
pytest -v
```

To run the server in development, using a local SQLite database:
```
FLASK_ENV=dev python app.py
```

To run the server in production, using a Postgres database:
```
FLASK_ENV=prod python app.py
```

Some command-line `curl` examples, assuming the following environment variables:
* `URL=http://127.0.0.1:5000/api/users`
* `JSON="Content-Type: application/json"`

```
curl -X POST $URL -H $JSON -d '{"email": "gonzo@example.com", "name": "Gonzo the Great"}'
curl -X POST $URL -H $JSON -d '{"email": "nico@example.com", "name": "Nico the Amazing"}'
curl -X GET $URL | jq .
curl -X GET $URL/1
curl -X GET $URL/2
curl -X GET $URL/3
curl -X DELETE $URL/1
curl -X DELETE $URL/1
curl -X GET $URL | jq .
curl -X GET $URL/1
curl -X GET $URL/2
curl -X PATCH $URL/3 -H $JSON -d '{"name": "Gonzo the Obnoxious"}' | jq .
curl -X GET $URL/1
```
