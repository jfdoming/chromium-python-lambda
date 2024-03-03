from tempfile import mkdtemp
from typing import Any, Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from scrape.interface import Interface
from scrape.interface.interface import SelectOptions


class SeleniumInterface(Interface):
    def __get_options(self):
        return {
            "headless": "new",
            "no-sandbox": True,
            "no-zygote": True,
            "single-process": True,
            "disable-dev-shm-usage": True,
            "disable-dev-tools": True,
            "disable-gpu": True,
            "disable-software-rasterizer": True,
            "remote-debugging-port": 9222,
            "window-size": "1920,1080",
            "user-data-dir": mkdtemp(),
            "data-path": mkdtemp(),
            "disk-cache-dir": mkdtemp(),
            "user-agent": " ".join(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "AppleWebKit/537.36 (KHTML, like Gecko)",
                    "Chrome/79.0.3945.79 Safari/537.36",
                ]
            ),
        }

    @staticmethod
    def __create_options(options_dict: dict[str, Any]):
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/bin/chromium"
        options.capabilities
        for key, value in options_dict.items():
            if isinstance(value, bool):
                if value:
                    options.add_argument(f"--{key}")
            else:
                options.add_argument(f"--{key}={value}")

        return options

    def __init__(self, timeout: int | None = None):
        super().__init__(timeout=timeout)

        self.__options = SeleniumInterface.__create_options(
            self.__get_options()
        )
        self.__service = webdriver.chrome.service.Service(
            executable_path="/opt/bin/chromedriver",
        )
        self.__driver = None

    def __enter__(self):
        self.__driver = webdriver.Chrome(
            options=self.__options,
            service=self.__service,
        )
        return self

    def __exit__(self, *_):
        self.__driver.quit()

    @property
    def url(self):
        return self.__driver.current_url

    @url.setter
    def url(self, url: str):
        self.__driver.get(url)

    def __call_with_timeout(
        self,
        method: Callable,
        timeout: int | None,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ):
        if timeout is not None:
            wait = WebDriverWait(self.__driver, timeout)
            try:
                return wait.until(lambda _: method(*args, **kwargs))
            except Exception:
                return None
        return method(*args, **kwargs)

    def _by_id(self, id: str, timeout: int | None) -> WebElement | None:
        return self.__call_with_timeout(
            self.__driver.find_element, timeout, By.ID, id
        )

    def _by_query(
        self,
        query: str,
        timeout: int | None,
    ) -> list[WebElement]:
        return self.__call_with_timeout(
            self.__driver.find_elements, timeout, By.CSS_SELECTOR, query
        )

    def _by_text(
        self, els: list[WebElement], text: str, _: int | None
    ) -> list[WebElement]:
        return [el for el in els if el.text == text]

    def click(self, **kwargs: SelectOptions):
        el = self._select_for_action(**kwargs)
        el.click()
        return el

    def type(self, text: str, **kwargs: SelectOptions):
        el = self._select_for_action(**kwargs)
        el.send_keys(text)
        return el

    def screenshot(self, path: str = "/var/task/scrape/screenshot.png"):
        self.__driver.save_screenshot(path)
