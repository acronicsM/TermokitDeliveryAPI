from pydantic import BaseModel, Field, model_validator


class ItemBase(BaseModel):
    code_item: str
    article_item: str
    unit: str
    name: str
    quantity: float = Field(gt=0)
    quantity_shipped: float = Field(ge=0)
    price: float = Field(ge=0)
    sum: float = Field(ge=0)
    discount: float = Field(ge=0)
    bonus: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_quantity_shipped(self):
        if self.quantity_shipped > self.quantity:
            raise ValueError("Quantity shipped cannot be greater than quantity")
        return self


class ItemWithID(ItemBase):
    id: int


class ItemCreate(ItemBase):
    order_id: int
