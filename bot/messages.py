from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Messages:
    greeting = "👋Привет!\n" \
               "Этот бот предназначен для составления списка этюдов.\n" \
               "Вот доступные команды:"

    list_etudes = "Список созданных тобою этюдов:\n"\
                  "{etudes}"

    prepare_runtime = "Укажи количество этюдов для создания очереди"

    create_etude = "Дай название этюду"

    add_partners = "Добавь участника этюда (вставь его никнейм с или без @)\n\n"\
                    "📃*Этюд:* {name}\n"\
                    "🙋*Участников:* {amount}\n"\
                    "{members}\n"\
                    "Если участник указан без имени - это значит, что он еще ни разу не открывал бота\n"\
                    "Чтобы удалить участника, напиши его номер"

    etude_created = "Этюд успешно добавлен\n"\
                    "📃*Этюд*: {etude}\n"\
                    "🙋*Участники*: \n{members}"

    error = "😵Бип-буп\n"\
            "Произошла ошибка. Информация о ней уже передана и возможно ее скоро исправят\n"\
            'Попробуй повторить запрос позже'

    WIP = "😶‍🌫️Упс...\n"\
          "Пока данный функционал не реализован. Скоро допилю"

class Keyboards:
    onlyback = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️Назад", callback_data="back")]
    ])

    greeting = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏁Начать прогоны", callback_data="prepare_runtime")],
        [InlineKeyboardButton("📃Список этюдов", callback_data="list_etudes")]
    ])

    list_etudes = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕Добавить этюд", callback_data="add_etude")],
        [InlineKeyboardButton("🖊️Редактировать этюд", callback_data="modify_etude")],
        [InlineKeyboardButton("🗑️Удалить этюд", callback_data="delete_etude")],
        [InlineKeyboardButton("⬅️Назад", callback_data="back")],
    ])

    save_etude = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅Сохранить", callback_data="save_etude")],
        [InlineKeyboardButton("⬅️Назад", callback_data="back")],
    ])