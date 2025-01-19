from enum import Enum
from pydantic import BaseModel, Field


class MenuMetadata(BaseModel):
    chef_name: str | None = Field(description="Il nome dello chef", default=None)
    restaurant_name: str | None = Field(
        description="Il nome del ristorante", default=None
    )
    planet_name: str | None = Field(
        description="Il nome del pianeta sul quale si trova il ristorante", default=None
    )
    licences: list[str] | None = Field(
        description="Le licenze dello chef. Ogni licenza è caratterizzata da un nome e un livello. I livelli possono essere numeri interi, in numeri romani oppure descritti a parole. Usa la numerazione decimale (0,1,2,3,4,5) come standard.",
        default_factory=list,
    )


menu_metadata_keys = list(MenuMetadata.model_fields.keys())


class DishMetadata(BaseModel):
    dish_name: str | None = Field(description="Il nome del piatto", default=None)
    dish_techniques: list[str] | None = Field(
        description="Le tecniche di preparazione utilizzate per il piatto",
        default_factory=list,
    )
    dish_ingredients: list[str] | None = Field(
        description="Gli ingredienti che compongono il piatto. ", default_factory=list
    )


dish_metadata_keys = list(DishMetadata.model_fields.keys())
