from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Addition(BaseModel):
    additional_info: Optional[str] = Field(
        ..., title="Дополнительная информация о сущности", max_length=255
    )
    additional_number: Optional[int] = Field(
        None, title="Дополнительное число для сущности", ge=0
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
