from flask import Flask, render_template, json, g, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.httpauth import HTTPBasicAuth
from database import db_session
from models import *

app = Flask(__name__)
app.config['SECRET_KAY'] = 'test'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
auth = HTTPBasicAuth()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def hello_world():
    return 'Index Page'


@app.route('/scan/<user_id>', methods=['GET'])
@auth.login_required
def scan(user_id):
    result = db_session.query(User).filter(User.user_id == user_id).first()
    if result is None:
        json_result = {'user_id': None}
        return json.dumps(json_result, ensure_ascii=False)
    else:
        json_result = {'user_id': result.user_id, 'user_email': result.user_email, 'user_pass': result.user_pass,
                       'user_nic': result.user_nic, 'user_phone': result.user_phone, 'user_name': result.user_name}
        return json.dumps(json_result, ensure_ascii=False)


@app.route('/hello/<username>/<int:user_id>')
def hello_page(username, user_id):
    print(username, user_id)
    return 'Hello Page' + username + str(user_id)


@app.route('/templa')
def try_template():
    return render_template('template1.html')


@auth.verify_password
def verify_password(username_or_token, user_pass):
    print(username_or_token)
    user = User.verify_auth_token(username_or_token, app.config['SECRET_KAY'])
    if not user:
        print('Not token')
        user = db_session.query(User).filter(User.user_name == username_or_token).first()
        if user is None:
            print('User name is not right')
            return False
        else:
            if user.user_pass != user_pass:
                print('password is not right')
                return False
    g.user = user
    print("success")
    return True


@app.route('/api/token')
@auth.login_required
def get_token():
    token = g.user.generate_auth_token(app.config['SECRET_KAY'])
    print(token)
    return jsonify({'token': token.decode('utf8'), 'duration': 600})


@app.route('/templa2')
@auth.login_required
def try_template2():
    return render_template('template2.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
