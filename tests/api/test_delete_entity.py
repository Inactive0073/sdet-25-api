# tests/api/test_delete_entity.py
import allure
import pytest
from src.api.client import APIClient
from src.api.actions.entity_actions import EntityActions
from src.api.models.entity import Entity
from requests.exceptions import HTTPError


@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Удаление сущности")
@pytest.mark.api
class TestDeleteEntity:
    @allure.title("TC-005: Удаление сущности по ID")
    def test_delete_entity(self):
        client = APIClient()
        actions = EntityActions(client)

        created = actions.create_entity(Entity.random())
        assert actions.delete_entity(created.id), "Удаление не вернуло 204"

        # Проверяем, что объект действительно удалён
        with pytest.raises(HTTPError):
            actions.get_entity_by_id(created.id)
