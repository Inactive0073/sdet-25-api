from pydantic import ConfigDict, Field

from .entity_request import EntityRequest


class EntityResponse(EntityRequest):
    id: int = Field(..., description="ID сущности")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "addition": {
                    "additional_info": "Дополнительная информация",
                    "additional_number": 42,
                },
                "important_numbers": [1, 2, 3],
                "title": "Тестовая сущность",
                "verified": True,
            }
        },
    )
