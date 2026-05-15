from playwright.sync_api import Page
from pages.base_page import BasePage


class ListarProdutosPage(BasePage):
    URL = "/admin/listarprodutos"

    def __init__(self, page: Page):
        super().__init__(page)
        self.tabela_linhas = page.locator("table tbody tr")

    def goto(self):
        self.log.info("Abrindo listagem de produtos")
        self.page.goto(self.URL)

    def contar_produtos(self) -> int:
        total = self.tabela_linhas.count()
        self.log.info("Produtos encontrados na tabela: %d", total)
        return total
