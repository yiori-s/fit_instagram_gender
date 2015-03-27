from flask import Flask, render_template, request
from settings import instgram_access_token
from instagram_collector import InstagramAPI, Alchemy
from alchemyapi.alchemyapi import AlchemyAPI

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        insta = InstagramAPI(access_token=instgram_access_token)
        user_name = request.form['message']
        user_id = insta.user_id(user_name=user_name)
        user = {'user_name':user_name, 'user_is':user_id}
        user = insta.user_info(user=user)

        return render_template('index.html', title="Your gender?", method=request.method, body="Your Instagram data", userinfo=user)
    else:
        return render_template('index.html', title="Your gender?", method=request.method, body="Input Your Instagram User name", userinfo="[{}]")


if __name__ == "__main__":
    app.run(debug=True)

