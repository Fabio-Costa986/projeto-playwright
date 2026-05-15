from playwright.sync_api import Page
from pages.base_page import BasePage


class CadastroPage(BasePage):
    URL = "/cadastrarusuarios"

    def __init__(self, page: Page):
        super().__init__(page)
        self.nome_input = page.get_by_test_id("nome")
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.admin_checkbox = page.get_by_test_id("checkbox")
        self.cadastrar_button = page.get_by_test_id("cadastrar")

    def goto(self):
        self.log.info("Abrindo página de cadastro de usuário")
        self.page.goto(self.URL)

    def preencher_formulario(self, nome: str, email: str, senha: str, admin: bool = False):
        self.log.debug("Preenchendo formulário — nome: %s | email: %s | admin: %s", nome, email, admin)
        self.nome_input.fill(nome)
        self.email_input.fill(email)
        self.password_input.fill(senha)
        if admin:
            self.log.debug("Marcando checkbox de administrador")
            self.admin_checkbox.check()

    def cadastrar(self, nome: str, email: str, senha: str, admin: bool = False):
        self.preencher_formulario(nome, email, senha, admin)
        self.log.info("Submetendo cadastro de usuário: %s", email)
        self.cadastrar_button.click()
