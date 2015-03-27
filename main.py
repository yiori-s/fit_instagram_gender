#coding:utf-8

from flask import Flask, render_template, request
import sys
from settings import instgram_access_token
import requests, requests_cache
import json
from instagram_collector import InstagramAPI
import jinja2
from alchemyapi.alchemyapi import AlchemyAPI

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        insta = InstagramAPI(access_token=instgram_access_token)
        media_list = insta.media_list_dict(user_name=request.form['message'])
        for entry in medlia_list:
            image_url = entry["url"]
            alchemyapi = AlchemyAPI()
            alchemy_json=alchemyapi.imageTagging("url", image_url)
            if len(alchemy_json["imageKeywords"]) > 0:
                tag = alchemy_json["imageKeywords"][0]["text"]
                score = alchemy_json["imageKeywords"][0]["score"]
            entry["tag"] = tag
            entry["score"] = score
            #for i in range(len(media_list)):
            #    url = media_list[i][2]
        return render_template('index.html',title="Flask test", method=request.method, body="Your INSTAGRAM data" , entries=media_list)
    else:
        return render_template('index.html',title="Flask test", method=request.method,body="Input Your INSTAGRAM User name" ,entries="[{}]")


if __name__ == "__main__":
    app.run(debug=True)

