import base64
import json
import os
import sys
from functools import cache
from typing import Annotated

from pydantic import BaseModel, ConfigDict, NonNegativeInt, Strict


class BaseConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    verbosity: Annotated[NonNegativeInt, Strict] = 1

    @classmethod
    @cache
    def get(cls):
        if "SCRAPER_CONFIG" in os.environ:
            return cls(
                **json.loads(
                    base64.b64decode(os.environ["SCRAPER_CONFIG"]).decode(
                        "utf-8"
                    )
                )
            )

        if len(sys.argv) >= 2:
            is_payload_config_enabled = (
                os.environ.get("ENABLE_PAYLOAD_CONFIG", "false").lower()
                == "true"
            )
            assert is_payload_config_enabled, (
                "Payload-based configuration is disabled by default to "
                "prevent abuse of compute resources. If you are a developer, "
                "you can enable this feature by setting the environment "
                "variable `ENABLE_PAYLOAD_CONFIG` to the string `true`. "
                "Please note that this feature is not intended for use in "
                "production environments; you should use environment "
                "variables or a configuration file instead."
            )

            return cls(**json.loads(sys.argv[1]))
        with open("config.json", "r") as config:
            return cls(**json.load(config))
