from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[".secrets.toml", "settings.toml"],
)
