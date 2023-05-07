from typing import Any
from aiogram import types
import data
from aiogram.filters.callback_data import CallbackData

class IsAdmin:
    def __init__(self) -> None:
        ...

    async def __call__(self, message: types.Message) -> bool:
        user = data.session.query(data.SBdata).filter_by(user_id=message.from_user.id).first()
        return user is not None


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
