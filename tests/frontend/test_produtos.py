import re
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.produto_page import ProdutoPage
from pages.listar_produtos_page import ListarProdutosPage
from utils.data_factory import gerar_produto


@pytest.mark.frontend
class TestProdutos:
    def test_listar_produtos_exibe_tabela(self, logged_page: Page):
        listar = ListarProdutosPage(logged_page)
        listar.goto()

        expect(listar.tabela_linhas.first).to_be_visible()

    def test_cadastrar_produto_como_admin(self, logged_page: Page):
        produto = gerar_produto()
        produto_page = ProdutoPage(logged_page)
        produto_page.goto()
        produto_page.cadastrar_produto(
            produto["nome"],
            produto["preco"],
            produto["descricao"],
            produto["quantidade"],
        )

        expect(logged_page).to_have_url(re.compile(r".*/listarprodutos"))

    def test_link_cadastrar_produto_visivel_no_home(self, logged_page: Page):
        home = HomePage(logged_page)
        home.goto()

        expect(home.cadastrar_produto_link).to_be_visible()

    def test_campos_obrigatorios_cadastro_produto(self, logged_page: Page):
        produto_page = ProdutoPage(logged_page)
        produto_page.goto()
        produto_page.salvar_button.click()

        expect(logged_page.get_by_text("Nome é obrigatório")).to_be_visible()
        expect(logged_page.get_by_text("Preco é obrigatório")).to_be_visible()
