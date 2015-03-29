import sys
from settings import instgram_access_token
from api import InstagramAPI, Alchemy
import pandas as pd
import csv

def following_users(api, user_name):

    instgram_user_id = api.user_id(user_name=user_name)
    following_users = api.follows_list(user_id=instgram_user_id)

    return following_users


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if len(argvs) != 2:
        print('Usage: # python %s INSTAGRAM_USER_NAME' % argvs[0])
        quit()

    instgram_user_name = argvs[1]
    api = InstagramAPI(access_token=instgram_access_token)

    # 取得済みのユーザ情報をCSVからロード
    f = open('user_tags.csv', 'r')
    reader = csv.DictReader(f)
    gotten_users = []
    for user in reader:
        gotten_users.append(user)

    following_users = following_users(api, instgram_user_name)

    # フォロー中のユーザと取得済みユーザの差分辞書の作成
    userid_list = []
    get_users = []
    for g_user in gotten_users:
        userid_list.append(g_user["user_id"])

    for f_user in following_users:
        if f_user["user_id"] in set(userid_list):
            get_users.append(f_user)

    get_users = get_users[0:40]
    # following_users = following_users[0:40]

    userinfo_list = []
    # for user in following_users:
    for user in get_users:
        entries = api.media_list(user["user_id"])
        [entry.update({'tag_list': Alchemy.tag_list(image_url=entry['url'])}) for entry in entries]
        tags = [entry['tag_list'] for entry in entries]
        df = pd.DataFrame(tags).fillna(0)
        user_summery = df.sum()
        user_summery = user_summery.to_dict()
        user.update(user_summery)
        userinfo_list.append(user)
    users_df = pd.DataFrame(userinfo_list)
    users_df.to_csv("user_tags.csv")
    # for following_user in following_users:
    #     # entries = api.media_list(user_name=following_user)
    #     # for entry in entries:
    #     #     image_url = entry["url"]
    #     #     tag_list = Alchemy.tag_list(image_url=image_url)
    #     #     entry.update({"tag_list": tag_list})
    #     #     print(entry)
    #     # print(entries)
    print(userinfo_list)

