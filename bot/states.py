from enum import Enum

class DialogState(Enum):
    INIT = 1
    PREPARE_RUNTIME = 2
    RUNTIME = 3
    LIST_ALL = 4
    CREATE_ETUDE = 5
    ADD_ROLES = 6
    MODIFY = 7
    REMOVE = 8
