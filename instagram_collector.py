import sys
from settings import instgram_access_token
from api import InstagramAPI, Alchemy
import pandas as pd

def following_users(api, user_name):

    instgram_user_id = api.user_id(user_name=user_name)
    following_users = api.follows_list(user_id=instgram_user_id)

    return following_users


def userinfo_list(api, following_users):

    userinfo_list = []
    for user in following_users:
        entries = api.media_list(user["user_id"])

        for entry in entries:
            tag_list = Alchemy.tag_list(image_url=entry['url'])

            if tag_list is None:
                return userinfo_list

            entry.update({'tag_list': tag_list})

        tags = [entry['tag_list'] for entry in entries]
        df = pd.DataFrame(tags).fillna(0)
        user_summery = df.sum()
        user_summery = user_summery.to_dict()
        user.update(user_summery)
        userinfo_list.append(user)

    return userinfo_list


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if len(argvs) != 2:
        print('Usage: # python %s INSTAGRAM_USER_NAME' % argvs[0])
        quit()

    instgram_user_name = argvs[1]
    api = InstagramAPI(access_token=instgram_access_token)

    following_users = following_users(api, instgram_user_name)
    following_users = following_users[0:40]

    userinfo_list = userinfo_list(api, following_users)
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

