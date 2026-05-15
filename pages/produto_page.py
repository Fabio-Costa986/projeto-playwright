from playwright.sync_api import Page
from pages.base_page import BasePage


class ProdutoPage(BasePage):
    URL = "/admin/cadastrarprodutos"

    def __init__(self, page: Page):
        super().__init__(page)
        self.nome_input = page.get_by_test_id("nome")
        self.preco_input = page.get_by_test_id("preco")
        self.descricao_input = page.get_by_test_id("descricao")
        self.quantidade_input = page.get_by_test_id("quantity")
        self.salvar_button = page.get_by_test_id("cadastarProdutos")

    def goto(self):
        self.log.info("Abrindo página de cadastro de produto")
        self.page.goto(self.URL)

    def cadastrar_produto(self, nome: str, preco: int, descricao: str, quantidade: int):
        self.log.info("Cadastrando produto: %s | preço: %s | qtd: %s", nome, preco, quantidade)
        self.nome_input.fill(nome)
        self.preco_input.fill(str(preco))
        self.descricao_input.fill(descricao)
        self.quantidade_input.fill(str(quantidade))
        self.log.debug("Clicando em salvar produto")
        self.salvar_button.click()
