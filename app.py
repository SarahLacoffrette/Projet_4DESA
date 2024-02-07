import os
from flask import Flask, render_template
from Database.connectDB import DB
from Routes.user import user_app
from Routes.media import media_app
from Routes.comment import comment_app


IMAGE= os.path.join('static', 'image')
app = Flask(__name__, template_folder='templates')
app.secret_key = '0b3e8ea349b521d7e5212c0ab24485fc'

app.register_blueprint(user_app)
app.register_blueprint(media_app)
app.register_blueprint(comment_app)

if DB:
    print("Connection successful")
else:
    print("Connection unsuccessful")


@app.route('/')
def get_home():
    return render_template('home.html')


app.run(host='0.0.0.0', port=7000, debug=True)