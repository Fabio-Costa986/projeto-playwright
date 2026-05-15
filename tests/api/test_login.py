import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
class TestLogin:
    def test_login_com_credenciais_validas(self, api_context: APIRequestContext):
        response = api_context.post("/login", data={
            "email": "fulano@qa.com",
            "password": "teste",
        })

        assert response.status == 200
        body = response.json()
        assert "authorization" in body
        assert body["authorization"].startswith("Bearer ")

    def test_login_email_invalido(self, api_context: APIRequestContext):
        response = api_context.post("/login", data={
            "email": "naoexiste@teste.com",
            "password": "senha123",
        })

        assert response.status == 401
        body = response.json()
        assert "message" in body

    def test_login_senha_invalida(self, api_context: APIRequestContext):
        response = api_context.post("/login", data={
            "email": "fulano@qa.com",
            "password": "senhaerrada",
        })

        assert response.status == 401

    def test_login_campos_obrigatorios(self, api_context: APIRequestContext):
        response = api_context.post("/login", data={})

        assert response.status == 400
        body = response.json()
        assert "email" in body or "password" in body
