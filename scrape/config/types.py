from typing import Annotated

from pydantic import SecretStr, StringConstraints

StrippedStr = Annotated[str, StringConstraints(strip_whitespace=True)]


class StrippedSecretStr(SecretStr):
    def __init__(self, secret_value: str):
        super().__init__(secret_value=secret_value)
        self._secret_value = self._secret_value.strip()
