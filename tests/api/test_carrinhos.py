import pytest
from playwright.sync_api import APIRequestContext, Playwright
from utils.data_factory import gerar_produto, gerar_usuario
import os


@pytest.mark.api
class TestCarrinhos:
    @pytest.fixture(autouse=True)
    def setup_carrinho(self, playwright: Playwright):
        """Cria contexto autenticado exclusivo para testes de carrinho."""
        base_url = os.getenv("BASE_URL_API", "https://serverest.dev")

        ctx = playwright.request.new_context(base_url=base_url)
        usuario = gerar_usuario()
        ctx.post("/usuarios", data=usuario)
        login = ctx.post("/login", data={
            "email": usuario["email"],
            "password": usuario["password"],
        })
        token = login.json()["authorization"]
        ctx.dispose()

        self.ctx = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={"Authorization": token},
        )

        # Cria um produto para usar nos testes
        produto = gerar_produto()
        admin_ctx = playwright.request.new_context(base_url=base_url)
        login_admin = admin_ctx.post("/login", data={
            "email": os.getenv("ADMIN_EMAIL", "fulano@qa.com"),
            "password": os.getenv("ADMIN_PASSWORD", "teste"),
        })
        admin_token = login_admin.json()["authorization"]
        admin_ctx.dispose()

        admin_auth_ctx = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={"Authorization": admin_token},
        )
        criado = admin_auth_ctx.post("/produtos", data=produto)
        self.produto_id = criado.json()["_id"]
        admin_auth_ctx.dispose()

        yield

        # Garante que o carrinho seja cancelado após o teste
        self.ctx.delete("/carrinhos/cancelar-compra")
        self.ctx.dispose()

    def test_listar_carrinhos(self, api_context: APIRequestContext):
        response = api_context.get("/carrinhos")

        assert response.status == 200
        body = response.json()
        assert "quantidade" in body
        assert "carrinhos" in body

    def test_criar_carrinho(self):
        response = self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })

        assert response.status == 201
        body = response.json()
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body

    def test_criar_segundo_carrinho_mesmo_usuario(self):
        self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })

        response = self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })

        assert response.status == 400
        body = response.json()
        assert "carrinho" in body["message"].lower()

    def test_concluir_compra(self):
        self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })

        response = self.ctx.delete("/carrinhos/concluir-compra")

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro excluído com sucesso"

    def test_cancelar_compra(self):
        self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })

        response = self.ctx.delete("/carrinhos/cancelar-compra")

        assert response.status == 200
        body = response.json()
        assert body["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"

    def test_buscar_carrinho_por_id(self):
        criado = self.ctx.post("/carrinhos", data={
            "produtos": [{"idProduto": self.produto_id, "quantidade": 1}]
        })
        carrinho_id = criado.json()["_id"]

        response = self.ctx.get(f"/carrinhos/{carrinho_id}")

        assert response.status == 200
        body = response.json()
        assert body["_id"] == carrinho_id
        assert len(body["produtos"]) == 1
