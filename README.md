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
7) Открыть в Telegram бота https://t.me/SalesInfo_v1_bot
8) Запустить (/start)
9) Выполнить необходимые действия (добавление записи о продаже, запрос записей о продажах в диапазоне дат).

Работа связки тестировалась на локальной машине.
