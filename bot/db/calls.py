import logging

from telegram import User
from bot.db.models import *


def initdb():
    db.connect()
    logging.info("Creating DB schema")
    db.create_tables([ChatUser], safe=True)
    db.create_tables([Etude], safe=True)
    db.create_tables([Memberships], safe=True)
    db.close()

async def adduser_ifnotex(user: User):
    '''
    Update user information based on TG ID
    :param user:
    :return:
    '''
    db.connect()
    logging.info(f"Adding user {user.id} to DB")
    usr, created = ChatUser.get_or_create(
        defaults={
            'tg_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    )
    if not created:
        logging.info(f"User {user.id} already exists, modifying")
        usr.tg_id = user.id
        usr.username = user.username
        usr.first_name = user.first_name
        usr.last_name = user.last_name
        usr.save()
    db.close()

async def add_member(username):
    '''
    Add member to DB if not exists
    :param username: TG Username
    :return:
    '''
    db.connect()
    username = username.replace('@', '')
    logging.info(f"Adding member {username} to DB")
    usr, created = ChatUser.get_or_create(
        username=username,
    )
    if not created:
        logging.info(f"User {usr.userid} already exists")
    usr.save()
    db.close()

async def finduser(username: str):
    '''
    Find user by username
    :param username: TG username
    :return: "Name Surname" if found, None otherwise
    '''
    db.connect()
    usr = ChatUser.get_or_none(ChatUser.username == username)
    db.close()
    if usr is None or usr.first_name is None:
        return None
    return f"{usr.first_name} {usr.last_name}"

async def create_etude(author, name, members):
    '''
    Create new Etude in DB
    :param author: Telegram Id of authore
    :param name: Name of etude
    :param members: List of Telegram nicknames of members
    :return:
    '''
    db.connect()
    user_records = []
    for member in members:
        member = member.replace("@","")
        record, created = ChatUser.get_or_create(
            username=member,
        )
        if created:
            logging.info(f"Created new user {member} without conversation")
            record.save()
        user_records.append(record)
    author_record = ChatUser.get_or_none(ChatUser.tg_id == author)
    etude_record = Etude.create(name=name, createdBy=author_record.userid)
    etude_record.save()
    for record in user_records:
        membership = Memberships.create(user=record.userid, etude=etude_record.etudeid)
        membership.save()
    db.close()

async def get_etudes(tgid):
    '''
    Returns list of Etudes models
    :param tgid: Telegram ID
    :return: Etudes list
    '''
    db.connect()
    userid = ChatUser.get_or_none(ChatUser.tg_id == tgid)
    if userid is None:
        return None
    query = Etude.select().where(Etude.createdBy == userid)
    etudes = list(query)
    db.close()
    return etudes

async def get_members(etudeid):
    '''
    Return list of Users who are members of Etude
    :param etudeid: Etude id
    :return: list of Users
    '''
    db.connect()
    memberships = Memberships.select().where(Memberships.etude == etudeid)
    members = []
    for membership in list(memberships):
        members.append(ChatUser.get_or_none(ChatUser.userid == membership.user))
    db.close()
    logging.info(f"Found {memberships}")
    return list(members)