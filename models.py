from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Items(models.Model):
    """
    The Item model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    description = fields.TextField()


Item_Pydantic = pydantic_model_creator(Items, name="Item")
ItemIn_Pydantic = pydantic_model_creator(Items, name="ItemIn", exclude=["id"])
