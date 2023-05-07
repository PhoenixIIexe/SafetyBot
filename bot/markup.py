from typing import List

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .filters import *

set_default_commands: List[types.BotCommand] = [
    types.BotCommand(command="start", description="Запустить бота"),
    types.BotCommand(
        command="reg", description="Получить права руководителя (При наличие пароля)"),
    types.BotCommand(command="newcamera", description="Добавить новую камеру"),
    types.BotCommand(command="mycamera",
                     description="Отредактируйте своу камеру")
]


def set_mycamera_buttons(mycameras) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text=mycamera.place,
                 callback_data=MyCamera(id=mycamera.id).pack()) for mycamera in mycameras], width=2)

    return keyboard.as_markup()


def set_editcamera_buttons(id_camera: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text='Состояние камеры?',
                 callback_data=StateCamera(id=id_camera).pack()), InlineKeyboardButton(text='Информация о камере',
                 callback_data=InfoCamera(id=id_camera).pack()), InlineKeyboardButton(text='Удалить камеру', callback_data=DeleteCamera(id=id_camera).pack())], width=2)
    keyboard.row(*[InlineKeyboardButton(text='<< Вернуться к списку камер',
                 callback_data=BackCamera().pack())], width=1)

    return keyboard.as_markup()


def set_statecamera_buttons(id_camera: int, to_change: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text=to_change,
                                        callback_data=ChangeStateCamera(id=id_camera).pack()),
                   InlineKeyboardButton(text='<< Вернуться к найстройке камер',
                                        callback_data=BackEditCamera(id=id_camera).pack())], width=1)

    return keyboard.as_markup()


def set_infocamera_buttons(id_camera: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text='Изменить IP',
                                        callback_data=IpEditCamera(id=id_camera).pack()),
                   InlineKeyboardButton(text='Изменить place',
                                        callback_data=PlaceEditCamera(id=id_camera).pack())], width=2)  # InlineKeyboardButton(text='Просмотр камеры', web_app=None)
    keyboard.row(*[InlineKeyboardButton(text='<< Вернуться к найстройке камер',
                                        callback_data=BackEditCamera(id=id_camera).pack())], width=1)

    return keyboard.as_markup()


def set_backmycamera_buttons() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text='<< Вернуться к списку камер',
                 callback_data=BackCamera().pack())], width=1)

    return keyboard.as_markup()


def set_success_buttons(id_camera) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*[InlineKeyboardButton(text='<< Вернуться к найстройке камер',
                                        callback_data=BackEditCamera(id=id_camera).pack()), InlineKeyboardButton(text='<< Вернуться к списку камер',
                 callback_data=BackCamera().pack())], width=2)

    return keyboard.as_markup()
