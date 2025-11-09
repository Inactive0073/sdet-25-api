import allure
import pytest

from src.api.actions.entity_actions import EntityActions
from src.api.client import APIClient
from src.api.models.entity_request import EntityRequest
from src.api.models.entity_response import EntityResponse


@allure.parent_suite("API test-service")
@allure.suite("Entity Management")
@allure.sub_suite("PATCH /api/patch")
@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Частичное обновление сущности")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "positive", "update", "v1.0")
@allure.label("owner", "Alexey Yumanov")
@allure.testcase("TC-004")
@allure.description("""
**Цель:** Проверить частичное обновление данных сущности через PATCH.  

**Ожидаемый результат:**  
- HTTP 200  
- Поля, переданные в теле запроса, обновлены
- Остальные поля остались без изменений
""")
@pytest.mark.api
class TestPatchEntity:
    @allure.title("TC-004: Частичное обновление сущности")
    def test_patch_entity(self, api_client: APIClient):
        actions = EntityActions(api_client)
        original = actions.create_entity(EntityRequest.random())
        updated_request = EntityRequest.random()
        updated = actions.patch_entity(original.id, updated_request)

        assert isinstance(updated, EntityResponse), (
            "Ответ не соответствует модели EntityResponse"
        )
        assert updated.id == original.id, "ID должен остаться тем же"
        assert updated.title != original.title, "Title должен измениться"
