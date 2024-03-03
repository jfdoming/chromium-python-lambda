import json
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
        if len(sys.argv) < 2:
            with open("config.json", "r") as config:
                return cls(**json.load(config))
        else:
            return cls(**json.loads(sys.argv[1]))
