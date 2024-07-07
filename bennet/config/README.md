# Config Package

## Overview

The `bennet.config` package provides a class for managing application configurations using a configuration file. It supports loading, saving, retrieving, and modifying settings and includes observer pattern support for handling configuration changes.

## Features

- Load and save configurations from/to a file.
- Retrieve and modify configuration settings.
- Add and remove sections and settings.
- Notify observers about configuration changes.
- Support dynamic attribute access for configuration settings.

## Installation

Ensure your project directory structure matches the following:

```
config/
├── bennet/
│   └── config/
│       ├── config.py
│       ├── __init__.py
```

Then, you can import the package in your Python code.

## Usage

### Initialization

To use the `Config` class, you need to create an instance of it by providing the path to the configuration file and an optional `Observable` instance for event handling.

```python
from bennet.config import Config
from bennet.observer import Observable

config = Config('config.ini', observable=Observable())
```

### Setting and Getting Values

You can set and get configuration values using the `set` and `get` methods.

```python
# Set a configuration value
config.set('section', 'key', 'value')

# Get a configuration value
value = config.get('section', 'key', fallback='default_value')
```

### Removing Settings or Sections

You can remove a specific setting or an entire section.

```python
# Remove a specific setting
config.remove('section', 'key')

# Remove an entire section
config.remove('section')
```

### Saving and Loading Configuration

You can load the configuration from a file and save it back to the file.

```python
# Load configuration from file
config.load()

# Save configuration to file
config.save()
```

### Dynamic Attribute Access

The `Config` class supports dynamic attribute access for configuration settings, allowing you to access and set settings using attribute-like syntax.

```python
# Set a configuration value
config.section_key = 'value'

# Get a configuration value
value = config.section_key
```

#### Example

Here is an example of how to use the `Config` class:

```python
from bennet.config import Config
from bennet.observer import Observable

# Create a Config instance
config = Config('config.ini', observable=Observable())

# Set a configuration value
config.set('section', 'key', 'value')

# Get a configuration value
value = config.get('section', 'key', fallback='default_value')

# Remove a configuration key
config.remove('section', 'key')

# Save the configuration to a file
config.save()

# Load the configuration from a file
config.load()

# Convert the configuration to a dictionary
config_dict = config.to_dict()
```

## API Reference

### Config

The `Config` class provides methods for managing configuration settings in a configuration file. It supports adding, removing, and notifying observers about changes to the configuration.

#### Initialization

```python
def __init__(self, filename=None, observable: Observable = None):
    """
    Initialize the Config object with a configuration file.

    :param filename: Path to the configuration file.
    :param observable: An instance of Observable for event handling.
    """
```

#### Methods

- **get(section, key, fallback=None)**

  ```python
  def get(self, section, key, fallback=None):
      """
      Get the value of a setting.

      :param section: The section of the setting.
      :param key: The key of the setting.
      :param fallback: The fallback value if the setting is not found.
      :return: The value of the setting, the default value or the fallback value in this order.
      """
  ```

- **set(section, key, value)**

  ```python
  def set(self, section, key, value):
      """
      Set the value of a setting.

      :param section: The section of the setting.
      :param key: The key of the setting.
      :param value: The value to set.
      """
  ```

- **remove(section, key=None)**

  ```python
  def remove(self, section, key=None):
      """
      Remove an option or an entire section.

      :param section: The section of the setting.
      :param key: The key of the setting to remove. If None, the entire section is removed.
      :return: True if the option or section was removed, False otherwise.
      """
  ```

- **load()**

  ```python
  def load(self):
      """Load configuration from the configuration file."""
  ```

- **save()**

  ```python
  def save(self):
      """Save configuration to the configuration file."""
  ```

- **to_dict()**

  ```python
  def to_dict(self, section=None):
      """
      Convert the entire configuration to a list of dictionaries.

      :return: A list of dictionaries, each representing a section and its key-value pairs.
      """
  ```

- **get_default(key, fallback=None)**

  ```python
  def get_default(self, key, fallback=None):
      """
      Get the value of a setting from the default section.

      :param key: The key of the setting.
      :param fallback: The default value if the setting is not found.
      :return: The value of the setting from the default section or the fallback value.
      """
  ```

- **set_default(key, value)**

  ```python
  def set_default(self, key, value):
      """
      Set the value of a setting in the default section.

      :param key: The key of the setting.
      :param value: The value to set.
      """
  ```

- **on_change(section, key, value)**

  ```python
  def on_change(self, section, key, value):
      """
      Hook for handling setting changes.

      This method can be overridden by subclasses to perform actions when a setting changes.

      :param section: The section of the setting.
      :param key: The key of the setting.
      :param value: The new value of the setting.
      """
  ```

- **on_remove(section, key)**

  ```python
  def on_remove(self, section, key):
      """
      Hook for handling setting or section removals.
  
      This method can be overridden by subclasses to perform actions when a setting or section is removed.
  
      :param section: The section of the setting.
      :param key: The key of the setting that was removed, or None if a section was removed.
      """
  ```

#### Properties

- **filename**

  ```python
  @property
  def filename(self):
      """The filename of the configuration file."""
  ```

- **config**

  ```python
  @property
  def config(self):
      """The configparser.ConfigParser instance."""
  ```

- **observable**

  ```python
  @property
  def observable(self):
      """The Observable instance for event handling."""
  ```

#### Dynamic Attribute Access

The `Config` class supports dynamic attribute access for configuration settings. This allows accessing and setting configuration values using attribute-like syntax.

- **__getattr__(name)**

  ```python
  def __getattr__(self, name):
      """
      Dynamic attribute access for config.

      :param name: The attribute name, formatted as section_key.
      :return: The value of the setting.
      """
  ```

- **__setattr__(name, value)**

  ```python
  def __setattr__(self, name, value):
      """
      Dynamic attribute setting for config.
  
      :param name: The attribute name, formatted as section_key.
      :param value: The value to set.
      """
  ```

## Logging

The `Config` class uses Python's built-in logging module to log important events (load, save, set, and remove). To view these logs, configure the logging level and handler in your main application.

```python
import logging

logging.basicConfig(level=logging.INFO)
```

## Observer Pattern

The `Config` class supports the observer pattern for event handling. You need to pass an instance of the `Observable` class from the `bennet.observer` package to the `Config` class to add, remove, and notify observers about changes to the configuration.

### Example

```python
from bennet.config import Config
from bennet.observer import Observable

class CustomObservable(Observable):
    def notify(self, event, section, key, value):
        print(f"Event: {event}, Section: {section}, Key: {key}, Value: {value}")

observable = CustomObservable()
config = Config('config.ini', observable=observable)

# Add an observer
observable.add_observer(lambda event, section, key, value: print(f"Observer notified of {event} in [{section}] {key} = {value}"))

# Change a setting to trigger the observer
config.set('section', 'key', 'new_value')
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

For more information, visit [bennet.hu](https://bennet.hu).