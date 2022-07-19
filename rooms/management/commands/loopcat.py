from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "let's Loop!"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            help="how many loop?",
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS(f'count_{t+1}'))
