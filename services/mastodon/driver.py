import json
from lib import shared
import copy
import requests

from lib import shared

def get_display_name(username, tab = None):
    response = parse_api_response(values["urls"]["BASE_URL"] + f'accounts/lookup?acct={username}')
    return response["display_name"]

def get_id(username):
    response = parse_api_response(values["urls"]["BASE_URL"] + f'accounts/lookup?acct={username}')
    return response["id"]

def save_pfp(username, tab = None):
    response = parse_api_response(values["urls"]["BASE_URL"] + f'accounts/lookup?acct={username}')
    open(save_pfp_location + username+'.png', 'wb').write(requests.get(response["avatar"]).content)

def get_friends(username, source, tab = None):
    id = get_id(username)
    
    match source:
        case "following":
            api_endpoint = "following"
        case "followers":
            api_endpoint = "followers"
    response = parse_api_response(values["urls"]["BASE_URL"] + 'accounts/' + id + '/' + api_endpoint)

    friends = copy.deepcopy(shared.users_db_structure)
    friends["users"] = {username: {source: []}}
    for friend in response:
        friend_username = friend["acct"]
        friend_display_name = friend["display_name"]
        if not args_nopfp:
            open(save_pfp_location + friend_username + '.png', 'wb').write(requests.get(friend["avatar"]).content)

        if friend_username not in friends["users"][username][source]:
            friends["users"][username][source] += [friend_username]
            if friend_display_name != "":
                friends["display_names"][friend_username] = friend_display_name
    return friends

def parse_api_response(url):
    return json.loads(requests.get(url).text)
