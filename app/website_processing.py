from flask_sqlalchemy import SQLAlchemy
from datetime import date
import time
from random import randint
from app.settings import get_settings, get_all_languages, get_string_contain


def get_user_data(db: SQLAlchemy, table: any, username: str = None,
                  user_id: int = None, email: str = None) -> any:
    users = table.query.all()
    if user_id:
        return table.query.filter_by(id=user_id).first()
    if username:
        return table.query.filter_by(username=username).first()
    if email:
        return table.query.filter_by(email=email).first()


def add_user(db: SQLAlchemy, User: any, username: str, email: str, password: str, register_date = date.today(), bonus_taked = 0):
    new_user = User(username=username, email=email, password=password, register_date=register_date, bonus_taked=bonus_taked)
    print(new_user, type(new_user))
    db.session.add(new_user)
    db.session.commit()


def take_bonus(db: SQLAlchemy, Role: any, user: any, different: int) -> int:
    indent = is_able_take_bonus(user)
    if is_able_take_bonus(user):
        return indent
    else:
        change_coins(db, Role, user, different)
        user.bonus_taked = time.time()
        db.session.commit()
        return 0


def change_user_info(db: SQLAlchemy, user: any, username: str = None, email: str = None, password: str = None, register_date: str = None, coins: int = None, language: str = None) -> None:
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = password
    if language:
        user.language = language
    if register_date:
        user.register_date = register_date
    if coins:
        user.coins = coins
    db.session.commit()


def change_coins(db: SQLAlchemy, Role: any, user: any, different: int) -> None:
    user.coins = user.coins + different
    db.session.commit()
    is_new_achievement(db, user, Role)


def random_count_coins() -> int:
    min, max = get_settings("min_coins_bonus"), get_settings("max_coins_bonus")
    if min > max:
        raise Exception("min can't be bigger than max in random_count_coins function.")
    if min == max:
        return min
    return randint(min, max)


def is_able_take_bonus(user: any, indent: int = None) -> int:
    """
    Gives 0 if indent time already passed or number of remaining minutes if not.
    """
    if indent is None:
        indent = get_settings("bonus_indent")
    now_indent = time.time() - float(user.bonus_taked)
    if now_indent >= indent:
        return 0
    return time.localtime(indent - now_indent).tm_min


def add_achievement(db: SQLAlchemy, Achievement: any, author: str, name: str, description: str) -> None:
    new_achievement = Achievement(author=author, name=name, description=description)
    db.session.add(new_achievement)
    db.session.commit()


def is_new_achievement(db: SQLAlchemy, user: any, Achievement: any) -> None:
    if user.rank in ["Moderator", "White crow"]:
        return None
    user_achievements = Achievement.query.filter_by(author=user.username).all()
    achievement_coins = [get_settings(f"achievement_coins_{index}") for index in range(1, get_settings("achievements_count")+1)]
    achievement_name = [user_achievement.name for user_achievement in user_achievements]
    for index in range(1, get_settings("achievements_count")+1):
        if f"role_coins_{index}" not in achievement_name and user.coins >= achievement_coins[index-1]:
            add_achievement(db, Achievement, user.username, f"achievement_coins_{index}", str(date.today()))
            user.rank = f"achievement_coins_{index}"
            db.session.commit()


def get_form_choices(choice_type: str) -> list[complex]:
    if choice_type == "languages":
        languages = get_all_languages()
        choices = [("-", "-")]
        for language in languages:
            choices.append((language, get_string_contain(language, "icon")))
        return choices


def new_admin(db: SQLAlchemy, User: any, user_id: int) -> str:
    user = User.query.get(user_id)
    if user.rank != "Moderator":
        user.rank = "Moderator"
        db.session.commit()
        return f"Now user \"{user.username}\" is admin"
    return f"User \"{user.username}\" already was an admin. Nothing changed"


def remove_admin(db: SQLAlchemy, User: any, user_id: int) -> None:
    user = User.query.get(user_id)
    if user.rank == "Moderator":
        user.rank = "White crow"
        db.session.commit()
        return f"User \"{user.username}\" was unpromoted"
    return f"User \"{user.username}\" wasn't an admin. Nothing changed"
