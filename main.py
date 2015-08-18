import os
from flask import Flask, render_template, request
from settings import instgram_access_token
from api import InstagramAPI
import pandas as pd
from sklearn.externals import joblib

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            if request.form['message'] == '':
                message = "Please input your Instagram User name in the box"
                return render_template('index.html', title="Your gender?", method=request.method, message=message)
            else:
                message = "Your Instagram data"
                insta = InstagramAPI(access_token=instgram_access_token)
                user_name = request.form['message']
                user_id = insta.user_id(user_name=user_name)
                profile_image = insta.profile_image(user_id)
                user = {'user_name': user_name, 'user_id': user_id, 'image': profile_image}
                user_summary = insta.user_info(user=user)
                test = {'nail': 0, 'hair': 0, 'person': 0, 'sport': 0, 'food': 0, 'night': 0, 'coffee': 0,
                        'wedding': 0, 'cake': 0, 'beer': 0, 'dog': 0, 'animal': 0, 'tree': 0, 'blossom': 0,
                        'cat': 0, 'flower': 0, 'sky': 0, 'nature': 0, 'cherry': 0, "user_name": "test", "user_id": "test"}
                X = pd.DataFrame([user_summary, test]).fillna(0)
                X['animal'] = X['animal']+X['dog']+X['cat']
                X['cosme'] = X['hair']+X['nail']
                X['nature'] = X['nature']+X['sky']+X['flower']+X['tree']+X['blossom']+X['cherry']
                X = X[X['user_name'] == user_name]
                X = X[['person', 'sport', 'food', 'night', 'coffee', 'wedding', 'cake', 'beer', 'animal', 'nature', 'cosme']]
                user_vec = X.values.tolist()[0]

                model_path = os.path.join(os.path.dirname(__file__), "clf/clf.pkl")
                clf = joblib.load(model_path)
                result = clf.predict(user_vec)

                return render_template('index.html', title="Your gender?", method=request.method, userinfo=user_summary, result=result, message=message)
        else:
            return render_template('index.html', title="Your gender?", method=request.method)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host='0.0.0.0')

