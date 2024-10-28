from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Рассчитать'),
        KeyboardButton(text='Информация'),
        KeyboardButton(text="Купить"),
        KeyboardButton(text='Регистрация')]], resize_keyboard=True)

kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать колории', callback_data='colories')],
        [InlineKeyboardButton(text='Формула рассчёта', callback_data='formulas')]])

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]])
