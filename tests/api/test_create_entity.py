import allure
import pytest
from src.api.client import APIClient
from src.api.actions.entity_actions import EntityActions
from src.api.models.entity import Entity


@allure.epic("API Testing")
@allure.feature("Entity Management")
@allure.story("Создание сущности")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
class TestCreateEntity:
    @allure.title("TC-001: Создание новой сущности")
    def test_create_entity(self):
        client = APIClient()
        entity_actions = EntityActions(client)

        test_entity = Entity.random()
        _id: int = entity_actions.create_entity(test_entity)

        assert _id is not None, "ID новой сущности не получен"
        assert entity_actions.get_entity_by_id(_id).title == test_entity.title, "Название в ответе не совпадает"
