# Murweh LGA tools – Django project

This Django project hosts a single site for Murweh Shire Council that brings
together several internal tools:

- Fleet defect reporting and maintenance history.
- Drinking water quality management (schemes, sampling, incidents, actions).
- Journey management planning for remote workers.
- Floodway sensor deployment management and public monitoring UI.

The project is based on the original `Django-Template` structure and is intended
for deployment to environments such as Opalstack with SQLite for development.

## Local development

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add any environment variables you need (for example in a shell profile or
`.env` loaded by your process manager):

```bash
export SECRET_KEY=change-me-for-production
export GOOGLE_MAPS_API_KEY=your-browser-api-key
export MQTT_BROKER_HOST=127.0.0.1
export MQTT_BROKER_PORT=1883
```

Run migrations and create the development superuser as requested:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_dev_superuser
```

Then run the development server:

```bash
python manage.py runserver
```

The main apps are available at:

- `/` – Home dashboard
- `/fleet/` – Fleet defects and maintenance
- `/water/` – Drinking water quality management
- `/journeys/` – Journey management plans
- `/flood/` – Public floodway map and history

## Email-based sign in

Authentication is via email validation links using a simple JWT-style token:

- Visit `/accounts/login/` and enter an `@murweh.qld.gov.au` address.
- A sign-in link is emailed; in development it is also printed to the console.
- First-time users are prompted to complete their profile after signing in.

The development superuser is:

- Email: `jacob_barton@murweh.qld.gov.au`
- Password: `1234`

Create or update this account using the `create_dev_superuser` management command.

## MQTT broker and floodway ingestion

An optional lightweight MQTT broker can be run using the `amqtt` package:

```bash
pip install amqtt
python manage.py run_mqtt_broker
```

Floodway devices can publish JSON payloads to topics like `flood/<device>/uplink`.
To persist these uplinks into the Django database, install `paho-mqtt` and run:

```bash
pip install paho-mqtt
python manage.py run_flood_mqtt_listener
```

The public flood map (`/flood/`) and history view (`/flood/plot/<handle>/`)
consume the stored uplinks through JSON endpoints in the `flood` app.
