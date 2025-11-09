import allure
import pytest

from src.api.actions.entity_actions import EntityActions
from src.api.client import APIClient
from src.api.models.entity_request import EntityRequest
from src.data.endpoints import Endpoints


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("DELETE /api/delete")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Удаление сущности по ID")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "positive", "delete", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-005")
@allure.description("""
**Цель:** Проверить успешное удаление сущности по `id`.

**Ожидаемый результат:**
- HTTP 200 или 204
- Повторный GET по `id` возвращает 404
""")
@pytest.mark.api
class TestDeleteEntity:
    @allure.title("TC-005: Удаление сущности по ID")
    def test_delete_entity(self, api_client: APIClient):
        actions = EntityActions(api_client)
        created = actions.create_entity(EntityRequest.random())

        delete_response = actions.delete_entity(created.id)
        assert "deleted" in delete_response.get("status", "").lower(), (
            f"Удаление не подтверждено, ответ: {delete_response}"
        )

        get_after_delete = actions.client.get(Endpoints.GET_BY_ID.format(id=created.id))
        assert get_after_delete.status_code in (404, 410), (
            f"Ожидали 404 или 410, получили {get_after_delete.status_code}"
        )
