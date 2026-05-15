import pytest
from playwright.sync_api import APIRequestContext
from utils.data_factory import gerar_produto


@pytest.mark.api
class TestProdutos:
    def test_listar_produtos(self, api_context: APIRequestContext):
        response = api_context.get("/produtos")

        assert response.status == 200
        body = response.json()
        assert "quantidade" in body
        assert "produtos" in body
        assert isinstance(body["produtos"], list)

    def test_criar_produto_autenticado(self, auth_api_context: APIRequestContext):
        produto = gerar_produto()
        response = auth_api_context.post("/produtos", data=produto)

        assert response.status == 201
        body = response.json()
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body

    def test_criar_produto_sem_autenticacao(self, api_context: APIRequestContext):
        produto = gerar_produto()
        response = api_context.post("/produtos", data=produto)

        assert response.status == 401

    def test_criar_produto_nome_duplicado(self, auth_api_context: APIRequestContext):
        produto = gerar_produto()
        auth_api_context.post("/produtos", data=produto)
        response = auth_api_context.post("/produtos", data=produto)

        assert response.status == 400
        body = response.json()
        assert "nome" in body["message"].lower() or "já" in body["message"]

    def test_buscar_produto_por_id(self, auth_api_context: APIRequestContext):
        produto = gerar_produto()
        criado = auth_api_context.post("/produtos", data=produto)
        produto_id = criado.json()["_id"]

        response = auth_api_context.get(f"/produtos/{produto_id}")

        assert response.status == 200
        body = response.json()
        assert body["nome"] == produto["nome"]
        assert body["preco"] == produto["preco"]

    def test_editar_produto(self, auth_api_context: APIRequestContext):
        produto = gerar_produto()
        criado = auth_api_context.post("/produtos", data=produto)
        produto_id = criado.json()["_id"]

        novo_preco = 999
        response = auth_api_context.put(
            f"/produtos/{produto_id}",
            data={**produto, "preco": novo_preco},
        )

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro alterado com sucesso"

    def test_deletar_produto(self, auth_api_context: APIRequestContext):
        produto = gerar_produto()
        criado = auth_api_context.post("/produtos", data=produto)
        produto_id = criado.json()["_id"]

        response = auth_api_context.delete(f"/produtos/{produto_id}")

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro excluído com sucesso"

    def test_buscar_produto_id_inexistente(self, api_context: APIRequestContext):
        response = api_context.get("/produtos/idInexistente000")

        assert response.status == 400
