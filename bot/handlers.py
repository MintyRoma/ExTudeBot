import logging

from telegram.constants import ParseMode

from bot.db import calls
from bot.messages import Messages, Keyboards
from bot.states import DialogState
from bot.utils import search_user
from bot.db.models import Etude, ChatUser
import sendings


async def start(update, context):
    logging.info(f"User {update.message.from_user.id} inited conversation")
    await sendings.send_greeting(update, context)
    return DialogState.INIT

async def start_choose_callback(update, context):
    logging.info(f"After start selection from {update.effective_user.id} with callback {update.callback_query.data}")
    query = update.callback_query
    if query.data == "list_etudes":
        await sendings.send_list(update, context)
        return DialogState.LIST_ALL
    if query.data == "prepare_runtime":
        await sendings.send_wip(update, context)
        return DialogState.PREPARE_RUNTIME

async def list_all_callback(update, context):
    logging.info(f"List all menu from {update.effective_user.id} callback {update.callback_query.data} ")
    query = update.callback_query
    if query.data == "back":
        await update.callback_query.edit_message_text(Messages.greeting,
                                                      reply_markup=Keyboards.greeting)
        return DialogState.INIT
    if query.data == "add_etude":
        await update.callback_query.message.reply_text(Messages.create_etude, reply_markup=Keyboards.onlyback)
        await update.callback_query.answer()
        return DialogState.CREATE_ETUDE
    if query.data == "modify_etude":
        '''TODO'''
        await sendings.send_wip(update, context)
        pass
    if query.data == "delete_etude":
        '''TODO'''
        await sendings.send_wip(update, context)
        pass

async def create_etude_callback(update, context):
    logging.info(f"Create etude callback from {update.effective_user.id} callback")
    query = update.callback_query
    if query.data == "back":
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_text(Messages.list_etudes, reply_markup=Keyboards.list_etudes)
        return DialogState.LIST_ALL

async def create_etude_message_callback(update, context):
    logging.info(f"Create etude message from {update.effective_user.id} with name {update.message.text}")
    name = update.message.text
    context.user_data["new_name"] = name
    message = Messages.add_partners.replace("{name}", name).replace("{amount}",'0').replace("{members}","_Пока никто не добавлен_")
    await update.message.reply_text(message, reply_markup=Keyboards.onlyback, parse_mode=ParseMode.MARKDOWN)
    return DialogState.ADD_ROLES

async def addroles_callback(update, context):
    logging.info(f"User {update.effective_user.id} pressed button on ADD_ROLES state")
    query = update.callback_query
    if query.data == "back":
        context.user_data["new_name"] = None
        logging.info(f"User {update.effective_user.id} backed from on ADD_ROLES state")
        await update.callback_query.edit_message_text(Messages.list_etudes, reply_markup=Keyboards.list_etudes)
        return DialogState.LIST_ALL
    if query.data == "save_etude":
        etudename = context.user_data["new_name"]
        members = context.user_data["members"]
        author = update.effective_user.id
        logging.info(f"User {author} trying to save etude {etudename} with members {members}")
        try:
            await calls.create_etude(author, etudename, members)
        except Exception as e:
            logging.error(f"Creating ethude error: {e}")
            await update.callback_query.message.reply_text(Messages.error)
            return DialogState.INIT
        message = Messages.etude_created
        message = message.replace("{etude}", etudename)
        members_names = []
        for member in members:
            await calls.add_member(member)
            name = await search_user(member)
            members_names.append(name)
        message = message.replace("{members}", "\n".join(members_names))
        await update.callback_query.message.reply_text(message)
        await sendings.send_list(update, context)
        return DialogState.LIST_ALL


async def addroles_message_callback(update, context):
    logging.info(f"User {update.effective_user.id} tried to add member {update.message.text} in etude {context.user_data["new_name"]} ")
    memberquery = update.message.text

    members = []

    if "members" in context.user_data:
        members = context.user_data["members"]

    if memberquery.isnumeric():
        index = int(memberquery)-1
        if index < len(members):
            members.remove(members[index])
    else:
        if not memberquery.startswith("@"):
            memberquery = f"@{memberquery}"

        members.append(memberquery)

    members_names = []
    counter = 1
    for member in members:
        name = await search_user(member)
        if member != name:
            members_names.append(f"{counter}. {name} ({member})\n")
        else:
            members_names.append(f"{counter}. {member}\n")
        counter+=1

    message = Messages.add_partners
    message= message.replace("{name}", context.user_data["new_name"])
    message= message.replace("{amount}",str(len(members)))
    message= message.replace("{members}","".join(members_names))
    context.user_data["members"] = members
    await update.message.reply_text(message, reply_markup=Keyboards.save_etude if len(members)>0 else Keyboards.onlyback, parse_mode=ParseMode.MARKDOWN)
    return DialogState.ADD_ROLES