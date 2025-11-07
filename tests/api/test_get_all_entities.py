import allure
import pytest
from src.api.client import APIClient
from src.api.actions.entity_actions import EntityActions
from src.api.models.entity import Entity


@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Получение списка всех сущностей")
@pytest.mark.api
class TestGetAllEntities:
    @allure.title("TC-003: Получение списка всех сущностей")
    def test_get_all_entities(self):
        client = APIClient()
        actions = EntityActions(client)

        # Добавим несколько
        for _ in range(3):
            actions.create_entity(Entity.random())

        entities = actions.get_all_entities()
        assert isinstance(entities, list), "Ответ не является списком"
        assert all(isinstance(e, Entity) for e in entities), "Не все элементы — Entity"
