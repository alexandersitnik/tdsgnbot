import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text

class generateCheck(StatesGroup):
    projectName = State()
    lastWeekResults = State()
    nextWeekPlans = State()

# Первый шаг менеджерского среза
async def checkpoint(message: types.Message):
    await generateCheck.projectName.set()
    await message.reply("Введи название проекта: ")

async def stop_check(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

# Ловим первый ответ
async def checkpoint_projectName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['projectName'] = message.text
    await generateCheck.next()
    await message.reply("Введи результаты прошлой недели: ")

async def checkpoint_lastWeekResults(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastWeekResults'] = message.text
    await generateCheck.next()
    await message.reply("Введи планы на следующую неделю: ")

async def checkpoint_nextWeekPlans(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nextWeekPlans'] = message.text
    
    async with state.proxy() as data:
        await message.reply(f"Название проекта: {data['projectName']} \nРезультаты прошлой недели: {data['lastWeekResults']} \nПланы на следующую неделю: {data['nextWeekPlans']}")
    await state.finish()

def register_handlers_check(dp : Dispatcher):
    dp.register_message_handler(checkpoint, commands=['checkpoint'])
    dp.register_message_handler(stop_check, commands=['stop'], state='*')
    dp.register_message_handler(stop_check, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(checkpoint_projectName, state=generateCheck.projectName)
    dp.register_message_handler(checkpoint_lastWeekResults, state=generateCheck.lastWeekResults)
    dp.register_message_handler(checkpoint_nextWeekPlans, state=generateCheck.nextWeekPlans)