from enum import Enum

class AppEnvironment(str, Enum):
    local = "local"
    test = "test"
    staging = "staging"
    production = "production"

    @classmethod
    def is_local_env(cls, env) -> bool:
        return env == cls.local.value or env == cls.local

    @classmethod
    def is_test_env(cls, env) -> bool:
        return env == cls.test.value or env == cls.test

    @classmethod
    def is_remote_env(cls, env) -> bool:
        return env in [cls.staging.value, cls.production.value, cls.staging, cls.production]

    @classmethod
    def is_production_env(cls, env) -> bool:
        return env == cls.production.value or env == cls.production