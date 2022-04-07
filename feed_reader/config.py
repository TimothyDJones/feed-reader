import yaml

YAML_FILE = "config.yaml"

class Config(object):
    def __init__(self, config_file=YAML_FILE):
        self.config_file = config_file

        self.config = None

    def get_config(self):
        with open(self.config_file, "r") as file:
            self.config = yaml.safe_load(file)

        return (self.config)