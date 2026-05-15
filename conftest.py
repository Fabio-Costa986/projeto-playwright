import logging
import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright, Page

load_dotenv()

# Silencia loggers ruidosos de bibliotecas externas
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

BASE_URL_API = os.getenv("BASE_URL_API", "https://serverest.dev")
BASE_URL_FRONT = os.getenv("BASE_URL_FRONT", "https://front.serverest.dev")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "fulano@qa.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "teste")


# Captura resultado de cada fase do teste para detectar falha no fixture `page`
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=BASE_URL_API)
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_context: APIRequestContext) -> str:
    response = api_context.post("/login", data={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
    })
    assert response.ok, f"Login falhou: {response.text()}"
    return response.json()["authorization"]


@pytest.fixture(scope="session")
def auth_api_context(playwright: Playwright, auth_token: str) -> APIRequestContext:
    context = playwright.request.new_context(
        base_url=BASE_URL_API,
        extra_http_headers={"Authorization": auth_token},
    )
    yield context
    context.dispose()


@pytest.fixture
def page(browser, request) -> Page:
    context = browser.new_context(base_url=BASE_URL_FRONT)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    # Salva o trace apenas se o teste falhou
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        safe_name = request.node.name.replace("[", "_").replace("]", "")
        trace_path = f"reports/traces/{safe_name}.zip"
        context.tracing.stop(path=trace_path)
        logging.getLogger("conftest").warning("Trace salvo: %s", trace_path)
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture
def logged_page(page: Page) -> Page:
    from pages.login_page import LoginPage
    login = LoginPage(page)
    login.goto()
    login.fazer_login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("**/admin/home", timeout=10000)
    return page


def pytest_configure(config):
    os.makedirs("reports/traces", exist_ok=True)
