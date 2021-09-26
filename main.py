import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string
from datetime import datetime, timedelta


doc_name = '9vyXAKdNyxmG1eu5xhmL'


def random_name(N=20):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + "_", k=N))


def match_breaks(slots, priorities):
    
    all_values = [0]
    for priority in priorities.values():
        for val in priority.values():
            all_values.append(val)
    max_priority = max(all_values)

    breaks = []

    ids = set(slot["id"] for slot in slots)
    while not len(ids)==0:
        current_id = ids.pop()
        current_slots = [slot for slot in slots if slot["id"]==current_id]
        # check that I have slots
        assert not len(current_slots)==0
        current_priorities = priorities[current_id]
        other_ids = sorted(list(ids), key=lambda x: (current_priorities[x] if x in current_priorities else max_priority))
        found = False
        for other_id in other_ids:
            if found:
                break
            other_slots = [slot for slot in slots if slot["id"]==other_id]
            for current_slot in current_slots:
                if found:
                    break
                for other_slot in other_slots:
                    if found:
                        break
                    # check if match
                    if not (current_slot["end"]<=other_slot["start"] and current_slot["start"]>=other_slot["end"]):
                        new_meeting = {}
                        new_meeting["participants"] = [current_id, other_id]
                        new_meeting["start"] = max(current_slot["start"], other_slot["start"])
                        new_meeting["end"] = new_meeting["start"]+timedelta(minutes=30)
                        breaks.append(new_meeting)
                        # set new priorities
                        max_priority += 1
                        priorities[current_id][other_id] = max_priority
                        priorities[other_id][current_id] = max_priority
                        ids.discard(other_id)
                        
                        found = True
        # TODO if not found, match threesome
    return breaks, priorities


def daily_breaks():

    # Use a service account
    cred = credentials.Certificate('coffie-break-firebase-adminsdk-e37jb-daeee1fcee.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection('teams').document(doc_name).collection('users')

    users = users_ref.stream()
    user_ids = [user.id for user in users]

    all_slots = []
    all_priorities = {}
    for user_id in user_ids:
        user_slots = users_ref.document(user_id).collection('slots').stream()
        for slot in user_slots:
            slot_data = slot._data
            slot_data["id"] = user_id
            all_slots.append(slot_data)
        
        all_priorities[user_id] = {}
        if len(users_ref.document(user_id).collection('priorities').get())>0:
            user_priorities = users_ref.document(user_id).collection('priorities').stream()
            for priority in user_priorities:
                priority_data = priority._data
                all_priorities[user_id][priority.id] = priority_data['val']

    breaks, priorities = match_breaks(all_slots, all_priorities)

    breaks_ref = db.collection('teams').document(doc_name).collection('breaks')
    for i, _break in enumerate(breaks):
        new_break = _break.copy()
        new_break['participants'] = [f'/teams/{doc_name}/users/{participant}' for participant in new_break['participants']]
        new_break['link'] = f'http://teams.microsoft.com/break{i}link'
        breaks_ref.document(random_name()).set(new_break)

    for id1, priority in priorities.items():
        for id2, val in priority.items():
            users_ref.document(id1).collection('priorities').document(id2).set({"val":val})


def happy_hour():

    # Use a service account
    cred = credentials.Certificate('coffie-break-firebase-adminsdk-e37jb-daeee1fcee.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    users_ref = db.collection('teams').document(doc_name).collection('users')

    users = users_ref.stream()

    boss = None
    user_ids = []
    for user in users:
        if 'boss' in list(user.to_dict().keys()):
            boss = user.id
        else:
            user_ids.append(user.id)
    # boss has to be
    assert boss is not None
    # boss has to apply for weekly meeting
    assert len(users_ref.document(boss).collection('weekly_slot').get())>0
    boss_slots = []
    for slot in users_ref.document(boss).collection('weekly_slot').stream():
        boss_slots.append(slot._data)
    boss_slots = sorted(boss_slots, key=lambda x: x['start'])

    all_slots = []
    for user_id in user_ids:
        user_slots = users_ref.document(user_id).collection('weekly_slot').stream()
        for slot in user_slots:
            slot_data = slot._data
            slot_data["id"] = user_id
            all_slots.append(slot_data)
    
    max_counter = 0
    weekly_meeting = {}
    for boss_slot in boss_slots:
        start = boss_slot['start']
        end = start+timedelta(minutes=30)
        while end<=boss_slot['end']:
            fit_ids = [user_slot['id'] for user_slot in all_slots if start>=user_slot['start'] and end<=user_slot['end']]
            counter = len(fit_ids)
            if counter>max_counter:
                max_counter = counter
                weekly_meeting['start'] = start
                weekly_meeting['end'] = end
                weekly_meeting['participants'] = fit_ids + [boss]
                # fe09f0b2-7b0d-42e2-b08a-95e9ce469dd5
            start+=timedelta(minutes=30)
            end+=timedelta(minutes=30)
    
    weekly_ref = db.collection('teams').document(doc_name).collection('weekly_meeting')
    weekly_meeting['participants'] = [f'/teams/{doc_name}/users/{participant}' for participant in weekly_meeting['participants']]
    weekly_meeting['link'] = f'http://teams.microsoft.com/weeklylink'
    weekly_ref.document(random_name()).set(weekly_meeting)

#happy_hour()
daily_breaks()

exit()

from O365 import Account
from datetime import datetime

import requests
import json

# Get a token
url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': 'eb62ed45-8f09-4897-aa82-2ff374c46673',
    'scope': 'https://graph.microsoft.com/.default',
    'client_secret': 'fe09f0b2-7b0d-42e2-b08a-95e9ce469dd5',
}
r = requests.post(url, data=data)
token = r.json()
with open("token.json", "w") as outfile:
    json.dump(token, outfile)

credentials = ('eb62ed45-8f09-4897-aa82-2ff374c46673', 'fe09f0b2-7b0d-42e2-b08a-95e9ce469dd5')

scopes = ['https://outlook.office365.com/Calendars.Read']

from O365.utils.token import FileSystemTokenBackend
tk = FileSystemTokenBackend(token_path="/home/vasily/coffee_break/token.json", token_filename="token")
account = Account(credentials, token_backend=tk)

#account = Account(credentials, auth_flow_type = 'public',token_path="/home/vasily/coffee_break/token.json", token_filename="token.json")
#account = Account(credentials)

schedule = account.schedule()
calendar = schedule.get_default_calendar()

'''import requests

# Get a token
url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': 'eb62ed45-8f09-4897-aa82-2ff374c46673',
    'scope': 'https://graph.microsoft.com/.default',
    'client_secret': 'fe09f0b2-7b0d-42e2-b08a-95e9ce469dd5',
}
r = requests.post(url, data=data)
token = r.json().get('access_token')

# ...

# Use the token using microsoft graph endpoints
url = 'https://graph.microsoft.com/v1.0/users/{}/events'.format('user_email') # can also use the user_id (e.g. 12345-abcde-...)
headers = {
    'Authorization': 'Bearer {}'.format(token)
}
r = requests.get(url, headers=headers)'''


#happy_hour()
#daily_breaks()