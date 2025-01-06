from telegram.constants import ParseMode

from bot.db import calls
from bot.messages import Messages, Keyboards
from bot.utils import search_user


async def send_greeting(update, context):
    user = update.effective_user
    await calls.adduser_ifnotex(user)
    await update.message.reply_text(Messages.greeting,
                                    reply_markup=Keyboards.greeting)

async def send_list(update, context):
    user = update.effective_user.id
    etudes = await calls.get_etudes(user)
    full_etudes = {}
    for etude in etudes:
        members = await calls.get_members(etude.etudeid)
        full_etudes[etude.name] = members
    listing = ""
    number = 1
    for key, value in full_etudes.items():
        human_names = []
        for member in value:
            human_names.append(await search_user(member.username))
        listing += f"*{number}. {key}\n*" \
                   f"_{", ".join(human_names)}_\n"
        number += 1
    await update.callback_query.edit_message_text(
        text=Messages.list_etudes.replace("{etudes}", listing),
        reply_markup=Keyboards.list_etudes,
        parse_mode=ParseMode.MARKDOWN
    )

async def send_wip(update, context):
    await update.callback_query.message.reply_text(Messages.WIP)