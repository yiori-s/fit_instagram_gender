from flask import Flask, render_template, request
from settings import instgram_access_token
from api import InstagramAPI, Alchemy
import pandas as pd
from sklearn import datasets
from sklearn.externals import joblib

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        insta = InstagramAPI(access_token=instgram_access_token)
        user_name = request.form['message']
        user_id = insta.user_id(user_name=user_name)
        profile_image = insta.profile_image(user_id)
        user = {'user_name': user_name, 'user_id': user_id, 'image': profile_image}
        user_summery = insta.user_info(user=user)
        test = {'nail': 0, 'hair': 0, 'person': 0, 'sport': 0, 'food': 0, 'night': 0, 'coffee': 0,
                'wedding': 0, 'cake': 0, 'beer': 0, 'dog': 0, 'animal': 0, 'tree': 0, 'blossom': 0,
                'cat': 0, 'flower': 0, 'sky': 0, 'nature': 0, 'cherry': 0, "user_name": "test", "user_id": "test"}
        X = pd.DataFrame([user_summery, test]).fillna(0)
        X['animal'] = X['animal']+X['dog']+X['cat']
        X['cosme'] = X['hair']+X['nail']
        X['nature'] = X['nature']+X['sky']+X['flower']+X['tree']+X['blossom']+X['cherry']
        X = X[X['user_name'] == user_name]
        X = X[['person', 'sport', 'food', 'night', 'coffee', 'wedding', 'cake', 'beer', 'animal', 'nature', 'cosme']]
        user_vec = X.values.tolist()[0]
        clf = joblib.load('clf/clf.pkl')
        result = clf.predict(user_vec)

        return render_template('index.html', title="Your gender?", method=request.method, userinfo=user_summery, result=result)
    else:
        return render_template('index.html', title="Your gender?", method=request.method)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

