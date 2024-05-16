from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="STRATA_FIT_VAL",
    settings_files=["settings.yaml"],
    merge_enabled=True,
)