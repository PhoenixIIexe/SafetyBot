from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from sqlalchemy import or_, and_

from .filters import *
from .states import CameraState, EditCameraState
from data import models
from . import markup


class AdminCommand:
    def __init__(self: Bot) -> None:
        self.router_admin_command = Router()

        self.router_admin_command.message.register(
            self.newcamera, Command('newcamera'), IsAdmin())
        self.router_admin_command.message.register(
            self.get_ip_camera, CameraState.ip)
        self.router_admin_command.message.register(
            self.get_place_camera, CameraState.place)
        self.router_admin_command.message.register(
            self.mycamera, Command('mycamera'), IsAdmin())
        self.router_admin_command.message.register(
            self.ipeditedcamera, EditCameraState.ip)
        self.router_admin_command.message.register(
            self.placeeditedcamera, EditCameraState.place)

        self.router_admin_command.callback_query.register(
            self.backmycamera, BackCamera.filter())
        self.router_admin_command.callback_query.register(
            self.editcamera, MyCamera.filter())
        self.router_admin_command.callback_query.register(
            self.editcamera, BackEditCamera.filter())
        self.router_admin_command.callback_query.register(
            self.statecamera, StateCamera.filter())
        self.router_admin_command.callback_query.register(
            self.changestatecamera, ChangeStateCamera.filter())
        self.router_admin_command.callback_query.register(
            self.infocamera, InfoCamera.filter())
        self.router_admin_command.callback_query.register(
            self.ipeditcamera, IpEditCamera.filter())
        self.router_admin_command.callback_query.register(
            self.placeeditcamera, PlaceEditCamera.filter())
        self.router_admin_command.callback_query.register(
            self.deletecamera, DeleteCamera.filter())

    async def newcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await message.answer('Введите IP камеры: ')
        await state.set_state(CameraState.ip)

    async def get_ip_camera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await state.update_data(ip=message.text)
        await message.answer('Введите место, где установлена камера: ')
        await state.set_state(CameraState.place)

    async def get_place_camera(self: Bot, message: types.Message, state: FSMContext) -> None:
        await state.update_data(place=message.text)

        info_camera = await state.get_data()

        user: models.User = models.session.query(models.User).filter_by(
            tg_id=message.from_user.id).first()

        stmt = models.db.select(models.Camera).where(and_(models.Camera.ip == info_camera.get(
            'ip'), models.Camera.user_id == user.id))
        camera: models.Camera = models.session.scalars(stmt).first()
        print(camera)
        if camera is None:
            new_camera = models.Camera(**info_camera)
            user.camera.append(new_camera)
            models.session.commit()
            await message.answer('Камера успешно установлена')
        else:
            await message.answer('Такая камеры уже есть!')

        await state.clear()

    async def mycamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        user: models.User = models.session.query(models.User).filter_by(
            tg_id=message.from_user.id).first()

        cameras: models.Camera = models.session.query(models.Camera).filter_by(
            user_id=user.id)

        await message.answer('Выберите камеру из списка ниже: ', reply_markup=markup.set_mycamera_buttons(cameras))

    async def backmycamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: BackCamera) -> None:
        user: models.User = models.session.query(models.User).filter_by(
            tg_id=query.from_user.id).first()

        cameras: models.Camera = models.session.query(models.Camera).filter_by(
            user_id=user.id)

        await query.message.edit_text('Выберите камеру из списка ниже: ', reply_markup=markup.set_mycamera_buttons(cameras))

    async def editcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: MyCamera) -> None:
        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=callback_data.id).first()
        text = f"""
Вот она: {camera.place}({camera.ip}).
Что вы хотите делать с камерой?
        """
        await query.message.edit_text(text, reply_markup=markup.set_editcamera_buttons(callback_data.id))

    async def statecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: StateCamera) -> None:
        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=callback_data.id).first()

        if camera.state:
            text = "Камера <b>включена</b>"
            to_change = "Выключить"
        else:
            text = "Камера <b>выключена</b>"
            to_change = "Включить"

        await query.message.edit_text(text, reply_markup=markup.set_statecamera_buttons(callback_data.id, to_change), parse_mode='html')

    async def changestatecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: ChangeStateCamera) -> None:
        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=callback_data.id).first()
        camera.state = not bool(camera.state)
        models.session.commit()

        if camera.state:
            text = "Камера <b>включена</b>"
            to_change = "Выключить"
        else:
            text = "Камера <b>выключена</b>"
            to_change = "Включить"

        await query.message.edit_text(text, reply_markup=markup.set_statecamera_buttons(callback_data.id, to_change), parse_mode='html')

    async def infocamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: InfoCamera) -> None:
        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=callback_data.id).first()

        text = f"""
Редактировать {camera.place} информацию

<b>IP:</b> {camera.ip}
<b>place:</b> {camera.place}
        """

        await query.message.edit_text(text, reply_markup=markup.set_infocamera_buttons(callback_data.id), parse_mode='html')

    async def ipeditcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: IpEditCamera, state: FSMContext) -> None:
        await query.message.answer('Введите IP камеры: ')
        await state.update_data(id=callback_data.id)
        await state.set_state(EditCameraState.ip)

    async def ipeditedcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        camera = await state.get_data()

        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=camera.get('id')).first()
        camera.ip = message.text

        await message.answer('Успешно!', reply_markup=markup.set_success_buttons(camera.id))

        await state.clear()

    async def placeeditcamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: PlaceEditCamera, state: FSMContext) -> None:
        await query.message.answer('Введите место, где установлена камера: ')
        await state.update_data(id=callback_data.id)
        await state.set_state(EditCameraState.place)

    async def placeeditedcamera(self: Bot, message: types.Message, state: FSMContext) -> None:
        camera = await state.get_data()

        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=camera.get('id')).first()
        camera.place = message.text

        await message.answer('Успешно!', reply_markup=markup.set_success_buttons(camera.id))

        await state.clear()

    async def deletecamera(self: Bot, query: types.callback_query.CallbackQuery, callback_data: DeleteCamera) -> None:
        camera: models.Camera = models.session.query(
            models.Camera).filter_by(id=callback_data.id).first()
        await query.message.edit_text(f'Ты успешно удалил камеру\n{camera.place}({camera.ip})', reply_markup=markup.set_backmycamera_buttons(), parse_mode='html')

        models.session.delete(camera)
        models.session.commit()
