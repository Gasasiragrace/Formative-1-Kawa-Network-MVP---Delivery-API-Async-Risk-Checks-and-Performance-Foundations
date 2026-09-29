import logging
import time

from django.core.management.base import BaseCommand

from deliveries.risk_checks import process_pending


class Command(BaseCommand):
    help = 'Background worker: runs pending plot risk checks against the registry.'

    def add_arguments(self, parser):
        parser.add_argument('--once', action='store_true', help='Process once and exit.')
        parser.add_argument('--interval', type=int, default=5, help='Seconds between polls.')

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        self.stdout.write('Risk worker started. Ctrl+C to stop.')
        while True:
            process_pending()
            if options['once']:
                break
            time.sleep(options['interval'])
