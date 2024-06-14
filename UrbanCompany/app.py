# from flask import Flask, render_template, url_for, redirect, session, request
# from authlib.integrations.flask_client import OAuth
# import json

# app=Flask(__name__)
# app.secret_key='urbansecret75'

# oauth = OAuth(app)

# google = oauth.register(
#     name='google',
#     client_id='799806588646-i2aabtg032c8mbc15sm1f473740el71u.apps.googleusercontent.com',
#     client_secret='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',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/o/oauth2/v1/',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope':'openid profile email'},

# )



# @app.route("/")
# def index():
#     email= dict(session).get('email',None)
#     return f"Hello, {email}"

# @app.route('/login')
# def login():
#     google=oauth.create_client('google')
#     state = generate_state()
#     session['state'] = state
#     redirect_uri = url_for('authorize', _external=True)
#     response = google.authorize_redirect(redirect_uri, state=state)
#     return redirect(response.location)

# import secrets

# def generate_state():
#   return secrets.token_urlsafe(32)

# @app.route('/authorize')
# def authorize():
#     google=oauth.create_client('google')
#     print("one")
#     state = request.args.get('state')
#     stored_state = session.get('state')
#     if not state or not stored_state or state != stored_state:
#         return "Invalid state parameter!", 400
#     print("two")
#     token=google.authorize_access_token()
#     print("post token")
#     userinfo=token['userinfo']
#     print("three")
#     claims = google.parse_id_token(token, leeway=30)
#     print(claims.get('iss'))
#     user_info = claims.json()
#     session['email'] = user_info['email']
#     return redirect("/")

# @app.route("/logout")
# def logout():
#     for key in list(session.keys()):
#         session.pop(key)
#     return redirect("/")




from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('homepage.html',user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    print("user authorized")
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



import controller.user_controller as user_controller
from model.info_model import info_model

obj1=info_model()

@app.route("/salonandspa")
def salonandspa():
    return render_template("salonandspa.html")
@app.route("/spa")
def spa():
    return render_template("spa.html",data=obj1.info_getall_package())

@app.route("/salon")
def salon():
    return render_template("salon.html")
