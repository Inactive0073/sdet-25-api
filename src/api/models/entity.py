from typing import Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from .addition_request import Addition

fake = Faker("en_US")


class EntityRequest(BaseModel):
    addition: Optional[Addition] = Field(
        default=None, description="Дополнительные данные сущности"
    )
    important_numbers: Optional[list[int]] = Field(
        default_factory=list, description="Список важных чисел"
    )
    title: str = Field(..., description="Название сущности")
    verified: bool = Field(..., description="Флаг верификации")

    @classmethod
    def random(
        cls,
        with_optional: bool = True,
        length_list: int = 5,
        unique_list: bool = True,
    ) -> "EntityRequest":
        """Генерирует случайную сущность с использованием Faker."""
        if with_optional:
            addition = Addition(
                additional_info=fake.sentence(nb_words=6),
                additional_number=fake.random_int(min=1, max=100),
            )
            important_numbers = list(
                fake.random_elements(
                    elements=range(1, 100), length=length_list, unique=unique_list
                )
            )
            return cls(
                addition=addition,
                important_numbers=important_numbers,
                title=fake.sentence(nb_words=3),
                verified=fake.boolean(),
            )
        else:
            return cls(
                title=fake.sentence(nb_words=3),
                verified=fake.boolean(),
            )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "addition": {
                    "additional_info": "Additional information",
                    "additional_number": 42,
                },
                "important_numbers": [1, 2, 3],
                "title": "Test Entity",
                "verified": True,
            }
        },
    )
