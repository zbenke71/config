import configparser
import logging
from bennet.observer import Observable

logger = logging.getLogger(__name__)


class Config:
    """
    A class to manage application config using a configuration file.

    The Config class provides methods to load, save, retrieve, and modify
    application config stored in a configuration file. It supports adding,
    removing, and notifying observers about changes to the config, making it
    suitable for applications following the MVC pattern.

    https://bennet.hu
    """

    def __init__(self, filename, observable: Observable = None):
        """
        Initialize the Config object with a configuration file.

        :param filename: Path to the configuration file.
        :param observable: An instance of Observable for event handling.
        """
        if observable is not None and not isinstance(observable, Observable):
            raise TypeError("observable must be an instance of Observable")        
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.observable = observable or Observable()
        self.load()

    def get(self, section, key, fallback=None):
        """
        Get the value of a setting.

        :param section: The section of the setting.
        :param key: The key of the setting.
        :param fallback: The fallback value if the setting is not found.
        :return: The value of the setting, the default value or the fallback value in this order.
        """
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            logger.warning(f"Setting not found: [{section}] {key}, returning fallback: {fallback}")
            return fallback

    def set(self, section, key, value):
        """
        Set the value of a setting.

        :param section: The section of the setting.
        :param key: The key of the setting.
        :param value: The value to set.
        """
        if not self.config.has_section(section) and section != configparser.DEFAULTSECT:
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.observable.trigger_event("setting_changed", section, key, value)
        logger.info(f"Setting changed: [{section}] {key} = {value}")
        return self

    def remove(self, section, key=None):
        """
        Remove an option or an entire section.

        :param section: The section of the setting.
        :param key: The key of the setting to remove. If None, the entire section is removed.
        :return: True if the option or section was removed, False otherwise.
        """
        try:
            if key is None:
                if self.config.has_section(section):
                    self.config.remove_section(section)
                    self.observable.trigger_event("setting_removed", section, key)
                    logger.info(f"Removed section: [{section}]")
                    return True
                else:
                    logger.warning(f"Section not found: [{section}]")
            else:
                if self.config.has_option(section, key):
                    self.config.remove_option(section, key)
                    self.observable.trigger_event("setting_removed", section, key)
                    logger.info(f"Removed setting: [{section}] {key}")
                    return True
                else:
                    logger.warning(f"Option not found: [{section}] {key}")
            return False
        except configparser.ParsingError as e:
            logger.error(f"ConfigParser error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

    def load(self):
        """Load configuration from the configuration file."""
        try:
            self.config.read(self.filename)
            logger.info(f"Settings loaded from {self.filename}")
        except (configparser.MissingSectionHeaderError, configparser.ParsingError) as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def save(self):
        """Save configuration to the configuration file."""
        try:
            with open(self.filename, 'w') as configfile:
                self.config.write(configfile)
            logger.info(f"Settings saved to {self.filename}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            raise

    def to_dict(self, section=None):
        """
        Convert the entire configuration to a list of dictionaries.

        :return: A list of dictionaries, each representing a section and its key-value pairs.
        """
        config_data = {}
        for isection in self.config.sections():
            section_data = {key: self.config.get(isection, key) for key in self.config.options(isection)}
            config_data.update({isection: section_data})
        return config_data.get(section) if section is not None else config_data

    def get_default(self, key, fallback=None):
        """
        Get the value of a setting from the default section.

        :param key: The key of the setting.
        :param fallback: The default value if the setting is not found.
        :return: The value of the setting from the default section or the fallback value.
        """
        return self.get(configparser.DEFAULTSECT, key, fallback)

    def set_default(self, key, value):
        """
        Set the value of a setting in the default section.

        :param key: The key of the setting.
        :param value: The value to set.
        """
        self.set(configparser.DEFAULTSECT, key, value)

    def __getattr__(self, name):
        """
        Dynamic attribute access for config.

        :param name: The attribute name, formatted as section_key.
        :return: The value of the setting.
        """
        section, key = name.split('_', 1)
        try:
            return self.get(section, key)
        except ValueError:
            raise AttributeError(f"'Settings' object has no attribute '{name}'")
        except configparser.NoOptionError:
            raise AttributeError(f"Setting '{section}.{key}' not found")

    def __setattr__(self, name, value):
        """
        Dynamic attribute setting for config.

        :param name: The attribute name, formatted as section_key.
        :param value: The value to set.
        """
        if name in ('filename', 'config', 'observable'):
            super().__setattr__(name, value)
        else:
            try:
                section, key = name.split('_', 1)
                self.set(section, key, value)
            except ValueError:
                super().__setattr__(name, value)

    def on_change(self, section, key, value):
        """
        Hook for handling setting changes.

        This method can be overridden by subclasses to perform actions when a setting changes.

        :param section: The section of the setting.
        :param key: The key of the setting.
        :param value: The new value of the setting.
        """
        pass

    def on_remove(self, section, key):
        """
        Hook for handling setting or section removals.

        This method can be overridden by subclasses to perform actions when a setting or section is removed.

        :param section: The section of the setting.
        :param key: The key of the setting that was removed, or None if a section was removed.
        """
        pass


if __name__ == "__main__":
    config = Config('example.ini')
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s - %(message)s")
    print(config.config)
    print(config.config.defaults())
    print(config.config.sections())

    print(config.get('oracle', 'user'))
    print(config.get('oracle', 'session', 'no session'))

    common = config.config['common']
    print(common.get('usr', 'usr fallback'))

    print(config.get('common', 'something'))
    config.set('common', 'time', 'no').save()
    # print(config.get_default('compressionlevel'))
    # print(config.get('topsecret', 'pass', 'NA'))
    print("oracle_user --> __getattr__(oracle, user): ", config.oracle_user)
    print("DEFAULT_postal_code --> __getattr__(DEFAULT, postal_code): ", config.DEFAULT_postal_code)
    config.DEFAULT_postal_code = '3300'
    # config.remove('extra')
    config.set_default('system', 'Linux Mint 20.1')
    config.save()
    print(config.config.__dir__())
    print(config.__dir__())
    print(config.__dict__)
    print(config.to_dict())
