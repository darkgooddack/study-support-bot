from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import data.text as data

def get_role_keyboard():
    roles = [
        ("Студент", "student"),
        ("Абитуриент", "prospect"),
        ("Преподаватель", "teacher"),
        ("Родитель", "parent"),
        ("Другое", "other"),
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=role_name, callback_data=f"role.{role_key}")]
            for role_name, role_key in roles
        ]
    )
    return keyboard

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Информация"), KeyboardButton(text="🌐 Абитуриентам")],
            [KeyboardButton(text="👩🏻‍🎓 Студентам"), KeyboardButton(text="📲 Техническая поддержка")],
        ],
        resize_keyboard=True
    )


def get_prospects_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❔ FAQ"), KeyboardButton(text="🎯 Поступление")],
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="📋 Зачисление")],
        ],
        resize_keyboard=True
    )

def get_students_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Внеучебная деятельность"), KeyboardButton(text="🧑🏻‍💻 Обучение")],
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🆘 В помощь учащимся")],
        ],
        resize_keyboard=True
    )

HELP_DICT = {
    "Расписание занятий": "Расписание занятий можно найти в личном кабинете студента на сайте университета или уточнить в деканате. Если произошли изменения в расписании, их обычно сообщают через официальные группы в социальных сетях или на сайте. Для вопросов, связанных с расписанием, обратитесь к куратору группы.",
    "Библиотека и доступ к учебникам": "Библиотека предоставляет доступ к учебникам и научной литературе как в печатном, так и в электронном виде. Для пользования библиотекой необходимо оформить читательский билет или использовать студенческий. Электронные учебники доступны через портал университета. Если у вас нет доступа, обратитесь в библиотеку или службу поддержки.",
    "Как получить справку об обучении?": "Справку об обучении можно заказать через личный кабинет студента или в учебной части. Обычно на оформление уходит 2-3 рабочих дня. Справка может понадобиться для военкомата, места работы или других целей. Для уточнения сроков и процедуры обратитесь в деканат.",
    "Пересдачи экзаменов": "Если вы не сдали экзамен с первого раза, вам нужно уточнить дату пересдачи у преподавателя или в учебной части. Пересдачи проводятся по графику, который утверждается деканатом. Учтите, что количество попыток может быть ограничено. Важно заранее подготовиться и уточнить все детали у своего куратора или преподавателя. 📝",
    "Академический отпуск": "Академический отпуск может быть предоставлен по уважительным причинам: медицинские показания, семейные обстоятельства и т.д. Для оформления необходимо подать заявление в деканат, приложив подтверждающие документы. 📄Сроки отпуска и порядок восстановления после него регламентируются внутренними правилами университета. ",
}

# Функция для создания клавиатуры
def get_help_students_keyboard():
    builder = InlineKeyboardBuilder()
    for button_text in HELP_DICT.keys():
        builder.add(InlineKeyboardButton(text=button_text, callback_data=button_text))
    builder.adjust(1)  # Каждая кнопка в отдельной строке
    return builder.as_markup()

def get_projects_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти 👩🏼‍💻"), KeyboardButton(text="🐈 GitHub")],
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🍭 Хакатон")],
        ],
        resize_keyboard=True
    )

DIRECTIONS = ["Frontend", "Backend", "ML", "Devops", "PM"]
def get_direction_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=direction, callback_data=f"dir.{direction}")]
            for direction in DIRECTIONS
        ]
    )

def get_search_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🪪 Профиль")],
        ],
        resize_keyboard=True
    )

def get_profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Направление", callback_data="edit_direction")],
            [InlineKeyboardButton(text="О себе", callback_data="edit_about")],
            [InlineKeyboardButton(text="GitHub", callback_data="edit_github")],
            [InlineKeyboardButton(text="LinkedIn", callback_data="edit_linkedin")],
            [InlineKeyboardButton(text="Видимость", callback_data="edit_visibility")],
        ]
    )

def generate_cuisine_keyboard():
    cuisines = ["Frontend", "Backend", "ML", "Devops", "PM"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cuisine, callback_data=f"cuisine_{cuisine}")]
            for cuisine in cuisines
        ]
    )
    return keyboard

def return_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

#################################################################################################

def get_entrance_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📌 Проходные баллы"), KeyboardButton(text="📁 Документы")],
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🧩‍ Специальности")],
        ],
        resize_keyboard=True
    )

def get_training_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Оплата обучения"), KeyboardButton(text="🔍 Стипендии")],
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🙈 Закрытие сессии")],
        ],
        resize_keyboard=True
    )

# Словарь документов
DOCS = {
    'Списки зачисленных': data.lists_of_enrolled,
    'Бюджетная форма': data.budget_information,
    'Платная форма': data.information_paid,
    'Дистанционная форма': data.remotely,
    'Оплата обучения': data.tuition_fees,
    'Выдача документов': data.issuance_of_documents
}

# Словарь специальностей
SPECIALTIES = {
    "РиСПОИС": data.rispois,
    "ТЭЭУ": data.teey,
    "ПЭУ": data.peu,
    "ПМУ": data.pmu,
    "ПИМиН": data.pimin,
    "ТОИБ": data.toib,
    "ТЭСВТ": data.tesvt
}
#
# FAQ = {
#     "Расписание занятий?": data.schedule,
#     "Даты экзаменов или сессии?": data.session,
#     "Где узнать о кружках?": data.courses,
#     "Мероприятиях в колледже?": data.events,
#     "Как добраться до колледжа?": data.way,
# }
#
#
# def get_faq_keyboard():
#     builder = InlineKeyboardBuilder()
#     for button_text in FAQ.keys():
#         builder.add(InlineKeyboardButton(text=button_text, callback_data=f"faq_{button_text}"))
#     builder.adjust(1)
#     return builder.as_markup()


# Функция для создания клавиатуры для DOCS
def get_docs_keyboard():
    builder = InlineKeyboardBuilder()
    for button_text in DOCS.keys():
        # Добавляем уникальный префикс doc_ для callback_data
        builder.add(InlineKeyboardButton(text=button_text, callback_data=f"doc_{button_text}"))
    builder.adjust(1)
    return builder.as_markup()

# Функция для создания клавиатуры для SPECIALTIES
def get_specialties_keyboard():
    builder = InlineKeyboardBuilder()
    for button_text in SPECIALTIES.keys():
        # Добавляем уникальный префикс spec_ для callback_data
        builder.add(InlineKeyboardButton(text=button_text, callback_data=f"spec_{button_text}"))
    builder.adjust(1)
    return builder.as_markup()