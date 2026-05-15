import re
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.frontend
class TestLogin:
    def test_login_valido_redireciona_para_home(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.fazer_login("fulano@qa.com", "teste")

        expect(page).to_have_url(re.compile(r".*/admin/home"))

    def test_login_invalido_exibe_mensagem_erro(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.fazer_login("errado@teste.com", "senhaerrada")

        expect(page.get_by_text("Email e/ou senha inválidos")).to_be_visible()

    def test_login_campos_vazios_exibe_validacoes(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.submit_button.click()

        expect(page.get_by_text("Email é obrigatório")).to_be_visible()
        expect(page.get_by_text("Password é obrigatório")).to_be_visible()

    def test_logout_redireciona_para_login(self, logged_page: Page):
        home = HomePage(logged_page)
        home.sair()

        expect(logged_page).to_have_url(re.compile(r".*/login"))

    def test_link_cadastro_visivel_na_pagina_login(self, page: Page):
        login = LoginPage(page)
        login.goto()

        expect(login.cadastrar_link).to_be_visible()

    def test_link_cadastro_redireciona(self, page: Page):
        login = LoginPage(page)
        login.goto()
        login.ir_para_cadastro()

        expect(page).to_have_url(re.compile(r".*/cadastrarusuarios"))
