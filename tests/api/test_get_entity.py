import allure
import pytest

from src.api.actions.entity_actions import EntityActions
from src.api.client import APIClient
from src.api.models.entity_request import EntityRequest
from src.api.models.entity_response import EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("GET /api/get")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение сущности по ID")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "get", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-002")
@allure.description("""
**Цель:** Проверить получение ранее созданной сущности по `id`.

**Ожидаемый результат:**
- HTTP 200
- В теле ответа корректная сущность с нужным `id`
""")
@pytest.mark.api
class TestGetEntityById:
    @allure.title("TC-002: Получение сущности по ID")
    def test_get_entity_by_id(self, api_client: APIClient):
        actions = EntityActions(api_client)
        created = actions.create_entity_synthetic(EntityRequest.random())

        fetched = actions.get_entity_by_id(created.id)

        assert isinstance(fetched, EntityResponse), (
            "Ответ не соответствует модели EntityResponse"
        )
        assert fetched.id == created.id, (
            f"ID должен совпадать: ожидали {created.id}, получили {fetched.id}"
        )
        assert fetched.title == created.title, "Title должен совпадать"
