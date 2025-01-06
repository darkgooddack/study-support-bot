# StudySupportBot
 
### [StudySupportBot](https://t.me/mrkStudent2_bot) — это Telegram bot, который помогает студентам и абитуриентам находить ответы на вопросы, получать актуальную информацию, следить за мероприятиями и оставаться в курсе всех важных событий. 

## Технологии
Для разработки был выбран язык программирования Python 3.12 из-за наличия подходящих библиотек и удобного их использования. Использованные библиотеки:
- **Python**: основной язык программирования проекта.  
- **aiogram 3**: современный фреймворк для создания Telegram-ботов, поддерживающий асинхронную обработку.  
- **alembic**: инструмент для управления миграциями базы данных.  
- **pydantic**: библиотека для валидации данных и работы с типами, упрощающая создание моделей.  
- **SQLAlchemy**: ORM для работы с базами данных.  

## Установка проекта
### 1. Убедитесь, что на вашем компьютере установлен [Git](https://git-scm.com/).  

### 2. Перейдите в папку с проектом:
```
cd ваша папка проекта
```
### 3. Клонируйте репозиторий: 
```
git clone https://github.com/darkgooddack/study-support-bot.git .
```
## Запуск проекта

### 1. Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```
### 2. Установите зависимости:
```
pip install -r requirements.txt
```
### 3. Настройка переменных окружения
Создайте файл .env в корневом каталоге проекта и добавьте следующие переменные окружения:
    
```
# telegram
BOT_TOKEN=your_bot_token
YOUR_TELEGRAM_ID=your_telegram_id 

# postgreSQL
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_USER=your_db_user
DB_NAME=your_db_name
DB_PASS=your_db_pass
    
# other
ADMIN_ID=admin_id
BLOCKED_USERS_FILE=blocked_users.json
```
Убедитесь, что вы заменили BOT_TOKEN на ваш актуальный токен бота Telegram и указали корректный данные подключения к вашей БД.

### 4. Создание и инициализация базы данных

Создайте базу данных и выполните миграции:
```
alembic upgrade head
```
### 5. Запуск бота

После выполнения всех предыдущих шагов, вы можете запустить бота с помощью следующей команды:
```
python main.py
```

## Запуск с использованием Docker и Docker Compose

Для запуска проекта с Docker и Docker Compose выполните следующие шаги:

### Шаг 1: Убедитесь, что Docker и Docker Compose установлены
- Установите [Docker](https://www.docker.com/) на вашем компьютере.  
- Убедитесь, что установлен **Docker Compose**. В большинстве современных версий Docker Compose встроен в Docker.  

Проверьте установку командой:
```
docker --version
docker compose version
```
### Шаг 2. Клонируйте репозиторий:
```
git clone https://github.com/darkgooddack/study-support-bot.git .
```

### Шаг 3. Настройка переменных окружения
Создайте файл .env в корневой папке проекта и добавьте необходимые переменные окружения.
```
# telegram
BOT_TOKEN=your_bot_token
YOUR_TELEGRAM_ID=your_telegram_id

# postgreSQL
DB_HOST=your_db_host
DB_PORT=5433 # должен соответствовать значению в docker-compose.yml
DB_USER=your_db_user
DB_NAME=your_db_name
DB_PASS=your_db_pass

# other
ADMIN_ID=admin_id
BLOCKED_USERS_FILE=blocked_users.json
```
Убедитесь, что вы заменили BOT_TOKEN на ваш актуальный токен бота Telegram и указали корректный данные подключения к вашей БД.
### Шаг 4. Соберите и запустите контейнеры
Поднимите Docker Compose для создания и запуска контейнеров:
```
docker compose up --build
```

