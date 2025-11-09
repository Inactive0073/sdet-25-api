import allure

from src.api.client import APIClient
from src.api.models.entity_request import EntityRequest
from src.api.models.entity_response import EntityResponse
from src.api.utils.deserializer import parse_list_response, parse_response
from src.data import Endpoints


class EntityActions:
    """Слой бизнес-логики API для работы с сущностями."""

    def __init__(self, client: APIClient):
        self.client = client

    def create_entity(self, entity: EntityRequest) -> EntityResponse:
        allure.step("Создание новой сущности: {entity.title}")
        response = self.client.post(
            Endpoints.CREATE, json=entity.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return parse_response(EntityResponse, response)

    @allure.step("Получение сущности по ID: {entity_id}")
    def get_entity_by_id(self, entity_id: int) -> EntityResponse:
        response = self.client.get(f"{Endpoints.GET_BY_ID}/{entity_id}")
        response.raise_for_status()
        return parse_response(EntityResponse, response)

    @allure.step("Получение списка всех сущностей")
    def get_all_entities(self) -> list[EntityResponse]:
        response = self.client.get(Endpoints.GET_ALL)
        response.raise_for_status()
        return parse_list_response(EntityResponse, response)

    @allure.step("Частичное обновление сущности ID={entity_id}")
    def patch_entity(self, entity_id: int, entity: EntityRequest) -> EntityResponse:
        response = self.client.patch(
            f"{Endpoints.PATCH}/{entity_id}", json=entity.model_dump(exclude_none=True)
        )
        response.raise_for_status()
        return parse_response(EntityResponse, response)

    @allure.step("Удаление сущности ID={entity_id}")
    def delete_entity(self, entity_id: int) -> dict:
        response = self.client.delete(f"{Endpoints.DELETE}/{entity_id}")
        response.raise_for_status()
        return response.json()
