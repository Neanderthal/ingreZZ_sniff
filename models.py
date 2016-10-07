from peewee import *

class CardTypeEnum(object):
    """
    Декада
    """
    ENLIGHTENED = 0
    RESISTANCE = 1
    NEUTRAL = 2

    values = {
        ENLIGHTENED: u'ENLIGHTENED',
        RESISTANCE: u'RESISTANCE',
        NEUTRAL: u'NEUTRAL',
    }

    values = {
        ENLIGHTENED: u'ENLIGHTENED',
        RESISTANCE: u'RESISTANCE',
        NEUTRAL: u'NEUTRAL',
    }

class Teams(object):
    @staticmethod
    def ENLIGHTENED():
        return 0
    @staticmethod
    def RESISTANCE():
        return 1

    @staticmethod
    def NEUTRAL():
        return 2


TEAMS = ['ENLIGHTENED', 'RESISTANCE', 'NEUTRAL']
team_short = {'N':'NEUTRAL', 'E':'ENLIGHTENED', 'R':'RESISTANCE'}

db = PostgresqlDatabase(database='ingres', user='ingres', host='localhost', password ='ingres')

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(index=True, unique=True)
    team = IntegerField(null=True)
    level = IntegerField(null=True)

class Tile(BaseModel):
    number = CharField(index=True, unique=True)

class Portal(BaseModel):
    e6lat = IntegerField()
    e6lng = IntegerField()
    name = CharField(null=True)
    uid = CharField(null=True)
    image = CharField(null=True)
    team = IntegerField(null=True)
    level = IntegerField(null=True)
    live = IntegerField(null=True)
    resonators = IntegerField(null=True)
    time = DateTimeField(null=True)

    class Meta:
        indexes = (
            (('e6lat', 'e6lng'), True),)


class PortalToTile(BaseModel):
    tile = ForeignKeyField(Tile, related_name='relationships')
    portal = ForeignKeyField(Portal, related_name='related_to')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('tile', 'portal'), True),
        )