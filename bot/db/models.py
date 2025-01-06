from datetime import datetime

from peewee import *

db = SqliteDatabase('database.db')

class ChatUser(Model):
    userid = AutoField(unique=True)
    tg_id = BigIntegerField(null=True)
    username = TextField(unique=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)

    class Meta:
        database = db

class Etude(Model):
    etudeid = AutoField(unique=True)
    name = TextField(unique=True)
    createdAt = DateTimeField(default=datetime.now)
    createdBy = ForeignKeyField(ChatUser)

    class Meta:
        database = db

class Memberships(Model):
    membership_id = AutoField(unique=True)
    user = ForeignKeyField(ChatUser)
    etude = ForeignKeyField(Etude)

    class Meta:
        database = db