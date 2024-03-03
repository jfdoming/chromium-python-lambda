from abc import ABC, abstractmethod
from typing import Any, TypedDict


class SelectOptions(TypedDict):
    id: str | None
    query: str | None
    index: int | None
    text: str | None
    timeout: int | None


class Interface(ABC):
    @staticmethod
    def create(engine: str, *args, **kwargs):
        if engine == "selenium":
            from scrape.interface.selenium import (
                SeleniumInterface as EngineInterface,
            )
        else:
            raise TypeError(f"'{engine}' is not a valid engine")

        return EngineInterface(*args, **kwargs)

    def __init__(self, timeout: int | None = None):
        self.timeout = timeout

    @property
    @abstractmethod
    def url(self, url: str) -> str:
        pass

    @abstractmethod
    def _by_id(self, id: str, timeout: int | None) -> Any | None:
        pass

    @abstractmethod
    def _by_query(
        self,
        query: str,
        timeout: int | None,
    ) -> list[Any]:
        pass

    @abstractmethod
    def _by_text(
        self, els: list[Any], text: str, timeout: int | None
    ) -> list[Any]:
        pass

    @abstractmethod
    def click(self, **kwargs: SelectOptions) -> Any | None:
        pass

    @abstractmethod
    def type(
        self,
        text: str,
        **kwargs: SelectOptions,
    ) -> Any | None:
        pass

    @abstractmethod
    def screenshot(self, path: str | None = None) -> None:
        pass

    def select(self, **kwargs: SelectOptions) -> Any | list[Any] | None:
        timeout = kwargs.pop("timeout", self.timeout)
        if "id" in kwargs:
            el = self._by_id(id=kwargs["id"], timeout=timeout)
            if el and "text" in kwargs:
                els = self._by_text([el], text=kwargs["text"], timeout=timeout)
                return els[0] if els else None
            return el
        if "query" in kwargs:
            els = self._by_query(query=kwargs["query"], timeout=timeout)
            if "text" in kwargs:
                els = self._by_text(els, text=kwargs["text"], timeout=timeout)
            if "index" in kwargs:
                return (
                    els[kwargs["index"]]
                    if len(els) > kwargs["index"]
                    else None
                )
            return els
        raise ValueError("No selector specified")

    def _select_for_action(self, **kwargs: SelectOptions):
        el = self.select(**kwargs)
        if isinstance(el, list):
            if len(el) != 1:
                raise ValueError(
                    "Ambiguous element selection, please specify an index"
                )
            el = el[0]
        return el
