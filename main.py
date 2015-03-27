from flask import Flask, render_template, request
from settings import instgram_access_token
from instagram_collector import InstagramAPI, Alchemy
from alchemyapi.alchemyapi import AlchemyAPI

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        insta = InstagramAPI(access_token=instgram_access_token)
        media_list = insta.media_list(user_name=request.form['message'])
        for entry in medlia_list:
            image_url = entry["url"]
            tag_list = Alchemy.tag_list(image_url=image_url)
            entry.update({"tag_list": tag_list})
            # for i in range(len(media_list)):
            #    url = media_list[i][2]
        return render_template('index.html',title="Flask test", method=request.method, body="Your INSTAGRAM data" , entries=media_list)
    else:
        return render_template('index.html',title="Flask test", method=request.method,body="Input Your INSTAGRAM User name" ,entries="[{}]")


if __name__ == "__main__":
    app.run(debug=True)

