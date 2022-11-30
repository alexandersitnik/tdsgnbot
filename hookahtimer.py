from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import data.variables

today = datetime.now()

class Hookah(StatesGroup):
    hookah = State()

async def hookah_start(message: types.Message, state: FSMContext):
    await Hookah.hookah.set()
    await message.answer('Установите время для таймера в формате: ЧЧ:ММ')
    async with state.proxy() as data:
        data['hookah'] = message.text

async def sethookahTimer(message: types.Message, state: FSMContext):
    try:
        formatedtime = datetime.strptime(message.text, '%H:%M')
        await message.answer('Таймер установлен на: ' + str(formatedtime.time()).split(':')[0] + ' ч. ' + str(formatedtime.time()).split(':')[1] + ' мин.')
        await state.finish()
    except:
        await message.answer('Неверный формат времени')
        return
    data.variables.hookahtime = formatedtime.replace(year=today.year, month=today.month, day=today.day)
    await state.finish()

async def getHookahTime(message: types.Message):
    if data.variables.hookahtime == None:
        await message.answer('Таймер не установлен. Алексей Витальевич, установите таймер')
    elif data.variables.hookahtime < datetime.now():
        await message.answer('Чужбанить трубку дьявола через: 0:00:00\n\nВозможно, вам стоит установить таймер заново. Обратитесь к Алексею Витальевичу')
    else:
        await message.answer('Чужбанить трубку дьявола через:\n'+ str(data.variables.hookahtime - datetime.now()).split('.')[0])

def register_handlers_hookah(dp: Dispatcher):
    dp.register_message_handler(hookah_start, commands='hookah')
    dp.register_message_handler(sethookahTimer, state=Hookah.hookah)
    dp.register_message_handler(getHookahTime, commands='shishatime')

