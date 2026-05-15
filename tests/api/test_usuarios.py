import pytest
from playwright.sync_api import APIRequestContext
from utils.data_factory import gerar_usuario


@pytest.mark.api
class TestUsuarios:
    def test_listar_usuarios(self, api_context: APIRequestContext):
        response = api_context.get("/usuarios")

        assert response.status == 200
        body = response.json()
        assert "quantidade" in body
        assert "usuarios" in body
        assert isinstance(body["usuarios"], list)

    def test_criar_usuario(self, api_context: APIRequestContext):
        usuario = gerar_usuario()
        response = api_context.post("/usuarios", data=usuario)

        assert response.status == 201
        body = response.json()
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body

    def test_criar_usuario_email_duplicado(self, api_context: APIRequestContext):
        usuario = gerar_usuario()
        api_context.post("/usuarios", data=usuario)
        response = api_context.post("/usuarios", data=usuario)

        assert response.status == 400
        body = response.json()
        assert "email" in body["message"].lower() or "já" in body["message"]

    def test_buscar_usuario_por_id(self, api_context: APIRequestContext):
        usuario = gerar_usuario()
        criado = api_context.post("/usuarios", data=usuario)
        usuario_id = criado.json()["_id"]

        response = api_context.get(f"/usuarios/{usuario_id}")

        assert response.status == 200
        body = response.json()
        assert body["email"] == usuario["email"]
        assert body["nome"] == usuario["nome"]

    def test_buscar_usuario_id_inexistente(self, api_context: APIRequestContext):
        response = api_context.get("/usuarios/idInexistente000")

        assert response.status == 400

    def test_editar_usuario(self, api_context: APIRequestContext):
        usuario = gerar_usuario()
        criado = api_context.post("/usuarios", data=usuario)
        usuario_id = criado.json()["_id"]

        novo_nome = "Nome Atualizado"
        response = api_context.put(f"/usuarios/{usuario_id}", data={**usuario, "nome": novo_nome})

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro alterado com sucesso"

    def test_deletar_usuario(self, api_context: APIRequestContext):
        usuario = gerar_usuario()
        criado = api_context.post("/usuarios", data=usuario)
        usuario_id = criado.json()["_id"]

        response = api_context.delete(f"/usuarios/{usuario_id}")

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro excluído com sucesso"

    def test_deletar_usuario_inexistente(self, api_context: APIRequestContext):
        response = api_context.delete("/usuarios/idInexistente000")

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Nenhum registro excluído"
