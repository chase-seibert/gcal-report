import ConfigParser
import os


_CONFIG_PATH = os.path.expanduser('~/.gcal-report')


class Settings(object):

    def __init__(self, path=None):
        self.config = ConfigParser.SafeConfigParser()
        self.path = path or _CONFIG_PATH
        if os.path.exists(self.path):
            self.config.read(self.path)

    def get(self, section, setting):
        return self.config.get(section, setting)

    def has_section(self, section):
        return self.config.has_section(section)

    def update_all(self, config):
        self.config = config
        self.save()

    def update_section(self, section, dict):
        if not self.has_section(section):
            self.config.add_section(section)
        for key, value in dict.items():
            self.config.set(section, key, value)
        self.save()

    def save(self):
        with open(self.path, 'w') as f:
            self.config.write(f)

_settings = Settings()


def update(config):
    _settings.update_all(config)
    print 'Wrote %s' % _settings.path


def get_setting(section, setting):
    return _settings.get(section, setting)


def get_section_settings(section):
    pass


def has_section(section):
    return _settings.has_section(section)


def update_section(section, dict):
    _settings.update_section(section, dict)
