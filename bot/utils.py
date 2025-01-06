import logging
from db import calls


async def search_user(nickname):
    '''
    Get user's name and surname if exists, otherwise return nickname
    :param bot - Bot instance
    :param nickname - nickname to search
    :return User's name or nickname
    '''
    logging.info(f"Trying to get user's name by nickname {nickname}")
    fullname = await calls.finduser(nickname.replace("@",""))
    if fullname:
        return fullname
    return nickname
