import datetime

from common import coroutine, print_exception
#
# "16_18695_9296_0_8_100": {
#                 "gameEntities": [
#                     ["9f5e96c358774c3bb5b05fe11090cd0b.9",
#                         1475587033959,
#                         ["e", "E", "7f5577ff694642f98e531dd9223d8cfc.16",
#                             59988467, 30331012,
#                             "6a923beb210a434bbd79aadc9c96daa9.16",
#                             59985967, 30322072]],
from models import TEAMS, team_short, Portal, Tile, PortalToTile


@coroutine
def proceed_entity(target):
    while True:
        result = (yield)["result"]["map"]
        for tile_number, tile in result.iteritems():
            if "gameEntities" in tile:
                for entity in tile["gameEntities"]:
                    if entity[2][0] == 'p':
                        portal = {'uid': entity[0],
                            'team': TEAMS.index(team_short[entity[2][1]]),
                            'lat': entity[2][2],
                            'lng': entity[2][3],
                            'lvl': entity[2][4],
                            'live': entity[2][5],
                            'resonators': entity[2][6],
                            'name': entity[2][8],
                            'image': entity[2][7],
                            'time': datetime.datetime.fromtimestamp(entity[1]/1000),
                            'tile': tile_number
                        }
                        target.send((portal, tile_number))

@coroutine
def portal_to_db():
    while True:
        res, tile_number = (yield)
        try:
            tile, tile_created = Tile.get_or_create(number = res['tile'])
            tile.save()

            portal, portal_created = Portal.get_or_create(
                e6lat = res['lat'], e6lng = res['lng'])
            portal.team = res['team']
            portal.level = res['lvl']
            portal.live = res['live']
            portal.resonators = res['resonators']
            portal.name = res['name']
            portal.image = res['image']
            portal.time = res['time']
            portal.uid = res['uid']
            portal.save()

            portal_to_tile, tile_created = PortalToTile.get_or_create(
                tile = tile, portal = portal)
            portal_to_tile.save()

        except KeyError as key:
            print_exception('KEY!!!! ', key)
            continue
        except Exception as e:
            print_exception('FUCCCCCCK!!!! ', e)
            continue
