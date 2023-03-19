from config import VK_TOKEN, API_VERSION


def vk_method(method, params):
    return f"https://api.vk.com/method/{method}?{params}&access_token={VK_TOKEN}&v={API_VERSION}"


def get_users_URL(id):
    return vk_method("users.get", f"user_ids={id}")


def get_friends_URL(id):
    return vk_method("friends.get", f"user_id={id}")
