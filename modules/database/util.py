from modules.database.database import db
from modules.database.models.tg_users import TgUsers
from modules.database.models.user_ideas import UserIdeas


def create_tables():
    with db:
        db.create_tables([
            TgUsers,
            UserIdeas,
        ])
