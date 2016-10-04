from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create dummy data for use in a development environment."

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            print 'Only run this command in development environment'
            return

        BOOTSTRAP_COMMANDS = [
            # run migrations
            ('migrate', (), {'interactive': False}),

            # flush data
            ('flush', (), {'interactive': False}),

            # load dev data
            ('gen_dev_data', (), {}),

        ]

        for c, cargs, ckwargs in BOOTSTRAP_COMMANDS:
            kw = ckwargs.copy()
            kw.update(kwargs)
            print 'Running', c, '...'
            call_command(c, *cargs, **kw)
            print 'Done running', c
