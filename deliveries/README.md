# Kawa Network MVP

Django REST API for coffee delivery traceability: farmers, plots, deliveries, async risk checks.

## Setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment variables
None required. The app uses SQLite (`db.sqlite3`) and default Django settings.

## Async risk checks
Registering a plot returns immediately with `risk_status: pending`. A background worker processes the queue, which is stored in the database. Start it in a second terminal (venv active):
```
python manage.py run_risk_worker
```
Each attempt is logged, for example: `Risk check plot=1 outcome=clear status=clear duration_ms=2443`.
Plots created while the worker is stopped are picked up when it starts.

## Example requests
```
curl -X POST http://127.0.0.1:8000/api/farmers/ -H "Content-Type: application/json" \
  -d '{"name":"Test Farmer","phone_number":"0788000000","national_id":"1199000000000001"}'

curl -X POST http://127.0.0.1:8000/api/plots/ -H "Content-Type: application/json" \
  -d '{"farmer":1,"sector":"Nyaruguru","station":"Nyaruguru Station"}'

curl http://127.0.0.1:8000/api/plots/

curl -X POST http://127.0.0.1:8000/api/deliveries/ -H "Content-Type: application/json" \
  -d '{"plot":1,"weight_kg":"25.5"}'

curl http://127.0.0.1:8000/api/deliveries/      # paginated delivery feed
curl http://127.0.0.1:8000/api/price-schedule/
```

## Performance feature
The delivery feed (`GET /api/deliveries/`) is cursor-paginated (`next`, `previous`, `results`) for harvest-peak volume on slow connections. See ADR.md.


## API schema
OpenAPI schema: `schema.yml`. Regenerate with:
python manage.py spectacular --file schema.yml


## AI-use annex
I used an AI assistant for debugging help (settings errors, git and terminal commands) and for documentation formatting. The ADR reasoning and design decisions are my own.
