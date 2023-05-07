from aiogram.fsm.state import StatesGroup, State


class CameraState(StatesGroup):
    ip: State = State()
    place: State = State()


class EditCameraState(StatesGroup):
    id: State = State()
    ip: State = State()
    place: State = State()
