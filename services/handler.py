import json

from lib import shared

AVAILABLE_SERVICES = ['facebook', 'instagram', 'bluesky', 'mastodon', 'tiktok']
AVAILABLE_SOURCES = ['all', 'following', 'followers', 'friends']

def set_service(service, mode=None):
    global service_values
    service_values = json.load(open(f"services/{service}/values.json", "r", encoding="utf-8"))
    if mode == "scan":
        global service_driver
        match service:
            case 'facebook':
                import services.facebook.driver
                service_driver = services.facebook.driver
            case 'instagram':
                import services.instagram.driver
                service_driver = services.instagram.driver
            case 'bluesky':
                import services.bluesky.driver
                service_driver = services.bluesky.driver
            case 'mastodon':
                import services.mastodon.driver
                service_driver = services.mastodon.driver
            case 'tiktok':
                import services.tiktok.driver
                service_driver = services.tiktok.driver
        service_driver.values = service_values
        try:
            service_driver.calibrated_driver_values = json.load(open(f"{shared.user_data_folder}/calibrated_driver_values.json", "r", encoding="utf-8"))[service]
        except:
            pass
    return service_values

def get_display_name(user):
    return service_driver.get_display_name(user)

def save_pfp(user):
    service_driver.save_pfp(user)

def get_friends(user, source):
    if source == "all":
        result = {}
        for available_source in service_values["available_sources"]:
            result = shared.deep_update(result, service_driver.get_friends(user, available_source))
        return result
    else:
        if source in service_values["available_sources"]:
            return service_driver.get_friends(user, source)
        else:
            raise ValueError("This service does not support the selected source.")
