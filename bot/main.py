from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import asyncio

from admin_panel import AdminPanel
from keyboards import set_reg_keyboard, set_camera_keyboard
from states import Registration
from filters import IsAdmin
import text
import info
import data


class SafetyBot(Bot, AdminPanel):
    def __init__(self, token: str, session = None, parse_mode = None) -> None:
        super().__init__(token, session, parse_mode)
        AdminPanel.__init__(self)

        self.dispatcher = Dispatcher()
        self.main_router = Router()
        self.dispatcher.include_router(self.main_router)
        self.dispatcher.include_router(self.admin_router)
        self.set_default_commands: list = [
            types.BotCommand(command='start', description='Запуск'),
            types.BotCommand(command='registration', description='Регистрация'),
            types.BotCommand(command='new_camera', description='Добавить камеру'),
            types.BotCommand(command='my_cameras', description='Удалить камеру')
        ]
        self.flag = False
    
        self.main_router.message.register(self.start, Command('start'))
        self.main_router.message.register(self.reg_password, Text(text='Зарегистрироваться'))
        self.main_router.message.register(self.reg_password, Command('registration'))
        self.main_router.message.register(self.reg_rights, Registration.password)
        self.main_router.message.register(self.give_rights, Registration.rights)

    async def notification(self):
        if self.flag:
            stmt = data.db.select(data.Camera).where(data.Camera.camera_ip == ...)
            camera: data.Camera = data.session.scalars(stmt).first()
            boss_id = camera.user_id
            await self.send_message(chat_id=boss_id, text=f'{text.not_text} По адресу: {camera.camera_adress}.')
            await self.send_photo(chat_id=boss_id, photo=FSInputFile(path='d:\Coding\Safety_bot\photo.png'))

    async def start(self, message: types.Message):
        await self.set_my_commands(self.set_default_commands)
        await message.answer(text=text.start_text)
        if IsAdmin():
            await message.answer(text='Вы зашли с правами администратора.', reply_markup=set_camera_keyboard())
        else:
            await message.answer(text='Пройдите регистрацию.', reply_markup=set_reg_keyboard())
        asyncio.create_task(self.notification())
        # ad = IsAdmin()
        # await message.answer(text=f'{ad.__call__()}')

    async def reg_password(self, message: types.Message, state: FSMContext):
        user = data.session.query(data.SBdata).filter_by(user_id=message.from_user.id).first()
        if user is None:
            new_user = data.SBdata(user_id=message.from_user.id)
            data.session.add(new_user)
            data.session.commit()
            await message.answer(text=text.reg_text2, reply_markup=ReplyKeyboardRemove)
            await state.clear()
            await state.set_state(Registration.password)
        else:
            await message.answer(text=text.reg_text0)

    async def reg_rights(self, message: types.Message, state: FSMContext):
        stmt = data.db.select(data.SBdata).where(data.SBdata.user_id == message.from_user.id)
        user: data.SBdata = data.session.scalars(stmt).first()
        user.password = message.text
        data.session.commit()
        await message.answer(text=text.reg_text3)
        await state.clear()
        await state.set_state(Registration.rights)

    async def give_rights(self, message: types.Message, state: FSMContext):
        stmt = data.db.select(data.SBdata).where(data.SBdata.user_id == message.from_user.id)
        user: data.SBdata = data.session.scalars(stmt).first()
        if message.text == info.RIGHTS_CODE:
            await message.answer(text=text.reg_text4, reply_markup=set_camera_keyboard())
        else:
            data.session.delete(user)
            await message.answer(text=text.reg_text5, reply_markup=set_camera_keyboard())
        data.session.commit()
        await state.clear()


if __name__ == '__main__':
    safe_bot = SafetyBot(token=info.TOKEN)
    safe_bot.dispatcher.run_polling(safe_bot)