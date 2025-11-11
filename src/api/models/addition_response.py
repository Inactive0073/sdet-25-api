from pydantic import ConfigDict, Field

from .addition_request import Addition


class AdditionResponse(Addition):
    id: int = Field(..., title="ID дополнительной информации")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "additional_info": "Дополнительная информация",
                "additional_number": 42,
            }
        },
    )
