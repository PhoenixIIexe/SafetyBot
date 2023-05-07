from aiogram import Bot, Router, types
from aiogram.filters import Command

from . import config
from data import models


class UserCommand:
    def __init__(self: Bot) -> None:
        self.router_user_command = Router()

        self.router_user_command.message.register(self.reg, Command('reg'))

    async def reg(self: Bot, message: types.Message) -> None:
        if message.text.endswith(config.SECRET_PASSWORD):
            stmt = models.db.select(models.User).where(
                models.User.tg_id == message.from_user.id)
            user: models.User = models.session.scalars(stmt).first()
            if user is None:
                new_user = models.User(tg_id=message.from_user.id)
                models.session.add(new_user)
                models.session.commit()
                await message.answer('Вы успешно зарегестрировались')
            else:
                await message.answer('Вы уже зарегестрировались!')
        else:
            await message.answer('Пароль неверный!')
