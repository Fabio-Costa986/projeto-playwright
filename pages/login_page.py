from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("senha")
        self.submit_button = page.get_by_test_id("entrar")
        self.cadastrar_link = page.get_by_test_id("cadastrar")

    def goto(self):
        self.log.info("Abrindo página de login")
        self.page.goto(self.URL)

    def fazer_login(self, email: str, senha: str):
        self.log.info("Realizando login com: %s", email)
        self.email_input.fill(email)
        self.password_input.fill(senha)
        self.submit_button.click()
        self.log.debug("Botão 'Entrar' clicado")

    def ir_para_cadastro(self):
        self.log.info("Clicando no link de cadastro")
        self.cadastrar_link.click()
