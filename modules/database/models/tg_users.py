from peewee import IntegerField, DateTimeField
from datetime import datetime
from modules.database.models.base_model import BaseModel


class TgUsers(BaseModel):
    telegram_id = IntegerField()
    chat_id = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    last_update = DateTimeField(default=datetime.now)
