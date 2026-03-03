import copy
import requests
import json

from lib import shared

def get_display_name(username):
    response = parse_api_response(values["urls"]["BASE_URL"]+'xrpc/app.bsky.actor.getProfile?actor='+username)
    return response["displayName"]

def save_pfp(username):
    response = parse_api_response(values["urls"]["BASE_URL"]+'xrpc/app.bsky.actor.getProfile?actor='+username)
    open(shared.get_user_pfp_path(database, username), 'wb').write(requests.get(response["avatar"]).content)

def get_friends(username, source):
    match source:
        case "following":
            api_endpoint = "getFollows"
            api_value = "follows"
        case "followers":
            api_endpoint = "getFollowers"
            api_value = "followers"
    response = parse_api_response(values["urls"]["BASE_URL"]+'xrpc/app.bsky.graph.'+api_endpoint+'?actor='+username)

    friends = copy.deepcopy(shared.users_db_structure)
    friends["users"] = {username: {source: []}}
    for friend in response[api_value]:
        friend_username = friend["handle"]
        try:
            friend_display_name = friend["displayName"]
        except:
            friend_display_name = friend_username

        friends["users"][username][source] += [friend_username]
        if friend_display_name != "":
            friends["display_names"][friend_username] = friend_display_name

        if args_save_pfp and "avatar" in friend:
            open(shared.get_user_pfp_path(database, friend_username), 'wb').write(requests.get(friend["avatar"]).content)
    return friends

def parse_api_response(url):
    return json.loads(requests.get(url).text)
