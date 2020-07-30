from dotenv import load_dotenv

load_dotenv()

from os import getenv


def smart_bool(val: str) -> bool:
    if val.strip().lower() in ["true", "yes", "1"]:
        return True
    if val.strip().lower() in ["false", "no", "0", ""]:
        return False
    raise ValueError(f"Config value of {val} could not be coerced into bool")


class BaseConfig:
    def __init__(self):
        for env_variable, value_class in self.__class__.__dict__[
            "__annotations__"
        ].items():
            env_value = getenv(env_variable.upper())
            if env_value:
                parsed_value = value_class(env_value)
            else:
                parsed_value = getattr(self, env_variable)
            setattr(self, env_variable, parsed_value)


def write_env(config):
    with open(".env", "w") as f:
        for env_var in config.__class__.__dict__["__annotations__"]:
            val = getattr(config, env_var)
            f.write(f"{env_var.upper()}={val}\n")
