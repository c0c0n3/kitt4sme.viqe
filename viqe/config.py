from fipy.cfg.reader import YamlReader
from pydantic import AnyHttpUrl, BaseSettings
from uri import URI


CONFIG_FILE_ENV_VAR_NAME = 'VIQE_CONFIG'


class Settings(BaseSettings):
    quantumleap_base_url: AnyHttpUrl = 'http://quantumleap:8668'

    @staticmethod
    def load() -> 'Settings':
        reader = YamlReader()
        raw_settings = reader.from_env_file(
            env_var_name=CONFIG_FILE_ENV_VAR_NAME, defaults={})
        if raw_settings:
            return Settings(**raw_settings)
        return Settings()


def viqe_config() -> Settings:
    return Settings.load()


def to_uri(url: AnyHttpUrl) -> URI:
    return URI(f"{url}")
