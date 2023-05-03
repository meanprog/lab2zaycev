import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import data
import telebot
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext



bot = telebot.TeleBot = Bot(token="6162677846:AAFyrYUIxkw--mOfKI87D_HGo0UiS_4vJNs")
dispatcher = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    fio = State()

@dispatcher.message_handler(commands=['start'])#(c(start))
async def cmd_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2) #row_width=2
    answer_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    answer_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.add(answer_yes, answer_no)

    await bot.send_message(message.chat.id, "Ого! Вы записываетесь на марафон! Вы же сюда и собирались зайти, да, {0.first_name}?".format(message.from_user),reply_markup=markup, parse_mode='html')

@dispatcher.callback_query_handler(lambda call: call.data=="yes" or call.data=="no")
async def yes_or_no(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == "yes":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                await man_or_woman(call.message)
            elif call.data == "no":
                await bot.send_message(call.message.chat.id,"Я так и думал...")
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    except Exception as e:
        print(repr(e))



def write_to_excel(column, user_info):
    print(data.row)
    print(user_info)
    data.df.at[data.row, column] = user_info
    data.print_to_database(data.df)


async def get_fio(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите ФИО:')
    await Form.fio.set() # Устанавливаем состояние

@dispatcher.message_handler(state=Form.fio) # Принимаем состояние
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as fio_data: # Устанавливаем состояние ожидания
        fio_data['fio'] = message.text
        write_to_excel('ФИО', message.text)
        await bot.send_message(message.chat.id,"Вы записаны на ближайшую дату - 7 июня. Место встречи: политех".format(message.from_user), parse_mode='html')
        print(message.text)
        await state.finish()
        data.row += 1



async def man_or_woman(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    answer_man = types.InlineKeyboardButton('Мужчина', callback_data='man')
    answer_womanhahaha = types.InlineKeyboardButton('Женщина', callback_data='woman')
    markup.add(answer_man, answer_womanhahaha)
    await bot.send_message(message.chat.id,"Тогда давайте уточним некоторую информацию. Ваш пол?".format(message.from_user),reply_markup=markup, parse_mode='html')


@dispatcher.callback_query_handler(lambda call: call.data=="man" or call.data=="woman")
async def man_or_woman_answer(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == "man":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Мужчина"
                write_to_excel('Пол', user_info)
                await years_old(call.message)
            elif call.data == "woman":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Женщина"
                write_to_excel('Пол', user_info)
                await years_old(call.message)

    except Exception as e:
        print(repr(e))



async def years_old(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    answer_old = types.InlineKeyboardButton('Старше 18', callback_data='older18')
    answer_young = types.InlineKeyboardButton('Младше 18', callback_data='under18')
    markup.add(answer_old, answer_young)
    await bot.send_message(message.chat.id, "Возрастная категория:".format(message.from_user),reply_markup=markup, parse_mode='html')


@dispatcher.callback_query_handler(lambda call: call.data=="older18" or call.data=="under18")
async def years_old_answer(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == "older18":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Старше 18"
                write_to_excel('Возраст', user_info)
                await types_marathon(call.message)
            elif call.data == "under18":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Младше 18"
                write_to_excel('Возраст', user_info)
                await types_marathon(call.message)

    except Exception as e:
        print(repr(e))

async def types_marathon(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    sprint = types.InlineKeyboardButton("🏃‍♂️ Спринт", callback_data='marathon_sprint')
    mid_dist_run = types.InlineKeyboardButton("🏃‍♂️ Бег на среднюю дистанцию", callback_data='marathon_mid_dist_run')
    half_marathon = types.InlineKeyboardButton("🏃‍♂️ Полумарафон", callback_data='marathon_half_marathon')
    marathon = types.InlineKeyboardButton("🏃‍♂️ Марафон",  callback_data='marathon_marathon')
    ultra_marathon = types.InlineKeyboardButton("🏃‍♂️ Ультрамарафон",  callback_data='marathon_ultra_marathon')
    markup.add(sprint, mid_dist_run, half_marathon, marathon, ultra_marathon)
    await bot.send_message(message.chat.id, "Выберите вид забега:\nСпринт (100 м)\nБег на среднюю дистанцию (1 км)\nПолумарафон (25 км)\nМарафон (42 км 195 м)\nУльтрамарафон (100 км)".format(message.from_user), reply_markup=markup,parse_mode='html')

@dispatcher.callback_query_handler(text = "marathon_sprint" or "marathon_mid_dist_run" )
async def types_marathon_answer1(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == "marathon_sprint":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Спринт"
                write_to_excel('Вид забега', user_info)
                await get_fio(call.message)
            elif call.data == "marathon_mid_dist_run":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Бег на среднюю дистанцию"
                write_to_excel('Вид забега', user_info)
                await get_fio(call.message)
    except Exception as e:
        print(repr(e))

@dispatcher.callback_query_handler(text = "marathon_half_marathon" or "marathon_marathon")
async def types_marathon_answer2(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == "marathon_half_marathon":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Полумарафон"
                write_to_excel('Вид забега', user_info)
                await get_fio(call.message)
            elif call.data == "marathon_marathon":
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                user_info = "Марафон"
                write_to_excel('Вид забега', user_info)
                await get_fio(call.message)
    except Exception as e:
        print(repr(e))


@dispatcher.callback_query_handler(text = "marathon_ultra_marathon")
async def types_marathon_answer3(call: types.CallbackQuery):
    try:
        if call.data == "marathon_ultra_marathon":
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            user_info = "Ультрамарафон"
            write_to_excel('Вид забега', user_info)
            await get_fio(call.message)


    except Exception as e:
        print(repr(e))

async def main():
    await dispatcher.start_polling(bot)

#if __name__ == "__main__":
 #   asyncio.run(main())
