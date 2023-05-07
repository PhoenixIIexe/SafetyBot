from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Registration(StatesGroup):
    password: State = State()
    rights: State = State()


class Enter(StatesGroup):
    password: State = State()


class CameraState(StatesGroup):
    ip: State = State()
    place: State = State()


class Entered(StatesGroup):
    entered: State = State()


class EditCameraState(StatesGroup):
    id: State = State()
    ip: State = State()
    place: State = State()


