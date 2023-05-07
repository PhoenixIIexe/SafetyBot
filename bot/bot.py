from typing import Optional
from aiogram.client.session.base import BaseSession

import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from .admin_command import AdminCommand
from .user_command import UserCommand
from . import markup


class SecuritySystem(Bot, AdminCommand, UserCommand):
    def __init__(self, token: str, session: Optional[BaseSession] = None, parse_mode: Optional[str] = None) -> None:
        super().__init__(token, session, parse_mode)
        AdminCommand.__init__(self)
        UserCommand.__init__(self)
        logging.basicConfig(level=logging.INFO)

        self.storage = MemoryStorage()
        self.dispatcher = Dispatcher(storage=self.storage)
        self.router_main = Router()

        self.dispatcher.include_router(self.router_main)
        self.dispatcher.include_router(self.router_admin_command)
        self.dispatcher.include_router(self.router_user_command)

        self.router_main.message.register(self.start, Command('start'))

    async def start(self, message: types.Message) -> None:
        text = f"""
Добро пожаловать, {message.from_user.first_name}!
Вы можете ознакомиться с моими функциями, нажав на '/' или 'меню'.
    """

        await self.set_my_commands(markup.set_default_commands)
        await message.answer(text)
