from faker import Faker

_fake = Faker("pt_BR")


def gerar_usuario(admin: bool = False) -> dict:
    return {
        "nome": _fake.name(),
        "email": _fake.unique.email(),
        "password": _fake.password(length=10),
        "administrador": "true" if admin else "false",
    }


def gerar_produto() -> dict:
    return {
        "nome": f"{_fake.word().capitalize()} {_fake.unique.uuid4()[:8]}",
        "preco": _fake.random_int(min=10, max=5000),
        "descricao": _fake.sentence(),
        "quantidade": _fake.random_int(min=1, max=100),
    }
