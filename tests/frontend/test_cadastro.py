import re
import pytest
from playwright.sync_api import Page, expect
from pages.cadastro_page import CadastroPage
from utils.data_factory import gerar_usuario


@pytest.mark.frontend
class TestCadastro:
    def test_cadastro_usuario_valido(self, page: Page):
        usuario = gerar_usuario()
        cadastro = CadastroPage(page)
        cadastro.goto()
        cadastro.cadastrar(usuario["nome"], usuario["email"], usuario["password"])

        expect(page).to_have_url(re.compile(r".*/home"))

    def test_cadastro_email_ja_cadastrado(self, page: Page, api_context):
        # Pré-cria o usuário via API para não precisar de logout entre cadastros
        usuario = gerar_usuario()
        api_context.post("/usuarios", data=usuario)

        cadastro = CadastroPage(page)
        cadastro.goto()
        cadastro.cadastrar(usuario["nome"], usuario["email"], usuario["password"])

        expect(page.get_by_text("Este email já está sendo usado")).to_be_visible()

    def test_cadastro_campos_obrigatorios(self, page: Page):
        cadastro = CadastroPage(page)
        cadastro.goto()
        cadastro.cadastrar_button.click()

        expect(page.get_by_text("Nome é obrigatório")).to_be_visible()
        expect(page.get_by_text("Email é obrigatório")).to_be_visible()
        expect(page.get_by_text("Password é obrigatório")).to_be_visible()

    def test_cadastro_com_perfil_admin(self, page: Page):
        usuario = gerar_usuario()
        cadastro = CadastroPage(page)
        cadastro.goto()
        cadastro.cadastrar(usuario["nome"], usuario["email"], usuario["password"], admin=True)

        expect(page).to_have_url(re.compile(r".*/home"))
