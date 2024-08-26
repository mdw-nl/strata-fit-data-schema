from dynaconf import Dynaconf
import os

config_path = os.getenv("CONFIG_PATH", "config/")  # Default to config/ if not specified

settings = Dynaconf(
    envvar_prefix="STRATA_FIT_VAL",
    settings_files=[
        os.path.join(config_path, "settings.yaml"),
        os.path.join(config_path, "schema.yaml")
    ],
    merge_enabled=True,
)