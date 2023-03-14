# Sales-Info-Bot
1) pythonFlaskService - HTTP сервис на Python (Flask), который имеет 2 метода:
  ● добавить запись о продаже
  ● получить данные о продажах за период

2) pythonTelegramBot - Telegram-бот на Python имеющий две кнопки:
  ● Внести данные о продаже
  ● Получить отчет о продажах за период
  
3) pythonSQLiteBaseGenerator - Python скрипт для генерации и заполнения случанными данными SQLite базы данных sales.db.

План:
1) Скопировать main.py из pythonFlaskService на сервер.
2) Сгенерировать БД запустив main.py из pythonSQLiteBaseGenerator.
3) Скопировать полученный файл sales.db на сервер с pythonFlaskService.
4) Скопировать bot.py из pythonTelegramBot на сервер.
5) Запустить main.py на сервере pythonFlaskService.
6) Запустить bot.py на сервере pythonTelegramBot.
>  Если возникнит ошибка вида:
>  ```sh
>   <Traceback (most recent call last):
>     File "C:\...\pythonTelegramBot\bot.py", line 5, in <module> updater = Updater("6208106902:AAEXkL7t40T954qw0CcZmMKYOpaJfnCFYMo", use_context=True)
>     TypeError: __init__() got an unexpected keyword argument 'use_context' >
>  ```
>  Решить её можно вручную задав версию python-telegram-bot, я использовал 13.7, соответственно используйте команду: pip install python-telegram-bot==13.7
7) Открыть в Telegram бота https://t.me/SalesInfo_v1_bot
8) Запустить (/start)
9) Выполнить необходимые действия (добавление записи о продаже, запрос записей о продажах в диапазоне дат).

Работа связки тестировалась на локальной машине.
