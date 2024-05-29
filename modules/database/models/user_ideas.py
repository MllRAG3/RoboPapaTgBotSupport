from peewee import CharField, ForeignKeyField
from modules.database.models.base_model import BaseModel
from modules.database.models.tg_users import TgUsers


class UserIdeas(BaseModel):
    idea = CharField()
    user = ForeignKeyField(TgUsers, backref='ideas')
