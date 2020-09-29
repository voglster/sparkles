"""Provide a custom uvicorn worker that can be configured."""
from starlette.config import Config
from uvicorn.workers import UvicornWorker


config = Config()


class ConfigurableWorker(UvicornWorker):
    #: dict: Set the equivalent of uvicorn command line options as keys.
    CONFIG_KWARGS = {
        "root_path": config("SCRIPT_NAME", default=""),
        "proxy_headers": True,
    }
