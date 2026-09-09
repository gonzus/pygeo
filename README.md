To install all dependencies:
```
mise install
```

To run all (pending) DB migrations:
```
flask db upgrade head
```

To run tests:
```
pytest -v
```

The server uses Postgres for both development and production.
You can force it to use SQLite by defining an environment variable:
```
DATABASE_URL="sqlite:///data.db"
```

To run the server in development, run one of:
```
python app.py
FLASK_ENV=dev python app.py
```

To run the server in production:
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
