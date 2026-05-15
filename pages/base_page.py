import logging
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger(self.__class__.__name__)

    def goto(self, path: str = ""):
        self.log.info("Navegando para: %s", path)
        self.page.goto(path)
        self.log.debug("URL atual: %s", self.page.url)

    def wait_for_url(self, pattern: str):
        self.page.wait_for_url(f"**{pattern}**")

    def get_toast_message(self) -> str:
        toast = self.page.locator(".toast-message, .alert, [role='alert']").first
        toast.wait_for(state="visible", timeout=5000)
        msg = toast.inner_text()
        self.log.info("Toast exibido: %s", msg)
        return msg
