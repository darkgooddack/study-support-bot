import json
from aiogram import types, Bot, exceptions
from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram import F
from app import keyboard
from app.keyboard import HELP_DICT, DOCS, SPECIALTIES
from data.crud import get_all_users
from data.database import async_session_factory
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from data.models import User
from data.database import get_db
from data import crud
from aiogram.types import CallbackQuery
from data.text import TRIGGER_RESPONSES
from config import settings

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    async for session in get_db():
        # Проверяем, есть ли пользователь в базе
        result = await session.execute(select(User).where(User.telegram_id == msg.from_user.id))
        user = result.scalars().first()

        if user:
            # Если пользователь уже существует, приветствуем его
            await msg.answer(
                f"Привет снова, {msg.from_user.full_name}! 👋",
                reply_markup=keyboard.get_main_keyboard()  # Отправляем главную клавиатуру
            )
        else:
            # Если пользователя нет в базе, предлагаем выбрать роль
            await msg.answer(
                f"Привет, {msg.from_user.full_name}! 👋\nВыберите вашу роль:",
                reply_markup=keyboard.get_role_keyboard()  # Отправляем клавиатуру для выбора роли
            )

# Обработка выбора роли
@router.callback_query(lambda c: c.data.startswith("role."))
async def handle_role_selection(callback: CallbackQuery):
    role = callback.data.split("role.")[1]  # Извлекаем роль из callback_data

    # Сохраняем пользователя с выбранной ролью
    async for session in get_db():
        await crud.add_user(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            role=role,
            session=session,
        )

    # Ответ пользователю
    await callback.message.answer(
        f"Спасибо! Ваша роль установлена: {role.capitalize()} ✅",
        reply_markup=keyboard.get_main_keyboard()  # Отправляем главную клавиатуру после установки роли
    )
    await callback.answer()

def load_blocked_users() -> dict:
    """Загрузка списка заблокированных пользователей из файла."""
    try:
        with open(settings.BLOCKED_USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_blocked_users(blocked_users: dict) -> None:
    """Сохранение списка заблокированных пользователей в файл."""
    with open(settings.BLOCKED_USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(blocked_users, file, indent=4, ensure_ascii=False)


# Загружаем список заблокированных пользователей
blocked_users = load_blocked_users()


@router.message(Command("block"))
async def block_user(message: Message):
    """Команда для блокировки пользователей."""
    admin_ids = [1741279318]  # Укажите ID администраторов
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /block <id или username>")
        return

    target = args[1]
    # Определяем, ID или username указан
    if target.isdigit():
        blocked_users[target] = True
    else:
        blocked_users[target] = True

    save_blocked_users(blocked_users)
    await message.answer(f"Пользователь `{target}` был заблокирован.")


@router.message(Command("unblock"))
async def unblock_user(message: Message):
    """Команда для разблокировки пользователей."""
    admin_ids = [1741279318]
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /unblock <id или username>")
        return

    target = args[1]
    if target in blocked_users:
        del blocked_users[target]
        save_blocked_users(blocked_users)
        await message.answer(f"Пользователь `{target}` был разблокирован.")
    else:
        await message.answer(f"Пользователь `{target}` не найден в списке блокировки.")


@router.message(Command("sendmessage_all"))
async def send_message_to_all_users(message: types.Message, bot: Bot):
    async for session in get_db():
        if message.from_user.id != 1741279318:
            await message.answer("⛔ У вас нет доступа к этой команде.")
            return

        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("⚠️ Использование: /sendmessage_all <сообщение>")
            return

        broadcast_message = args[1]

        try:
            users = await get_all_users(session)
            failed_users = []
            for user in users:
                try:
                    await bot.send_message(chat_id=user.telegram_id, text=broadcast_message, parse_mode="HTML")
                except TelegramForbiddenError:
                    print(f"⚠️ Пользователь {user.user_id} заблокировал бота.")
                except Exception as e:
                    print(f"⚠️ Не удалось отправить сообщение пользователю {user.telegram_id}. Ошибка: {e}")
                    failed_users.append(user.telegram_id)

            await message.answer("✅ Сообщение отправлено всем пользователям.")
            if failed_users:
                await message.answer(f"⚠️ Не удалось отправить сообщение {len(failed_users)} пользователям.")

        except Exception as e:
            await message.answer(f"❌ Ошибка: {e}")


@router.message(Command("sendmessage"))
async def send_message_to_user(message: Message, bot: Bot):
    user_id = message.from_user.id
    username_sender = message.from_user.username or str(user_id)

    if user_id != 1741279318:

        await message.reply("⛔ У вас нет доступа к этой команде.")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("⚠️ Использование: /sendmessage @username сообщение или /sendmessage user_id сообщение")
        return

    identifier = args[1]
    message_text = args[2]

    async for session in get_db():
        try:
            if identifier.startswith("@"):
                username = identifier.lstrip("@")
                query = select(User.telegram_id).where(User.username == username)
            else:
                query = select(User.telegram_id).where(User.telegram_id == int(identifier))

            result = await session.execute(query)
            target_user = result.scalar()

            if target_user:
                await bot.send_message(chat_id=target_user, text=message_text, parse_mode="HTML")
                await message.reply(f"✅ Сообщение отправлено пользователю {identifier}.")

                if user_id != 1741279318:
                    notification_text = (
                        f"Администратор @{username_sender} отправил сообщение пользователю {identifier}:\n{message_text}"
                    )
                    await bot.send_message(chat_id=1741279318, text=notification_text, parse_mode="HTML")
            else:
                await message.reply(f"⚠️ Не удалось найти пользователя {identifier}.")

        except Exception as ex:
            await message.reply(f"❌ Произошла ошибка: {ex}")


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "🔙 Назад")
async def menu(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())

@router.message(F.text == "✅ Информация")
async def info(msg: Message):
    await msg.answer(
         "🔔 <b>Сессия приближается!</b>\n\n"
        "👱‍♂️ Информация актуальна для студентов.\n\n"
        "💻 Мы знаем, что сессия — это сложно, волнительно и порой даже страшно. Но именно в такие моменты нужно проявить упорство и стремление, чтобы достичь высоких результатов. Каждый экзамен и зачет — возможность показать, на что вы способны!\n\n"
        "🗓 <b>Даты экзаменов и зачетов</b> будут доступны на сайте:\n"
        "👉 <a href='https://mrk-bsuir.by/ru/explore/search/936/'>mrk-bsuir.by</a>\n\n"
        "👁 Помните, что вы не одни! При возникновении вопросов вы всегда можете обратиться к нашему психологу.\n\n"
        "🍀 Каждый из вас способен на большее, чем думает! Желаем успешной и легкой сессии! 🌟\n\n"
        "🔔 <b>For English version:</b> 👉 <a href='https://telegra.ph/The-interim-exams-period-is-coming-12-16'>Press here</a>",
        parse_mode="HTML",
        reply_markup=keyboard.return_keyboard()
    )


@router.message(F.text == "🌐 Абитуриентам")
async def prospects(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_prospects_keyboard())


@router.message(F.text == "👩🏻‍🎓 Студентам")
async def students(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_students_keyboard())

@router.message(F.text == "🆘 В помощь учащимся")
async def help_student(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_help_students_keyboard())

@router.callback_query(F.data.in_(HELP_DICT.keys()))
async def handle_callback(callback: CallbackQuery):
    response_text = HELP_DICT[callback.data]
    await callback.message.answer(response_text)
    await callback.answer()


@router.message(F.text == "📲 Техническая поддержка")
async def tech_support(msg: Message):
    await msg.answer(
        "Наш бот находится в стадии постоянного развития, что может привести к временным сбоям в его работе. "
        'Если у вас возникли вопросы или проблемы, пожалуйста, свяжитесь с <a href="https://t.me/lost_wandering">администратором</a> для получения поддержки.',
        parse_mode="HTML",
        reply_markup=keyboard.get_main_keyboard()
    )


@router.message(F.text == "❔ Общие вопросы")
async def general_questions(msg: Message):
    await msg.answer('Задайте ваш вопрос, и я постараюсь на него ответить.', reply_markup=keyboard.get_prospects_keyboard())


@router.message(F.text == "🎯 Поступление")
async def entrance(msg: Message):
    await msg.answer('Выберите один из вариантов:', reply_markup=keyboard.get_entrance_keyboard())


@router.message(F.text == "🧑🏻‍💻 Обучение")
async def training(msg: Message):
    await msg.answer('Выберите один из вариантов:', reply_markup=keyboard.get_training_keyboard())


@router.message(F.text == "📌 Проходные баллы")
async def passing_scores(msg: Message):
    await msg.answer('Ссылка на проходные баллы прошлых лет и ожидания на 2025', reply_markup=keyboard.get_entrance_keyboard())


@router.message(F.text == "📁 Документы")
async def passing_scores(msg: Message):
    await msg.answer('Документы для абитуриентов:', reply_markup=keyboard.get_docs_keyboard())


@router.message(F.text == "🧩‍ Специальности")
async def specialties(msg: Message):
    await msg.answer('Наши специальности:', reply_markup=keyboard.get_specialties_keyboard())


@router.callback_query(F.data.startswith("doc_"))
async def handle_docs_callback(callback: CallbackQuery):
    button_text = callback.data[len("doc_"):]
    document_text = DOCS.get(button_text, "Документ не найден")
    await callback.message.answer(f"Вы выбрали: {document_text}")
    await callback.answer()


@router.callback_query(F.data.startswith("spec_"))
async def handle_specialties_callback(callback: CallbackQuery):
    button_text = callback.data[len("spec_"):]
    specialty_text = SPECIALTIES.get(button_text, "Специальность не найдена")
    await callback.message.answer(f"{specialty_text}")
    await callback.answer()


@router.message(F.text == "📋 Зачисление")
async def enrollment(msg: Message):
    await msg.answer('Текст зачисления:', reply_markup=keyboard.get_prospects_keyboard())


@router.message(F.text == "🙈 Закрытие сессии")
async def students(msg: Message):
    await msg.answer(
        "Закрытие сессии — это важный этап в учебном процессе. Вот что нужно знать:\n\n"
        "1️⃣ **Сроки сдачи:** Обязательно уточните дату окончания сессии в деканате или в своем расписании.\n\n"
        "2️⃣ **Аттестации и зачеты:** Проверьте, сданы ли все зачеты и экзамены. Если есть задолженности, обратитесь к преподавателю или куратору группы.\n\n"
        "3️⃣ **Пересдачи:** В случае несданных дисциплин уточните сроки пересдач. Они проводятся по согласованию с преподавателем.\n\n"
        "❗ Не забывайте: если сессия не будет закрыта в срок, это может повлиять на получение стипендии или допуск к следующему семестру.\n\n"
        "Если у вас возникли вопросы, обратитесь в учебную часть или к своему куратору.",
        reply_markup=keyboard.get_training_keyboard()
    )


@router.message(F.text == "📖 Оплата обучения")
async def students(msg: Message):
    await msg.answer(
        "Оплата обучения — это обязательная часть для студентов на коммерческой основе. Вот основные моменты:\n\n"
        "1️⃣ **Сроки оплаты:** Оплата за семестр или год должна быть внесена до установленной даты. Проверьте свой договор или свяжитесь с бухгалтерией учебного заведения.\n\n"
        "2️⃣ **Реквизиты:** Для перевода средств используйте реквизиты, указанные в договоре. Обратите внимание на точность ввода данных.\n\n"
        "3️⃣ **Частичная оплата:** Некоторые учебные заведения предоставляют возможность оплаты частями. Уточните условия в бухгалтерии.\n\n"
        "4️⃣ **Льготы:** Если у вас есть право на льготы или вы оформляете рассрочку, обратитесь в деканат для получения дополнительных инструкций.\n\n"
        "❗ **Важно:** При задержке оплаты возможен временный отстранение от занятий или недопуск к экзаменационной сессии.",
        reply_markup=keyboard.get_training_keyboard()
    )


@router.message(F.text == "🔍 Стипендии")
async def students(msg: Message):
    await msg.answer(
        "Стипендия — это денежная поддержка, предоставляемая студентам на конкурсной основе или за академические достижения. Вот основные категории стипендий:\n\n"
        "1️⃣ **Академическая стипендия:** Выплачивается студентам, успешно закрывающим сессию без троек. Размер зависит от учебного заведения.\n\n"
        "2️⃣ **Социальная стипендия:** Доступна студентам из социально незащищенных категорий (например, сиротам или многодетным). Для получения обратитесь в отдел стипендий с подтверждающими документами.\n\n"
        "3️⃣ **Повышенная стипендия:** За особые достижения в учебе, науке, спорте или общественной деятельности. Требует подачи заявки и рекомендаций.\n\n"
        "4️⃣ **Гранты и внешние стипендии:** Возможность получения дополнительной финансовой поддержки от сторонних организаций.\n\n"
        "❗ **Совет:** Для получения стипендии важно своевременно сдавать сессию и следить за успеваемостью.",
        reply_markup=keyboard.get_training_keyboard()
    )


@router.message(F.text == "🎬 Внеучебная деятельность")
async def students(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_projects_keyboard())


@router.message(F.text == "Найти 👩🏼‍💻")
async def students(msg: Message):
    await msg.answer(
        "Вы можете заполнить карточку разработчика, указав данные о себе, а также выбрать разработчика для вашего проекта из доступной базы. "
        "Карточку можно редактировать или скрыть из видимости.",
        reply_markup=keyboard.get_search_keyboard()
    )
    await msg.answer("Выберите направление:", reply_markup=keyboard.get_direction_keyboard())


@router.callback_query(lambda c: c.data.startswith("dir."))
async def handle_direction_callback(callback_query: CallbackQuery):
    direction = callback_query.data.split(".")[1]
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).filter(User.visibility == True)
        )
        users = result.scalars().all()

    if users:
        filtered_users = [user for user in users if user.direction == direction]

        if filtered_users:
            users_info = "\n\n".join([
                f"Username: <a href='https://t.me/{user.username}'>{user.username}</a>\n"
                f"О себе: {user.about or 'Не указано'}\n"
                f"GitHub: {user.github or 'Не указано'}\n"
                f"LinkedIn: {user.linkedin or 'Не указано'}"
                for user in filtered_users
            ])
            await callback_query.message.answer(f"Пользователи с направлением {direction}:\n\n{users_info}")
        else:
            await callback_query.message.answer(f"Нет пользователей с направлением {direction}.")
    else:
        await callback_query.message.answer("Нет пользователей с видимостью.")


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


async def get_user_info(session, telegram_id: int) -> str | None:
    user = await crud.get_user(session, telegram_id)
    if not user:
        return None

    user_info = (
        f"username: {user.username or 'Не указано'}\n"
        f"Направление: {user.direction or 'Не указано'}\n"
        f"О себе: {user.about or 'Не указано'}\n"
        f"GitHub: {user.github or 'Не указано'}\n"
        f"LinkedIn: {user.linkedin or 'Не указано'}\n"
        f"Видимость: {'виден' if user.visibility else 'не виден'}\n\n"
    )
    return user_info


@router.message(F.text == "🪪 Профиль")
async def settings(message: types.Message):
    telegram_id = message.from_user.id

    async with async_session_factory() as session:
        user_info = await get_user_info(session, telegram_id)
        if not user_info:
            await message.reply("Пользователь не найден!")
            return

        await message.answer(user_info, reply_markup=get_profile_keyboard())


@router.callback_query(lambda c: c.data == "edit_visibility")
async def change_visibility(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        async with async_session_factory() as session:
            user = await crud.get_user(session, user_id)
            if not user:
                await callback_query.message.reply("Пользователь не найден!")
                return

            new_visibility = not user.visibility
            await crud.update_visibility(user_id, new_visibility, session)

            user_info = await get_user_info(session, user_id)
            if not user_info:
                await callback_query.message.reply("Пользователь не найден!")
                return

            await callback_query.message.edit_text(
                f"{user_info}",
                reply_markup=get_profile_keyboard()
            )
    except Exception as e:
        await callback_query.message.reply(f"Произошла ошибка: {str(e)}")


def get_direction_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=direction.capitalize(), callback_data=f"set_direction_{direction}")]
            for direction in keyboard.DIRECTIONS
        ]
    )


@router.callback_query(lambda c: c.data == "edit_direction")
async def choose_direction(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Выберите направление:", reply_markup=get_direction_keyboard())


@router.callback_query(lambda c: c.data.startswith("set_direction_"))
async def set_direction(callback_query: types.CallbackQuery):
    direction = callback_query.data.split("_")[-1]
    user_id = callback_query.from_user.id

    if direction not in keyboard.DIRECTIONS:
        await callback_query.answer("Неверное направление.", show_alert=True)
        return

    async for session in get_db():
        success = await crud.update_user_profile(user_id, "direction", direction, session)

        if success:
            await callback_query.answer(f"Направление успешно обновлено на '{direction}'.")
        else:
            await callback_query.answer("Не удалось обновить направление. Попробуйте снова.")


    user_info = await get_user_info(session, user_id)
    if not user_info:
        await callback_query.message.reply("Пользователь не найден!")
        return

    await callback_query.message.edit_text(
    f"{user_info}",
            reply_markup=get_profile_keyboard()
    )


class EditProfile(StatesGroup):
    edit_about = State()
    edit_github = State()
    edit_linkedin = State()

VALID_FIELDS = {"about", "github", "linkedin"}

@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_profile_field(callback_query: types.CallbackQuery, state: FSMContext):
    field = callback_query.data[5:]

    if field not in VALID_FIELDS:
        await callback_query.answer("Неверное поле для редактирования.", show_alert=True)
        return

    await state.set_state(f'EditProfile:edit_{field}')
    await callback_query.message.answer(f"Введите новое значение для поля: {field}")


@router.message(StateFilter("EditProfile:edit_about", "EditProfile:edit_github", "EditProfile:edit_linkedin"))
async def handle_new_value(msg: types.Message, state: FSMContext):
    state_name = await state.get_state()
    print(f"Current state: {state_name}")

    if state_name and state_name.startswith("EditProfile:edit_"):
        field_name = state_name.split(":")[1][5:]
        new_value = msg.text
        print(f"Updating field: {field_name} with value: {new_value}")

        async with async_session_factory() as session:
            user_id = msg.from_user.id

            success = await crud.update_user_profile(user_id, field_name, new_value, session)
            print(f"Update success: {success}")

            if success:
                user_info = await get_user_info(session, user_id)
                if not user_info:
                    await msg.reply("Пользователь не найден!")
                    return

                await msg.answer(
                    f"{user_info}",
                    reply_markup=get_profile_keyboard()
                )
                await state.clear()
            else:
                await msg.answer(f"Не удалось обновить поле '{field_name}'. Попробуйте снова.")
    else:
        await msg.answer("Ошибка. Пожалуйста, выберите поле для редактирования.")


@router.message()
async def handle_unknown_query(message: Message, bot: Bot):
    text = message.text.lower()

    for trigger, response in TRIGGER_RESPONSES.items():
        if trigger in text:
            await message.answer(
                response,
                parse_mode="HTML",
            )
            return

    user = message.from_user
    user_id = user.id
    username = user.username if user.username else f"ID: {user_id}"
    question = message.text

    try:
        await bot.send_message(
            chat_id=1741279318,
            text=f"📩 Вопрос от пользователя @{username}: {question}",
            parse_mode="HTML"
        )
        await message.answer("Ваш вопрос отправлен администратору. Спасибо!")
    except Exception as e:
        await message.answer("❌ Произошла ошибка при отправке вашего вопроса. Попробуйте позже.")


