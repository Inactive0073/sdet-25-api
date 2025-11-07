from pydantic import BaseModel, Field
from faker import Faker
from typing import Optional

fake = Faker("en_US")


class Entity(BaseModel):
    addition: Optional[dict] = Field(
        default_factory=dict, description="Дополнительные данные сущности"
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
        length_dict: int = 3,
        length_list: int = 5,
        unique_list: bool = True,
    ) -> "Entity":
        """Генерирует случайную сущность с использованием Faker."""
        if with_optional:
            addition_dict = {
                fake.word(): fake.word() for _ in range(length_dict)
            }
            important_numbers = list(fake.random_elements(
                elements=range(1, 100), length=length_list, unique=unique_list
            ))
            return cls(
                addition=addition_dict,
                important_numbers=important_numbers,
                title=fake.sentence(nb_words=3),
                verified=fake.boolean(),
            )
        else:
            return cls(
                title=fake.sentence(nb_words=3),
                verified=fake.boolean(),
            )

    class Config:
        schema_extra = {
            "example": {
                "addition": {"key": "value"},
                "important_numbers": [1, 2, 3],
                "title": "Test Entity",
                "verified": True,
            }
        }
