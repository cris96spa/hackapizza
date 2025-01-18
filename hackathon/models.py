from enum import Enum
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    assertion: bool


class MenuMetadata(BaseModel):
    chef_name: str | None = Field(description="The name of the chef", default=None)
    restaurant_name: str | None = Field(
        description="The name of the restaurant", default=None
    )
    planet_name: str | None = Field(
        description="The name of the planet the restaurant is located", default=None
    )
    licences: list = Field(description="The licences of the chef", default_factory=list)


menu_metadata_keys = list(MenuMetadata.model_fields.keys())


class DishMetadata(BaseModel):
    dish_name: str = Field(..., description="Dish Name")
    dish_techniques: list = Field(
        description="Techniques involved in making the dish", default_factory=list
    )
    dish_ingredients: list = Field(
        description="Ingredients used in the dish", default_factory=list
    )


dish_metadata_keys = list(DishMetadata.model_fields.keys())
