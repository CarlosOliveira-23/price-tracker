import yaml


class Config:
    def __init__(self, config_file="config.yml"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Loads the configuration file."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("⚠️ Config file not found. Using default values.")
            return {}

    def get(self, key, default=None):
        """Gets a configuration value."""
        return self.config.get(key, default)
