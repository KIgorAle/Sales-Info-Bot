import os

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import requests, re

#import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger()

updater = Updater("6208106902:AAEXkL7t40T954qw0CcZmMKYOpaJfnCFYMo", use_context=True)

SALES = range(1)

def sales_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'add_sale':
        # Удаляем сообщение с меню
        try:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
            return add_sale(update, context)
        except Exception:
            return None
    elif query.data == 'get_sales':
        # Удаляем сообщение с меню
        try:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
            return get_sales(update, context)
        except Exception:
            return None

# Функция для обработки команды /start (кнопки бота)
def sales_buttons(update: Update, context: CallbackContext):
    # context.user_data.clear()
    keyboard = [[InlineKeyboardButton("Добавить запись о продаже", callback_data='add_sale')],
                [InlineKeyboardButton("Получить отчет о продажах за период", callback_data='get_sales')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Я помогу тебе вести учет продаж. Что ты хочешь сделать?', reply_markup=reply_markup)
    return SALES

# Функция для отправки POST-запроса на добавление записи о продаже
def add_sale(update: Update, context: CallbackContext):
    #context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите данные о продаже (день, название продукта, количество, цена) в формате: "ГГГГ-ММ-ДД, Название без запятых, Целое число, рубли.копейки"')
    context.user_data['mode'] = 'add_sale'
    return SALES

# Функция для отправки GET-запроса на получение данных о продажах за период
def get_sales(update: Update, context: CallbackContext):
    #context.user_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите даты в формате "YYYY-MM-DD, YYYY-MM-DD"')
    context.user_data['mode'] = 'get_sales'
    return SALES

# Функция для проверки правильности ввода данных продажи
def is_valid_sale(sale_str):
    pattern = r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]), [\w\s]+, \d+, \d+\.\d{2}$"
    return re.match(pattern, sale_str) is not None

# Функция для проверки правильности ввода периода
def is_valid_dates(dates_str):
    pattern = r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]), (19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    return re.match(pattern, dates_str) is not None

# Функция для обработки данных от пользователя и отправки POST-запроса/GET-запроса на сервер
def handle_sales(update: Update, context: CallbackContext):
    try:
        if 'mode' in context.user_data and context.user_data['mode'] == 'add_sale':
            sale_str = update.message.text
            if is_valid_sale(sale_str):
                date, product, quantity, price = sale_str.split(', ')
                response = requests.post('http://127.0.0.1:5000/sales/',
                                         json={'date': date, 'product': product, 'quantity': quantity, 'price': price})
                if response.json()['success']:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=response.json()['message'])
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка при добавлении записи.')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Неверный формат данных.')
        elif 'mode' in context.user_data and context.user_data['mode'] == 'get_sales':
            dates_str = update.message.text
            if is_valid_dates(dates_str):
                start_date, end_date = dates_str.split(', ')
                response = requests.get('http://127.0.0.1:5000/sales/', params={'start_date': start_date, 'end_date': end_date})
                if response.json()['success']:
                    sales = response.json()['sales']
                    if len(sales) != 0:
                        message = ''
                        for sale in sales:
                            message += f"Дата: {sale['date']}, Название: {sale['product']}, Количество: {sale['quantity']}, Цена: {sale['price']}\n"
                        if len(message)>=4096:
                            filename = 'sales_report.txt'
                            with open(filename, 'w') as f:
                                f.write(message)
                            with open(filename, 'rb') as f:
                                context.bot.send_document(chat_id=update.effective_chat.id, document=f)
                            os.remove(filename)
                        else:
                            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Продаж в заданном диапазоне нет.')
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка при получении отчета о продажах.')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Неверный формат данных.')
    except requests.exceptions.ConnectionError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ошибка соединения с сервером. Попробуйте повторить позже.')
    return ConversationHandler.END

# Функция для отмены текущего диалога
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    #logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('До свидания! Ждем Вас снова.')
    return ConversationHandler.END

# Главная функция бота
def main():
    updater.dispatcher.add_handler(CommandHandler('start', sales_buttons))
    updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(sales_callback)],
        states={
            SALES: [
                MessageHandler(Filters.text, handle_sales)
            ]
        },
        fallbacks=[CallbackQueryHandler(sales_buttons)]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(sales_callback), group=1)
    updater.start_polling()
    updater.idle()

# Запускаем бота
if __name__ == '__main__':
    main()