from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import crud_functions
from keyborad import *
from aiogram.dispatcher import FSMContext
import asyncio
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()
get_all_products()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя ( только латинский алфавит')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message.text):
        await message.answer('Пользователь существует,введите другое имя')
        await RegistrationState.email.set()
        return
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация пропрошла успешно')
    await state.finish()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=kb2)
    await RegistrationState.username.set()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        await message.answer(f' Название:{i[1]} |  Описание:{i[2]} | Цена:{i[3]} ')
        with open(f'files/product{i[0]}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb3)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес + 6.25 * рост - 5 * возраст + 5')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (см)')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (кг)')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    weight = data['weight']
    growth = data['growth']
    colories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма колорий является {colories}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
