"""Kernel Builder main application entry point."""

from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults
from cement.core.exc import FrameworkError, CaughtSignal
from kbuilder.core import exc
from kbuilder.cli.config_parser import parse_android_kernel_config

# Application default.  Should update config/kbuilder.conf to reflect any
# changes, or additions here.
defaults = init_defaults('kbuilder')

# All internal/external plugin configurations are loaded from here
defaults['kbuilder']['plugin_config_dir'] = '/etc/kbuilder/plugins.d'

# External plugins (generally, do not ship with application code)
defaults['kbuilder']['plugin_dir'] = '/var/lib/kbuilder/plugins'

# External templates (generally, do not ship with application code)
defaults['kbuilder']['template_dir'] = '/var/lib/kbuilder/templates'


class KbuilderApp(CementApp):
    class Meta:
        label = 'kbuilder'
        config_defaults = defaults

        # All built-in application bootstrapping (always run)
        bootstrap = 'kbuilder.cli.bootstrap'

        # Internal plugins (ship with application code)
        plugin_bootstrap = 'kbuilder.cli.plugins'

        # Internal templates (ship with application code)
        template_module = 'kbuilder.cli.templates'


class KbuilderTestApp(KbuilderApp):

    """A test app that is better suited for testing."""
    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


# Define the applicaiton object outside of main, as some libraries might wish
# to import it as a global (rather than passing it into another class/func)
app = KbuilderApp()


def main():
    with app:
        try:
            app.hook.register('pre_run', parse_android_kernel_config)
            app.run()

        except exc.KbuilderError as e:
            # Catch our application errors and exit 1 (error)
            print('KbuilderError > %s' % e)
            app.exit_code = 1

        except FrameworkError as e:
            # Catch framework errors and exit 1 (error)
            print('FrameworkError > %s' % e)
            app.exit_code = 1

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('CaughtSignal > %s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
