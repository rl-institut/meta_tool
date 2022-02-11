
import json
import environ

env = environ.Env()
CRAWLER_CONFIG = env.str("CRAWLER_CONFIG", "crawler_config.json")

with open(CRAWLER_CONFIG, "r") as configfile:
    config = json.load(configfile)
