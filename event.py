from common import coroutine, print_exception
from models import User, TEAMS


@coroutine
def proceed_event(target):
    while True:
        result = (yield)["result"]
        for event in result:
            id = event[0]
            time = event[1]
            plext = event[2]['plext']
            text = plext['text']
            markup = plext['markup']

            user = markup[0][1]
            target['user'].send(user)

@coroutine
def user_to_db():
    while True:
        res = (yield)
        try:
            # pl = {
            #     "plain": "werelobz",
            #     "team": "ENLIGHTENED"
            # }
            team_ = res['team']
            user, created = User.get_or_create(
                name = res['plain'])
            user.team = TEAMS.index(team_)

            if created:
                print(str(user.name) + ' saved!')
            else:
                print(str(user.name) + ' exist')

            user.save()
        except KeyError as key:
            print_exception('KEY!!!! ', key)
            continue
        except Exception as e:
            print_exception('FUCCCCCCK!!!! ', e)
            continue

