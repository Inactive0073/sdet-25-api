import allure
from src.api.client import APIClient
from src.api.models.entity import Entity
from src.api.endpoints import Endpoints


class EntityActions:
    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Создание новой сущности: {entity.name}")
    def create_entity(self, entity: Entity) -> int:
        response = self.client.post(Endpoints.CREATE, json=entity.dict(exclude_none=True))
        response.raise_for_status()
        return response.json().get("id")

    @allure.step("Получение всех сущностей")
    def get_all_entities(self) -> list[Entity]:
        response = self.client.get(Endpoints.GET_ALL)
        response.raise_for_status()
        return [Entity(**r) for r in response.json()]

    @allure.step("Получение сущности по ID: {entity_id}")
    def get_entity_by_id(self, entity_id: int) -> Entity:
        response = self.client.get(Endpoints.GET_BY_ID.format(id=entity_id))
        response.raise_for_status()
        return Entity(**response.json())

    @allure.step("Изменение сущности с ID {entity_id}")
    def patch_entity(self, entity_id: int, new_name: str) -> Entity:
        response = self.client.patch(
            Endpoints.PATCH.format(id=entity_id), json={"name": new_name}
        )
        response.raise_for_status()
        return Entity(**response.json())

    @allure.step("Удаление сущности с ID {entity_id}")
    def delete_entity(self, entity_id: int) -> bool:
        response = self.client.delete(Endpoints.DELETE.format(id=entity_id))
        response.raise_for_status()
        return response.status_code == 204
