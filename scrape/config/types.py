from typing import Annotated

from pydantic import SecretStr, StringConstraints

StrippedStr = Annotated[str, StringConstraints(strip_whitespace=True)]


class StrippedSecretStr(SecretStr):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._secret_value = self._secret_value.strip()
