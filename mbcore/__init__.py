import sys, os
from path import path


def wrap_path(possible_path):
    if not isinstance(possible_path, path):
        possible_path = path(possible_path)
    return possible_path

def require_configured(fn):
    def real_fn(*args, **kwargs):
        if not conf.is_configured():
            raise Exception("Call conf.configure() first.")
        return fn(*args, **kwargs)

    return real_fn

class Configuration(object):

    def __init__(self):
        self.PROJECT_ROOT = None
        self.DJANGO_PROJECT_NAME = None
        self.SITE_ROOT = None
        self.debug = False

    def is_configured(self):
        return self.PROJECT_ROOT is not None

    def configure(self, project_root, django_project_name, debug=False):
        """
        project_root is a path to the top level project folder.
        django_project_name is the name of the folder where manage.py lives.
        """
        if self.is_configured():
            return

        self.debug = debug
        self.PROJECT_ROOT = wrap_path(project_root).abspath().realpath()
        self.SITE_ROOT = self.PROJECT_ROOT / django_project_name
        self.DJANGO_PROJECT_NAME = django_project_name

        sys.path.append(self.PROJECT_ROOT)

        if self.debug:
            print "MB-Core Configured..."
            print "PROJECT_ROOT: %s" % self.PROJECT_ROOT
            print "SITE_ROOT: %s" % self.SITE_ROOT
            print "DJANGO_PROJECT_NAME: %s" % self.DJANGO_PROJECT_NAME


    def load_env(self, default_settings_module=None):
        if not self.is_configured():
            raise Exception("Call conf.configure() first.")

        # Load the .env file
        from mbcore import env_file
        env_file.load(self.PROJECT_ROOT / '.env')

        if default_settings_module is not None:
            # If that didn't set the settings module...
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings_module)

        if self.debug:
            print "MB-Core .env loaded"
            print "Django Settings Module: %s" % os.environ.get('DJANGO_SETTINGS_MODULE')

conf = Configuration()


def get_env_setting(setting, default=None, type=None):
    """ Get the environment setting or return exception """
    if default is not None:
        v = os.environ.get(setting, default)
    else:
        try:
            v =os.environ[setting]
        except KeyError:
            error_msg = "Set the %s env variable" % setting
            raise ImproperlyConfigured(error_msg)

    if type is None:
        return v

    elif type is bool:
        # check for falsey values
        return v not in (0, '0', None, '')

    else:
        # just cast it
        return type(v)