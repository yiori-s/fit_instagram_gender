import sys
from settings import instgram_access_token
from alchemyapi.alchemyapi import AlchemyAPI
import requests
import requests_cache
import json

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

	def userid(self, user_name):
		url = URL_ROOT + "users/search?q={0}&access_token={1}".format(instgram_user_name, self.access_token)

		r = requests.get(url)
		result = r.json()
		user_id = None	
		for i in range(len(result["data"])):
			if user_name == result["data"][i]["username"]:
				user_id = result["data"][i]["id"]
				break

		return user_id

	def media_list(self, user_name):
		# user_name = 'yiori_s'
		url = URL_ROOT + "users/search?q={0}&access_token={1}".format(user_name, self.access_token)
		r = requests.get(url)
		result = r.json()	
		user_id = None
		for i in range(len(result["data"])):
			if user_name == result["data"][i]["username"]:
				user_id = result["data"][i]["id"]
				break
		#user_id = str(37880905)

		instgram_user_id = user_id
		if instgram_user_id is not None:
			url = URL_ROOT + "users/{0}/media/recent/?access_token={1}".format(instgram_user_id, self.access_token)
			r = requests.get(url)
			response_json = r.json()
		
		rows = len(response_json["data"])
		data = []
		for i in range(rows):
			small_data = []
			small_data.append(response_json['data'][i]['created_time']) #投稿日時
			cap = response_json['data'][i]['caption']
			if cap is not None:
				small_data.append(response_json['data'][i]['caption']['text']) #キャプション
			else:
				small_data.append("No_caption")
			small_data.append(response_json['data'][i]['images']['standard_resolution']['url']) #画像URL
			data.append(small_data)
		return data

	def media_list_dict(self, user_name):
		url = URL_ROOT + "users/search?q={0}&access_token={1}".format(user_name, self.access_token)
		r = requests.get(url)
		result = r.json()
		user_id = None	
		for i in range(len(result["data"])):
			if user_name == result["data"][i]["username"]:
				user_id = result["data"][i]["id"]
				break
		instgram_user_id = user_id
		if instgram_user_id is not None:
			url = URL_ROOT + "users/{0}/media/recent/?access_token={1}".format(instgram_user_id, self.access_token)
			r = requests.get(url)
			response_json = r.json()
		
		rows = len(response_json["data"])
		data = []
		for i in range(rows):
			small_dict = {}
			small_dict["date"]=response_json['data'][i]['created_time'] #投稿日時
			cap = response_json['data'][i]['caption']
			if cap is not None:
				small_dict["caption"]=response_json['data'][i]['caption']['text'] #キャプション
			else:
				small_dict["caption"]="No_caption"
			small_dict["url"]=response_json['data'][i]['images']['standard_resolution']['url'] #画像URL
			data.append(small_dict)			
		return data

class Alchemy():
	def tag_list(image_url):
		alchemyapi = AlchemyAPI()
		alchemy_json=alchemyapi.imageTagging("url", image_url)
		tag = alchemy_json["imageKeywords"][0]["text"]
		score = alchemy_json["imageKeywords"][0]["score"]
		return tag, score

if __name__ == '__main__':
	argvs = sys.argv
	argc = len(argvs)
	if len(argvs) != 2:
		print('Usage: # python %s INSTAGRAM_USER_NAME' % argvs[0])
		quit()

	instgram_user_name = argvs[1]
	api = InstagramAPI(access_token=instgram_access_token)
	data = api.media_list(user_name=instgram_user_name)
	for entry in data:
		image_url = entry[2]
		alchemyapi = AlchemyAPI()
		alchemy_json=alchemyapi.imageTagging("url", image_url)
		if len(alchemy_json["imageKeywords"]) > 0:
			tag = alchemy_json["imageKeywords"][0]["text"]
			score = alchemy_json["imageKeywords"][0]["score"]
		#tag, score= Alchemy().tag_list(image_url=url)
		entry.append(tag)
		entry.append(score)
	
	print(data)

