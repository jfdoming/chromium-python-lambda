from tempfile import mkdtemp
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from scrape.interface import Interface


class SeleniumInterface(Interface[WebElement]):
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
        options = Options()
        options.binary_location = "/opt/bin/chromium"
        for key, value in options_dict.items():
            if isinstance(value, bool):
                if value:
                    options.add_argument(  # pyright: ignore [reportUnknownMemberType] # noqa: E501
                        f"--{key}"
                    )
            else:
                options.add_argument(  # pyright: ignore [reportUnknownMemberType] # noqa: E501
                    f"--{key}={value}"
                )

        return options

    def __init__(self, timeout: int | None = None):
        super().__init__(timeout=timeout)

        self.__options = SeleniumInterface.__create_options(
            self.__get_options()
        )
        self.__service = Service(
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
        if self.__driver is not None:
            self.__driver.quit()
            self.__driver = None

    @property
    def url(self):
        if self.__driver is None:
            return ""
        return self.__driver.current_url

    @url.setter
    def url(self, url: str):
        assert self.__driver is not None, "Driver is not initialized"

        self.__driver.get(url)
        return self.__driver.current_url

    def _by_id(self, id: str, timeout: int | None) -> WebElement | None:
        assert self.__driver is not None, "Driver is not initialized"
        if timeout is None:
            return self.__driver.find_element(By.ID, id)

        wait = WebDriverWait(self.__driver, timeout)
        try:
            return wait.until(lambda driver: driver.find_element(By.ID, id))
        except Exception:
            return None

    def _by_query(
        self,
        query: str,
        timeout: int | None,
    ) -> list[WebElement]:
        assert self.__driver is not None, "Driver is not initialized"
        if timeout is None:
            return self.__driver.find_elements(By.CSS_SELECTOR, query)

        wait = WebDriverWait(self.__driver, timeout)
        try:
            return wait.until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, query)
            )
        except Exception:
            return []

    def _by_text(
        self, els: list[WebElement], text: str, timeout: int | None
    ) -> list[WebElement]:
        return [el for el in els if el.text == text]

    def _click(
        self,
        el: WebElement,
    ) -> WebElement:
        el.click()
        return el

    def _type(self, el: WebElement, text: str) -> WebElement:
        el.send_keys(  # pyright: ignore [reportUnknownMemberType] # noqa: E501
            text
        )
        return el

    def screenshot(self, path: str | None = "/var/task/scrape/screenshot.png"):
        assert self.__driver is not None, "Driver is not initialized"
        if path is None:
            path = "/var/task/scrape/screenshot.png"
        self.__driver.save_screenshot(  # pyright: ignore [reportUnknownMemberType] # noqa: E501
            path
        )

    def switch_to_frame(self, selector: str | int):
        assert self.__driver is not None, "Driver is not initialized"
        self.__driver.switch_to.frame(selector)
