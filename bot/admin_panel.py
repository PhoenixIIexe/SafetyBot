from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from sqlalchemy import and_

import data
import text
from states import CameraState, EditCameraState
from filters import *
from keyboards import *
from states import Entered


class AdminPanel:
    def __init__(self: Bot):
        self.admin_router = Router()

        self.admin_router.message.register(
            self.newcamera, Command('new_camera'), IsAdmin())
        self.admin_router.message.register(
            self.newcamera, Text(text='Добавить камеру'), IsAdmin())
        self.admin_router.message.register(
            self.get_ip_camera, CameraState.ip)
        self.admin_router.message.register(
            self.get_place_camera, CameraState.place)
        self.admin_router.message.register(
            self.mycamera, Command('my_cameras'), IsAdmin())
        self.admin_router.message.register(
            self.mycamera, Text(text='Мои камеры'))
        self.admin_router.message.register(
            self.ipeditedcamera, EditCameraState.ip)
        self.admin_router.message.register(
            self.placeeditedcamera, EditCameraState.place)

        self.admin_router.callback_query.register(
            self.backmycamera, BackCamera.filter())
        self.admin_router.callback_query.register(
            self.editcamera, MyCamera.filter())
        self.admin_router.callback_query.register(
            self.editcamera, BackEditCamera.filter())
        self.admin_router.callback_query.register(
            self.statecamera, StateCamera.filter())
        self.admin_router.callback_query.register(
            self.changestatecamera, ChangeStateCamera.filter())
        self.admin_router.callback_query.register(
            self.infocamera, InfoCamera.filter())
        self.admin_router.callback_query.register(
            self.ipeditcamera, IpEditCamera.filter())
        self.admin_router.callback_query.register(
            self.placeeditcamera, PlaceEditCamera.filter())
        self.admin_router.callback_query.register(
            self.deletecamera, DeleteCamera.filter())

    async def newcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await message.answer('Введите IP камеры: ', reply_markup=ReplyKeyboardRemove)
        await state.clear()
        await state.set_state(Entered.entered)
        await state.set_state(CameraState.ip)

    async def get_ip_camera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await state.update_data(ip=message.text)
        await message.answer('Введите место, где установлена камера: ')
        await state.set_state(CameraState.place)

    async def get_place_camera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await state.update_data(place=message.text)

        info_camera = await state.get_data()

        user: data.SBdata = data.session.query(data.SBdata).filter_by(
            user_id=message.from_user.id).first()

        stmt = data.db.select(data.Camera).where(and_(data.Camera.ip == info_camera.get(
            'ip'), data.Camera.user_id == user.id))
        camera: data.Camera = data.session.scalars(stmt).first()
        print(camera)
        if camera is None:
            new_camera = data.Camera(**info_camera)
            user.camera.append(new_camera)
            data.session.commit()
            await message.answer(text=text.camera_text3, reply_markup=set_camera_keyboard())
        else:
            await message.answer(text=text.camera_text4, reply_markup=set_camera_keyboard())
        await state.clear()

    async def mycamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        user: data.SBdata = data.session.query(data.SBdata).filter_by(
            user_id=message.from_user.id).first()

        cameras: data.Camera = data.session.query(data.Camera).filter_by(
            user_id=user.id)

        await message.answer('Выберите камеру из списка ниже: ', reply_markup=set_mycamera_buttons(cameras))
        await state.clear()
        await state.set_state(Entered.entered)

    async def backmycamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: BackCamera) -> None:
        user: data.SBdata = data.session.query(data.SBdata).filter_by(
            user_id=query.from_user.id).first()

        cameras: data.Camera = data.session.query(data.Camera).filter_by(
            user_id=user.id)

        await query.message.edit_text('Выберите камеру из списка ниже: ', reply_markup=set_mycamera_buttons(cameras))

    async def editcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: MyCamera) -> None:
        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=callback_data.id).first()
        text = f"""
Вот она: {camera.place}({camera.ip}).
Что вы хотите делать с камерой?
        """
        await query.message.edit_text(text, reply_markup=set_editcamera_buttons(callback_data.id))

    async def statecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: StateCamera) -> None:
        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=callback_data.id).first()

        if camera.state:
            text = "Камера <b>включена</b>"
            to_change = "Выключить"
        else:
            text = "Камера <b>выключена</b>"
            to_change = "Включить"

        await query.message.edit_text(text, reply_markup=set_statecamera_buttons(callback_data.id, to_change), parse_mode='html')

    async def changestatecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: ChangeStateCamera) -> None:
        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=callback_data.id).first()
        camera.state = not bool(camera.state)
        data.session.commit()

        if camera.state:
            text = "Камера <b>включена</b>"
            to_change = "Выключить"
        else:
            text = "Камера <b>выключена</b>"
            to_change = "Включить"

        await query.message.edit_text(text, reply_markup=set_statecamera_buttons(callback_data.id, to_change), parse_mode='html')

    async def infocamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: InfoCamera) -> None:
        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=callback_data.id).first()

        text = f"""
Редактировать {camera.place} информацию

<b>IP:</b> {camera.ip}
<b>place:</b> {camera.place}
        """

        await query.message.edit_text(text, reply_markup=set_infocamera_buttons(callback_data.id), parse_mode='html')

    async def ipeditcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: IpEditCamera, state: FSMContext) -> None:
        await query.message.answer('Введите IP камеры: ')
        await state.update_data(id=callback_data.id)
        await state.set_state(EditCameraState.ip)

    async def ipeditedcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        camera = await state.get_data()

        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=camera.get('id')).first()
        camera.ip = message.text

        await message.answer('Успешно!', reply_markup=set_success_buttons(camera.id))

        await state.clear()

    async def placeeditcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: PlaceEditCamera, state: FSMContext) -> None:
        await query.message.answer('Введите место, где установлена камера: ')
        await state.update_data(id=callback_data.id)
        await state.set_state(EditCameraState.place)

    async def placeeditedcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        camera = await state.get_data()

        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=camera.get('id')).first()
        camera.place = message.text

        await message.answer('Успешно!', reply_markup=set_success_buttons(camera.id))

        await state.clear()

    async def deletecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: DeleteCamera) -> None:
        camera: data.Camera = data.session.query(
            data.Camera).filter_by(id=callback_data.id).first()
        await query.message.edit_text(f'Ты успешно удалил камеру\n{camera.place}({camera.ip})', reply_markup=set_backmycamera_buttons(), parse_mode='html')

        data.session.delete(camera)
        data.session.commit()
