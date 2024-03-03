from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, overload

ElementType = TypeVar("ElementType")


class Interface(ABC, Generic[ElementType]):
    @staticmethod
    def create(engine: str, *args: Any, **kwargs: Any):
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
    def url(self) -> str:
        pass

    @url.setter
    @abstractmethod
    def url(self, url: str) -> str:
        pass

    @abstractmethod
    def _by_id(self, id: str, timeout: int | None) -> ElementType | None:
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
        self, els: list[ElementType], text: str, timeout: int | None
    ) -> list[ElementType]:
        pass

    @abstractmethod
    def _click(self, el: ElementType) -> ElementType:
        pass

    @overload
    def click(
        self, *, id: str, timeout: int | None = None, text: str | None = None
    ) -> ElementType: ...

    @overload
    def click(
        self,
        *,
        query: str,
        index: int | None = None,
        timeout: int | None = None,
        text: str | None = None,
    ) -> ElementType: ...

    def click(
        self,
        id: str | None = None,
        query: str | None = None,
        index: int | None = None,
        text: str | None = None,
        timeout: int | None = None,
    ) -> ElementType:
        if id is not None:
            el = self._select_for_action(id=id, text=text, timeout=timeout)
        elif query is not None:
            el = self._select_for_action(
                query=query, index=index, text=text, timeout=timeout
            )
        else:
            raise ValueError("No selector specified")

        return self._click(el)

    @abstractmethod
    def _type(self, el: ElementType, text: str) -> ElementType:
        pass

    @overload
    def type(
        self, text: str, *, id: str, timeout: int | None = None
    ) -> ElementType: ...

    @overload
    def type(
        self,
        text: str,
        *,
        query: str,
        index: int | None = None,
        timeout: int | None = None,
    ) -> ElementType: ...

    def type(
        self,
        text: str,
        id: str | None = None,
        query: str | None = None,
        index: int | None = None,
        timeout: int | None = None,
    ) -> ElementType:
        if id is not None:
            el = self._select_for_action(id=id, timeout=timeout, text=None)
        elif query is not None:
            el = self._select_for_action(
                query=query, index=index, timeout=timeout, text=None
            )
        else:
            raise ValueError("No selector specified")

        return self._type(el, text)

    @abstractmethod
    def screenshot(self, path: str | None = None) -> None:
        pass

    @overload
    def select(
        self, *, id: str, timeout: int | None = None, text: str | None = None
    ) -> ElementType | None: ...

    @overload
    def select(
        self,
        *,
        query: str,
        timeout: int | None = None,
        text: str | None = None,
    ) -> list[ElementType]: ...

    @overload
    def select(
        self,
        *,
        query: str,
        index: int,
        timeout: int | None = None,
        text: str | None = None,
    ) -> ElementType | None: ...

    def select(
        self,
        id: str | None = None,
        query: str | None = None,
        index: int | None = None,
        text: str | None = None,
        timeout: int | None = None,
    ) -> ElementType | list[ElementType] | None:
        if id is not None:
            el = self._by_id(id=id, timeout=timeout)
            if el and text is not None:
                els = self._by_text([el], text=text, timeout=timeout)
                return els[0] if els else None
            return el
        if query is not None:
            els = self._by_query(query=query, timeout=timeout)
            if text is not None:
                els = self._by_text(els, text=text, timeout=timeout)
            if index is not None:
                return els[index] if len(els) > index else None
            return els
        raise ValueError("No selector specified")

    @overload
    def _select_for_action(
        self, *, id: str, timeout: int | None = None, text: str | None = None
    ) -> ElementType: ...

    @overload
    def _select_for_action(
        self,
        *,
        query: str,
        index: int | None = None,
        timeout: int | None = None,
        text: str | None = None,
    ) -> ElementType: ...

    def _select_for_action(
        self,
        id: str | None = None,
        query: str | None = None,
        index: int | None = None,
        text: str | None = None,
        timeout: int | None = None,
    ) -> ElementType:
        if id is not None:
            el = self.select(id=id, text=text, timeout=timeout)
        elif query is not None:
            if index is None:
                els = self.select(query=query, text=text, timeout=timeout)
                if len(els) != 1:
                    raise ValueError(
                        "Ambiguous element selection, please specify an index"
                    )
                el = els[0]
            else:
                el = self.select(
                    query=query, index=index, text=text, timeout=timeout
                )
        else:
            raise ValueError("No selector specified")

        assert el is not None, "Element not found"
        return el
