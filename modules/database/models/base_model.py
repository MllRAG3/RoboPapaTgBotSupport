from modules.database.database import db
from peewee import AutoField, Model


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db
