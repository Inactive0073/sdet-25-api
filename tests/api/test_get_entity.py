import allure
import pytest
from src.api.client import APIClient
from src.api.actions.entity_actions import EntityActions
from src.api.models.entity import Entity


@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение сущности по ID")
@pytest.mark.api
class TestGetEntity:
    @allure.title("TC-002: Получение созданной сущности по ID")
    def test_get_entity_by_id(self, api_client: APIClient):
        actions = EntityActions(api_client)

        created = actions.create_entity(Entity.random())
        fetched = actions.get_entity_by_id(created.id)

        assert fetched.id == created.id, "ID сущности не совпадает"
        assert fetched.title == created.title, "Название не совпадает"
