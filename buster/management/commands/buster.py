from django.core.management.base import LabelCommand, CommandError

from ... import reload_buster_cache, clear_buster_cache


class Command(LabelCommand):
    args = '<clear | reload>'
    label = 'command'
    help = """clear: clear cached busters json
reload: reload cached busters json"""

    def handle_label(self, label, **options):

        if label == 'clear':
            clear_buster_cache()
            self.stdout.write('Cleared busters cache.')
        elif label == 'reload':
            reload_buster_cache()
            self.stdout.write('Reloaded busters cache.')

        else:
            raise CommandError("Commands are: 'clear' or 'reload'")
