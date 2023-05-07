from aiogram import types
from aiogram.filters import Filter
from aiogram.filters.callback_data import CallbackData

from data import models


class IsAdmin(Filter):
    def __init__(self) -> None:
        ...

    async def __call__(self, message: types.Message) -> bool:
        return models.session.query(models.User).filter_by(tg_id=message.from_user.id).first()


class MyCamera(CallbackData, prefix='my_camera'):
    id: int


class StateCamera(CallbackData, prefix='state_camera'):
    id: int


class ChangeStateCamera(CallbackData, prefix='change_state_camera'):
    id: int


class InfoCamera(CallbackData, prefix='info_camera'):
    id: int


class IpEditCamera(CallbackData, prefix='ip_edit_camera'):
    id: int


class PlaceEditCamera(CallbackData, prefix='place_edit_camera'):
    id: int


class DeleteCamera(CallbackData, prefix='delete_camera'):
    id: int


class BackCamera(CallbackData, prefix='back_camera'):
    ...


class BackEditCamera(CallbackData, prefix='back_camera'):
    id: int
