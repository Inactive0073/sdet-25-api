import allure
import pytest
from src.api.client import APIClient
from src.api.actions.entity_actions import EntityActions
from src.api.models.entity import Entity


@allure.epic("API test-service")
@allure.feature("Entity")
@allure.story("Обновление сущности")
@pytest.mark.api
class TestPatchEntity:
    @allure.title("TC-004: Обновление поля title у сущности")
    def test_patch_entity(self):
        client = APIClient()
        actions = EntityActions(client)

        created = actions.create_entity(Entity.random())
        new_title = "Updated " + created.title

        updated = actions.patch_entity(created.id, {"title": new_title})

        assert updated.title == new_title, "Название не обновилось"
        assert updated.id == created.id, "ID не должен меняться при PATCH"
