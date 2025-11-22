import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Run a lightweight MQTT broker using the 'amqtt' package.\n"
        "This is intended for development and small deployments."
    )

    def handle(self, *args, **options):
        try:
            from amqtt.broker import Broker  # type: ignore[import-not-found]
        except Exception:  # noqa: BLE001
            self.stderr.write(
                "The 'amqtt' package is not installed.\n"
                "Install it with:\n"
                "  pip install amqtt\n"
            )
            return

        host = getattr(settings, "MQTT_BROKER_HOST", "127.0.0.1")
        port = getattr(settings, "MQTT_BROKER_PORT", 1883)

        config = {
            "listeners": {
                "default": {
                    "type": "tcp",
                    "bind": f"{host}:{port}",
                }
            },
            "sys_interval": 60,
            "auth": {"allow-anonymous": True, "password-file": None},
        }

        async def start_broker():
            broker = Broker(config)
            await broker.start()

        loop = asyncio.get_event_loop()
        self.stdout.write(
            self.style.SUCCESS(f"Starting MQTT broker on {host}:{port} (amqtt)")
        )
        try:
            loop.run_until_complete(start_broker())
            loop.run_forever()
        except KeyboardInterrupt:
            self.stdout.write("Broker stopped by user.")


