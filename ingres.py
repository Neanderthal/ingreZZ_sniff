from mitmproxy.models import decoded
from mitmproxy.script import concurrent

from common import response_filter, decode_json
from entities import proceed_entity, portal_to_db
from event import proceed_event, user_to_db
from models import User, db, PortalToTile, Tile, Portal

db.drop_tables([User, Portal, Tile, PortalToTile])

db.create_tables([User, Portal, Tile, PortalToTile])
log_filename = 'ingres_5'

plext_worker = response_filter('getPlexts', decode_json(proceed_event({
    'user':user_to_db(),})))

portal_worker = response_filter('getEntities', decode_json(proceed_entity(
    portal_to_db())))

@concurrent 
def response(context, flow):
    print('CALLLEED!!!!')
    with decoded(flow.response):
        plext_worker = response_filter('getPlexts', decode_json(proceed_event({
            'user':user_to_db(),})))

        portal_worker = response_filter('getEntities', decode_json(proceed_entity(
            portal_to_db())))

        plext_worker.send(flow)
        portal_worker.send(flow)
