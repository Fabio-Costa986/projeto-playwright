from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "/admin/home"

    def __init__(self, page: Page):
        super().__init__(page)
        self.sair_button = page.get_by_test_id("logout")
        self.cadastrar_produto_link = page.get_by_test_id("cadastrarProdutos")
        self.listar_produtos_link = page.get_by_test_id("listarProdutos")

    def goto(self):
        self.log.info("Abrindo home do administrador")
        self.page.goto(self.URL)

    def sair(self):
        self.log.info("Realizando logout")
        self.sair_button.click()

    def ir_para_listar_produtos(self):
        self.log.info("Navegando para listagem de produtos")
        self.listar_produtos_link.click()

    def ir_para_cadastrar_produto(self):
        self.log.info("Navegando para cadastro de produto")
        self.cadastrar_produto_link.click()
