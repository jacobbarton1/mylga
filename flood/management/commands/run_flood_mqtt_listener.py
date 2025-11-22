import json

from django.conf import settings
from django.core.management.base import BaseCommand

from flood.models import FloodSite, Uplink


class Command(BaseCommand):
    help = (
        "Subscribe to MQTT topics and store incoming floodway sensor uplinks.\n"
        "This expects JSON payloads containing at least an IMEI or site handle "
        "and a distance measurement in millimetres."
    )

    def handle(self, *args, **options):
        try:
            import paho.mqtt.client as mqtt  # type: ignore[import-not-found]
        except Exception:  # noqa: BLE001
            self.stderr.write(
                "The 'paho-mqtt' package is not installed.\n"
                "Install it with:\n"
                "  pip install paho-mqtt\n"
            )
            return

        host = getattr(settings, "MQTT_BROKER_HOST", "127.0.0.1")
        port = getattr(settings, "MQTT_BROKER_PORT", 1883)

        def on_connect(client, userdata, flags, rc):  # type: ignore[override]
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("Connected to MQTT broker"))
                client.subscribe("flood/+/uplink")
            else:
                self.stderr.write(f"MQTT connection failed with code {rc}")

        def on_message(client, userdata, msg):  # type: ignore[override]
            try:
                payload = json.loads(msg.payload.decode("utf-8"))
            except Exception:
                self.stderr.write("Received non-JSON payload; ignoring")
                return

            imei = payload.get("IMEI") or payload.get("imei")
            handle = payload.get("handle") or payload.get("site") or payload.get(
                "station"
            )

            site = None
            if imei:
                site = FloodSite.objects.filter(imei=imei).first()
            if site is None and handle:
                site = FloodSite.objects.filter(handle=str(handle)).first()

            if site is None:
                self.stderr.write(
                    "No FloodSite found for incoming payload; "
                    "ensure IMEI or handle fields match configured sites."
                )
                return

            # Flexible distance parsing
            distance = (
                payload.get("distance_mm")
                or payload.get("distance")
                or payload.get("WL_Ht")
            )
            if distance is None:
                self.stderr.write("Payload missing distance field; ignoring")
                return

            try:
                distance_mm = int(float(distance))
            except (TypeError, ValueError):
                self.stderr.write("Could not parse distance field; ignoring")
                return

            battery = payload.get("battery") or payload.get("battery_v")
            signal = payload.get("signal") or payload.get("rssi")

            try:
                battery_v = float(battery) if battery is not None else None
            except (TypeError, ValueError):
                battery_v = None

            try:
                signal_dbm = int(signal) if signal is not None else None
            except (TypeError, ValueError):
                signal_dbm = None

            Uplink.objects.create(
                site=site,
                distance_mm=distance_mm,
                battery_v=battery_v,
                signal_dbm=signal_dbm,
                raw_payload=payload,
            )

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        self.stdout.write(
            f"Connecting to MQTT broker at {host}:{port} and subscribing to flood/+/uplink"
        )
        client.connect(host, port, 60)
        client.loop_forever()


