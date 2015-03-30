from alchemyapi.alchemyapi import AlchemyAPI
import requests
import requests_cache
import pandas as pd

# API呼び出しの結果をsqliteにキャッシュする
requests_cache.install_cache('cache_instagram', allowable_methods=('GET', 'POST'))

URL_ROOT = "https://api.instagram.com/v1/"


class InstagramAPI():
    def __init__(self, access_token):
        self.access_token = access_token

    def user_recent_media(self, user_id):
        url = URL_ROOT + "users/{0}/media/recent/?access_token={1}".format(user_id, self.access_token)
        r = requests.get(url)
        return r.json()

    def user_id(self, user_name):
        url = URL_ROOT + "users/search?q={0}&access_token={1}".format(user_name, self.access_token)

        r = requests.get(url)
        result = r.json()
        user_id = None
        for i in range(len(result["data"])):
            if user_name == result["data"][i]["username"]:
                user_id = result["data"][i]["id"]
                break

        return user_id

    def media_list(self, user_id):

        response_json = {"data": []}
        if user_id is not None:
            response_json = self.user_recent_media(user_id=user_id)

        rows = len(response_json["data"])
        entries = []
        for i in range(rows):
            small_dict = {}
            small_dict["date"]=response_json['data'][i]['created_time']  # 投稿日時
            cap = response_json['data'][i]['caption']
            if cap is not None:
                small_dict["caption"] = response_json['data'][i]['caption']['text']  # キャプション
            else:
                small_dict["caption"] = "No_caption"
            small_dict["url"] = response_json['data'][i]['images']['standard_resolution']['url']  # 画像URL
            entries.append(small_dict)
        return entries

    def follows_list(self, user_id):
        url = URL_ROOT + "users/{0}/follows?access_token={1}".format(user_id, self.access_token)
        r = requests.get(url)
        result = r.json()
        user_list = result["data"]
        following_users = [{"user_name": user["username"], "user_id": user["id"]} for user in user_list]

        return following_users

    def user_info(self, user):
        entries = self.media_list(user["user_id"])
        [entry.update({'tag_list': Alchemy.tag_list(image_url=entry['url'])}) for entry in entries]
        tags = [entry['tag_list'] for entry in entries]
        df = pd.DataFrame(tags).fillna(0)
        user_summery = df.sum()
        user_summery = user_summery.to_dict()
        user.update(user_summery)

        return user


class Alchemy():

    @staticmethod
    def tag_list(image_url):
        alchemyapi = AlchemyAPI()
        alchemy_json = alchemyapi.imageTagging("url", image_url)

        try:
            image_keywords = alchemy_json["imageKeywords"]

        except KeyError:
            return None

        else:
            result_list = {image_keyword["text"]: float(image_keyword["score"]) for image_keyword in image_keywords}
            return result_list
