from flask import Flask, render_template, url_for
from flask import request, redirect, jsonify, flash
from functools import update_wrapper
from flask import Blueprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Aimodels import Base, User, AiCustom, AiCatalog
from Aimodels import Ai, AiBook, AiNews, AiMatch

from flask import session as login_session
from flask import make_response, g
from functools import wraps

import random
import string
import httplib2
import json
import requests
import time

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from redis import Redis
redis = Redis()


app = Flask(__name__)


# Rate Limit


class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        p = redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)


def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)


def on_over_limit(limit):
    return (jsonify({'data': 'You hit the rate limit', 'error': '429'}), 429)


def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            rlimit = RateLimit(key, limit, per, send_x_headers)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator


@app.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response


# PostgreSQL
engine = create_engine('postgresql://catalog:ducky@localhost/ai')

# SQlite
# engine = create_engine('sqlite:///Ai.db')

# Database Setup
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# API #

# Blue print definition
api = Blueprint('api', __name__)


@api.route('/aicatalogs/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiCatalogJSON():
    aicatalogsall = session.query(AiCatalog).all()
    return jsonify(aicatalogs=[i.serialize for i in aicatalogsall])


@api.route('/aicatalogs/<int:aicatalog_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiCustomJSON(aicatalog_id):
    if aicatalog_id not in Important_catalog_id:
        aicustomall = session.query(AiCustom).filter_by(
            aicatalog_id=aicatalog_id)
        return jsonify(aicustom=[i.serialize for i in aicustomall])
    else:
        aicatalog = session.query(AiCatalog).filter_by(id=aicatalog_id).one()
        catalogname = aicatalog.name.lower()
        redirecturl = '/api/v1/aicatalogs/%s/JSON' % catalogname
        return redirect(redirecturl)


@api.route('/aicatalogs/<int:aicatalog_id>/list/<int:aicustom_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiCustomitemJSON(aicatalog_id, aicustom_id):
    if aicatalog_id not in Important_catalog_id:
        aicustom = session.query(AiCustom).filter_by(
            id=aicustom_id, aicatalog_id=aicatalog_id).one()
        return jsonify(aicustom=aicustom.serialize)
    else:
        aicatalog = session.query(AiCatalog).filter_by(id=aicatalog_id).one()
        catalogname = aicatalog.name.lower()
        redirecturl = '/api/v1/aicatalogs/%s/list/%s/JSON' % (catalogname,
                                                              aicustom_id)
        return redirect(redirecturl)


@api.route('/aicatalogs/ai/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiJSON():
    aiall = session.query(Ai).all()
    return jsonify(ai=[i.serialize for i in aiall])


@api.route('/aicatalogs/ai/list/<int:ai_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiitemJSON(ai_id):
    ai = session.query(Ai).filter_by(id=ai_id).one()
    return jsonify(ai=ai.serialize)


@api.route('/aicatalogs/aibook/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiBookJSON():
    aibookall = session.query(AiBook).all()
    return jsonify(aibook=[i.serialize for i in aibookall])


@api.route('/aicatalogs/aibook/list/<int:aibook_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiBookitemJSON(aibook_id):
    aibook = session.query(AiBook).filter_by(id=aibook_id).one()
    return jsonify(aibook=aibook.serialize)


@api.route('/aicatalogs/ainews/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiNewsJSON():
    ainewsall = session.query(AiNews).all()
    return jsonify(ainews=[i.serialize for i in ainewsall])


@api.route('/aicatalogs/ainews/list/<int:ainews_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiNewsitemJSON(ainews_id):
    ainews = session.query(AiNews).filter_by(id=ainews_id).one()
    return jsonify(ainews=ainews.serialize)


@api.route('/aicatalogs/aimatch/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiMatchJSON():
    aimatchall = session.query(AiMatch).all()
    return jsonify(aimatch=[i.serialize for i in aimatchall])


@api.route('/aicatalogs/aimatch/list/<int:aimatch_id>/JSON')
@ratelimit(limit=300, per=60 * 1)
def AiMatchitemJSON(aimatch_id):
    aimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()
    return jsonify(aimatch=aimatch.serialize)


# GOOGLE OAUTH #

CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']

# FACEBOOK OAUTH #

APP_ID = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']

APP_SECRET = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']


# decorator for login


def login_required(f):
    @wraps(f)
    def decorater(*args, **kwargs):
        if 'username' not in login_session:
            flash('login to use the function')
            return redirect(url_for('Login'))
        return f(*args, **kwargs)
    return decorater


# h define

h = httplib2.Http()

# Login

# Tell about this is logged by token or not
# 0(no) = not by token
# 1(yes) = logged by token
# This is used when logout
logged_by_token = 0

# Tell about the user comed right now or not
# 0(no) = was in the page
# 1(yes) = open the page right now
# Token login is only executed when the user came right now
# This is used when understanding user came right now or not

# ERROR!!!!
# This is not correct. This is just valid for the first user came to server.
# I need to find a way to determine the user just came to server!

came_right_now = 1


@app.route('/login')
@ratelimit(limit=300, per=60 * 1)
def Login():

    # Did user camed just now?
    global came_right_now

    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in range(32))
    login_session['state'] = state
    aicatalogs = session.query(AiCatalog).all()

    # If i make token verify i need to add here
    # Store the token to the cookie when login and check it here.
    # it will make login session and return to main home

    token = request.cookies.get('token')

    if token:
        print('Token: ' + token)
        user_id = User.verify_auth_token(request.cookies.get('token'))
        print(user_id)
        if user_id and came_right_now == 1:  # user just came right now

            print("Login - yes token")

            user = session.query(User).filter_by(id=user_id).one()

            login_session['username'] = user.username
            login_session['picture'] = user.picture
            login_session['email'] = user.email
            login_session['provider'] = user.provider

            global logged_by_token
            logged_by_token = 1
            came_right_now = 0  # now the user is just remaining at the site

            flash("you are now token logged in as %s"
                  % login_session['username'])

            # Give new token
            token = user.generate_auth_token(600)

            redirect_to_main = redirect(url_for('showAiCatalog'))
            response = make_response(redirect_to_main)
            response.set_cookie('token', value=token)
            return response

    print("Login - no token")
    came_right_now = 0  # now the user is just remaining at the site
    return render_template('login.html',
                           STATE=state, aicatalogs=aicatalogs,
                           CLIENT_ID=CLIENT_ID,
                           APP_ID=APP_ID)


# Logout

@app.route('/logout')
@login_required
@ratelimit(limit=300, per=60 * 1)
def Logout():

    global logged_by_token

    if 'provider' in login_session:
        if login_session['provider'] == 'google' and logged_by_token == 0:
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']

        if login_session['provider'] == 'facebook' and logged_by_token == 0:
            fdisconnect()
            del login_session['facebook_id']
            del login_session['access_token']

        if login_session['provider'] == 'aily':
            ailydisconnect()

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']

        logged_by_token = 0

        flash("Successfully Logout!")

        redirect_to_main = redirect(url_for('showAiCatalog'))
        response = make_response(redirect_to_main)
        # overlap token info at cookie and destroy it
        response.set_cookie('token', value='')
        return response


# Website User Function

@app.route('/users', methods=['POST'])
@ratelimit(limit=300, per=60 * 1)
def new_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if username == '' or password == '' or email == '':
        flash("missing arguments")
        return redirect(url_for('Login'))

    if session.query(User).filter_by(username=username).first() is not None:
        flash("existing user")
        return redirect(url_for('Login'))

    newuser = User(username=username,
                   email=email,
                   picture='',
                   provider='aily')
    newuser.hash_password(password)

    session.add(newuser)
    session.commit()

    flash("Account successfully created!")
    return redirect(url_for('Login'))


# Aily Login

@app.route('/ailyconnect', methods=['POST'])
@ratelimit(limit=300, per=60 * 1)
def ailyconnect():
    email = request.form['email']
    password = request.form['password']

    if email == '' or password == '':
        flash("missing arguments")
        return redirect(url_for('Login'))

    if session.query(User).filter_by(email=email).first() is None:
        flash("You have to make account before login")
        return redirect(url_for('Login'))

    user_id = getUserID(email)
    user = session.query(User).filter_by(id=user_id).first()
    if not user or not user.verify_password(password):
        flash("You entered wrong password")
        return redirect(url_for('Login'))

    token = user.generate_auth_token(600)

    login_session['provider'] = 'aily'
    login_session['username'] = user.username
    login_session['email'] = user.email
    login_session['user_id'] = user.id
    login_session['picture'] = user.picture

    if user.id == 1:
        flash("WELCOME DUCK! WE WAITED FOR YOU!")
    else:
        flash("Sucessfully Logged In!")

    redirect_to_main = redirect(url_for('showAiCatalog'))
    response = make_response(redirect_to_main)
    response.set_cookie('token', value=token)
    return response

# Aily Logout


@app.route('/ailydisconnect')
@login_required
@ratelimit(limit=300, per=60 * 1)
def ailydisconnect():
    return "you have been logged out"


# Google Login

@app.route('/gconnect', methods=['POST'])
@ratelimit(limit=300, per=60 * 1)
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
                json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)

    # Submit request, parse response - Python3 compatible
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
                json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
                json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    user = session.query(User).filter_by(id=user_id).first()
    token = user.generate_auth_token(600)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''
    " style = "width: 300px;
    height: 300px;
    border-radius:150px;
    -webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''

    flash("you are now logged in as %s" % login_session['username'])

    response = make_response(output)
    response.set_cookie('token', value=token)
    return response

# Google Logout


@app.route('/gdisconnect')
@login_required
@ratelimit(limit=300, per=60 * 1)
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
                json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Facebook Login

@app.route('/fbconnect', methods=['POST'])
@ratelimit(limit=300, per=60 * 1)
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print ("access token received %s" % access_token)

    url = ('https://graph.facebook.com/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (APP_ID, APP_SECRET, access_token)

    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # userinfo_url = "https://graph.facebook.com/v2.8/me"

    '''
        Due to the formatting for the result from the server
        token exchange we have to split the token first on commas
        and select the first index which gives us the key : value
        for the server access token then we split it on colons to
        pull out the actual token value and replace the remaining quotes with
        nothing so that it can be used directly in the graph api calls
    '''

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?access_token'
           '=%s&fields=name,id,email') % token
    result = h.request(url, 'GET')[1]

    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    url = ('https://graph.facebook.com/v2.8/me/picture'
           '?access_token=%s&redirect=0&height=200&width=200') % token

    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    user = session.query(User).filter_by(id=user_id).first()

    token = user.generate_auth_token(600)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''
    " style = "width: 300px;
    height: 300px;
    border-radius: 150px;
    -webkit-border-radius: 150px;
    -moz-border-radius: 150px;">
    '''

    flash("you are now logged in as %s" % login_session['username'])

    response = make_response(output)
    response.set_cookie('token', value=token)
    return response

# Facebook Login


@app.route('/fdisconnect')
@login_required
@ratelimit(limit=300, per=60 * 1)
def fdisconnect():
    facebook_id = login_session['facebook_id']

    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
            facebook_id, access_token)
    result = h.request(url, 'DELETE')[1]
    print(result)
    return "you have been logged out"

# User Helper Functions


def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   provider=login_session['provider'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Making the website CRUD

# Only the admin could modify this catalog

Important_catalog_id = [1, 2, 3, 4]

# Main page and Catalog CRUD

# Blue print definition for catalog
catalog = Blueprint('catalog', __name__)


@app.route('/')
@app.route('/aicatalogs')
@ratelimit(limit=300, per=60 * 1)
def showAiCatalog():

    # Did user camed just now?
    global came_right_now
    print("Did user just camed? " + str(came_right_now))

    # Check if the user has token
    token = request.cookies.get('token')

    if token:
        print('Token: ' + token)
        user_id = User.verify_auth_token(request.cookies.get('token'))
        print(user_id)

        if user_id and came_right_now == 1:  # user just came right now
            global logged_by_token

            user = session.query(User).filter_by(id=user_id).one()

            login_session['username'] = user.username
            login_session['picture'] = user.picture
            login_session['email'] = user.email
            login_session['provider'] = user.provider

            logged_by_token = 1
            came_right_now = 0  # now the user is just remaining at the site

            flash("you are now token logged in as %s"
                  % login_session['username'])

            # Give new token
            token = user.generate_auth_token(600)

            redirect_to_main = redirect(url_for('showAiCatalog'))
            response = make_response(redirect_to_main)
            response.set_cookie('token', value=token)
            return response

    else:
        print("showAiCatalog - No Token")

    came_right_now = 0  # now the user is just remaining at the site

    # just give the website page if no token
    if 'username' not in login_session:
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiCatalog_show_public.html',
                               aicatalogs=aicatalogs)
    else:
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiCatalog_show.html',
                               aicatalogs=aicatalogs)


@catalog.route('/new', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAiCatalog():
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newaicatalog = AiCatalog(name=request.form['name'],
                                 description=request.form['description'],
                                 picture=image,
                                 user_id=login_session['user_id'])
        session.add(newaicatalog)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAiCatalog'))
    else:
        # anti-forgery attack
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in range(32))
        login_session['state'] = state
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiCatalog_new.html',
                               aicatalogs=aicatalogs,
                               STATE=state)


@catalog.route('/<int:aicatalog_id>/edit', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAiCatalog(aicatalog_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()

        # check is the user the owner of this item?
        if aicatalog.user_id != login_session['user_id']:
            flash('You are not the owner of this catalog')
            return redirect(url_for('showAiCatalog'))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editaicatalog = session.query(AiCatalog).filter_by(
            id=aicatalog_id).one()

        editaicatalog.name = request.form['name']
        editaicatalog.description = request.form['description']
        editaicatalog.picture = image

        session.add(editaicatalog)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAiCatalog'))
    else:
        if aicatalog_id not in Important_catalog_id:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            if aicatalog.user_id != login_session['user_id']:
                flash('You are not the owner of this catalog')
                return redirect(url_for('showAiCatalog'))
            else:
                # anti-forgery attack
                state = ''.join(random.choice(string.ascii_uppercase +
                                              string.digits
                                              ) for x in range(32))
                login_session['state'] = state
                return render_template('AiCatalog_edit.html',
                                       aicatalog=aicatalog,
                                       aicatalogs=aicatalogs,
                                       STATE=state)
        else:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            return render_template('AiCatalog_edit_denial.html',
                                   aicatalog=aicatalog,
                                   aicatalogs=aicatalogs)


@catalog.route('/<int:aicatalog_id>/delete', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAiCatalog(aicatalog_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()

        # check is the user the owner of this item?
        if aicatalog.user_id != login_session['user_id']:
            flash('You are not the owner of this catalog')
            return redirect(url_for('showAiCatalog'))

        deleteaicatalog = session.query(AiCatalog).filter_by(
            id=aicatalog_id).one()

        session.delete(deleteaicatalog)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAiCatalog'))
    else:
        if aicatalog_id not in Important_catalog_id:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            if aicatalog.user_id != login_session['user_id']:
                flash('You are not the owner of this catalog')
                return redirect(url_for('showAiCatalog'))
            else:
                # anti-forgery attack
                state = ''.join(random.choice(string.ascii_uppercase +
                                              string.digits
                                              ) for x in range(32))
                login_session['state'] = state
                return render_template('AiCatalog_delete.html',
                                       aicatalog=aicatalog,
                                       aicatalogs=aicatalogs,
                                       STATE=state)
        else:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            return render_template('AiCatalog_delete_denial.html',
                                   aicatalog=aicatalog,
                                   aicatalogs=aicatalogs)


# Entering the Catalog

# Ai Custom page


@app.route('/aicatalogs/<int:aicatalog_id>')
@app.route('/aicatalogs/<int:aicatalog_id>/list')
@ratelimit(limit=300, per=60 * 1)
def showAiCustom(aicatalog_id):
    # Check about the catalog is important or not
    if aicatalog_id not in Important_catalog_id:
        aicustoms = session.query(AiCustom).filter_by(
            aicatalog_id=aicatalog_id)
        aicatalog = session.query(AiCatalog).filter_by(id=aicatalog_id).one()
        aicatalogs = session.query(AiCatalog).all()
        if 'username' not in login_session:
            return render_template('AiCustom_show_public.html',
                                   aicustoms=aicustoms,
                                   aicatalog=aicatalog,
                                   aicatalogs=aicatalogs)
        else:
            return render_template('AiCustom_show.html',
                                   aicustoms=aicustoms,
                                   aicatalog=aicatalog,
                                   aicatalogs=aicatalogs)
    else:
        aicatalog = session.query(AiCatalog).filter_by(id=aicatalog_id).one()
        catalogname = aicatalog.name.lower()
        redirecturl = 'aicatalogs/%s/list' % catalogname
        return redirect(redirecturl)


@app.route('/aicatalogs/<int:aicatalog_id>/list/new',
           methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAiCustom(aicatalog_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newaicustom = AiCustom(name=request.form['name'],
                               description=request.form['description'],
                               picture=image,
                               aicatalog_id=aicatalog_id,
                               user_id=login_session['user_id'])
        session.add(newaicustom)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAiCustom', aicatalog_id=aicatalog_id))
    else:
        # Check about the catalog is important or not
        if aicatalog_id not in Important_catalog_id:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            # anti-forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('AiCustom_new.html',
                                   aicatalog=aicatalog,
                                   aicatalogs=aicatalogs,
                                   STATE=state)
        else:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            catalogname = aicatalog.name.lower()
            redirecturl = 'aicatalogs/%s/list/new' % catalogname
            return redirect(redirecturl)


@app.route('/aicatalogs/<int:aicatalog_id>/list/<int:aicustom_id>/edit',
           methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAiCustom(aicatalog_id, aicustom_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
        aicustom = session.query(AiCustom).filter_by(
                id=aicustom_id, aicatalog_id=aicatalog_id).one()

        # check is the user the owner of this item?
        if aicustom.user_id != login_session['user_id']:
            text = 'You are not the owner of this %s' % aicatalog.name
            flash(text)
            return redirect(url_for('showAiCustom',
                                    aicatalog_id=aicatalog.id))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editaicustom = session.query(AiCustom).filter_by(
            id=aicustom_id, aicatalog_id=aicatalog_id).one()

        editaicustom.name = request.form['name']
        editaicustom.description = request.form['description']
        editaicustom.picture = image

        session.add(editaicustom)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAiCustom', aicatalog_id=aicatalog_id))
    else:
        # Check about the catalog is important or not
        if aicatalog_id not in Important_catalog_id:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicustom = session.query(AiCustom).filter_by(
                id=aicustom_id, aicatalog_id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            # check is the user the owner of this item?
            if aicustom.user_id != login_session['user_id']:
                text = 'You are not the owner of this %s' % aicatalog.name
                flash(text)
                return redirect(url_for('showAiCustom',
                                        aicatalog_id=aicatalog.id))
            else:
                # anti forgery attack
                state = ''.join(random.choice(string.ascii_uppercase +
                                              string.digits
                                              ) for x in range(32))
                login_session['state'] = state
                return render_template('AiCustom_edit.html',
                                       aicatalog=aicatalog,
                                       aicustom=aicustom,
                                       aicatalogs=aicatalogs,
                                       STATE=state)
        else:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            catalogname = aicatalog.name.lower()
            redirecturl = 'aicatalogs/%s/list/%s/edit' % (catalogname,
                                                          aicustom_id)
            return redirect(redirecturl)


@app.route('/aicatalogs/<int:aicatalog_id>/list/<int:aicustom_id>/delete',
           methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAiCustom(aicatalog_id, aicustom_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
        aicustom = session.query(AiCustom).filter_by(
                id=aicustom_id, aicatalog_id=aicatalog_id).one()

        # check is the user the owner of this item?
        if aicustom.user_id != login_session['user_id']:
            text = 'You are not the owner of this %s' % aicatalog.name
            flash(text)
            return redirect(url_for('showAiCustom',
                                    aicatalog_id=aicatalog.id))

        deleteaicustom = session.query(AiCustom).filter_by(
            id=aicustom_id, aicatalog_id=aicatalog_id).one()

        session.delete(deleteaicustom)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAiCustom', aicatalog_id=aicatalog_id))
    else:
        # Check about the catalog is important or not
        if aicatalog_id not in Important_catalog_id:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            aicustom = session.query(AiCustom).filter_by(
                id=aicustom_id, aicatalog_id=aicatalog_id).one()
            aicatalogs = session.query(AiCatalog).all()
            # check is the user the owner of this item?
            if aicustom.user_id != login_session['user_id']:
                text = 'You are not the owner of this %s' % aicatalog.name
                flash(text)
                return redirect(url_for('showAiCustom',
                                        aicatalog_id=aicatalog.id))
            else:
                # anti forgery attack
                state = ''.join(random.choice(string.ascii_uppercase +
                                              string.digits
                                              ) for x in range(32))
                login_session['state'] = state
                return render_template('AiCustom_delete.html',
                                       aicatalog=aicatalog,
                                       aicustom=aicustom,
                                       aicatalogs=aicatalogs,
                                       STATE=state)
        else:
            aicatalog = session.query(AiCatalog).filter_by(
                id=aicatalog_id).one()
            catalogname = aicatalog.name.lower()
            redirecturl = 'aicatalogs/%s/list/%s/delete' % (catalogname,
                                                            aicustom_id)
            return redirect(redirecturl)


# Ai page

# Blue print definition for catalog
ai = Blueprint('ai', __name__)


@app.route('/aicatalogs/ai')
@app.route('/aicatalogs/ai/list')
@ratelimit(limit=300, per=60 * 1)
def showAi():
    ais = session.query(Ai).all()
    aicatalogs = session.query(AiCatalog).all()
    if 'username' not in login_session:
        return render_template('Ai_show_public.html',
                               ais=ais,
                               aicatalogs=aicatalogs)
    else:
        return render_template('Ai_show.html',
                               ais=ais,
                               aicatalogs=aicatalogs)


@ai.route('/list/new', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAi():
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newai = Ai(name=request.form['name'],
                   description=request.form['description'],
                   picture=image,
                   user_id=login_session['user_id'])
        session.add(newai)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAi'))
    else:
        # anti forgery attack
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in range(32))
        login_session['state'] = state
        aicatalogs = session.query(AiCatalog).all()
        return render_template('Ai_new.html',
                               aicatalogs=aicatalogs,
                               STATE=state)


@ai.route('/list/<int:ai_id>/edit', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAi(ai_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        ai = session.query(Ai).filter_by(id=ai_id).one()

        # check is the user the owner of this item?
        if ai.user_id != login_session['user_id']:
            flash('You are not the owner of this ai')
            return redirect(url_for('showAi'))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editai = session.query(Ai).filter_by(id=ai_id).one()

        editai.name = request.form['name']
        editai.description = request.form['description']
        editai.picture = image

        session.add(editai)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAi'))
    else:
        ai = session.query(Ai).filter_by(id=ai_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if ai.user_id != login_session['user_id']:
                flash('You are not the owner of this ai')
                return redirect(url_for('showAi'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('Ai_edit.html', ai=ai,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


@ai.route('/list/<int:ai_id>/delete', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAi(ai_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        ai = session.query(Ai).filter_by(id=ai_id).one()

        # check is the user the owner of this item?
        if ai.user_id != login_session['user_id']:
            flash('You are not the owner of this ai')
            return redirect(url_for('showAi'))

        deleteai = session.query(Ai).filter_by(id=ai_id).one()

        session.delete(deleteai)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAi'))
    else:
        ai = session.query(Ai).filter_by(id=ai_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if ai.user_id != login_session['user_id']:
                flash('You are not the owner of this ai')
                return redirect(url_for('showAi'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('Ai_delete.html',
                                   ai=ai,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


# Ai Book page

# Blue print definition for catalog
aibook = Blueprint('aibook', __name__)


@app.route('/aicatalogs/aibook')
@app.route('/aicatalogs/aibook/list')
@ratelimit(limit=300, per=60 * 1)
def showAiBook():
    aibooks = session.query(AiBook).all()
    aicatalogs = session.query(AiCatalog).all()
    if 'username' not in login_session:
        return render_template('AiBook_show_public.html',
                               aibooks=aibooks,
                               aicatalogs=aicatalogs)
    else:
        return render_template('AiBook_show.html',
                               aibooks=aibooks,
                               aicatalogs=aicatalogs)


@aibook.route('/aicatalogs/aibook/list/new', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAiBook():
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newaibook = AiBook(name=request.form['name'],
                           author=request.form['author'],
                           price=request.form['price'],
                           description=request.form['description'],
                           picture=image,
                           user_id=login_session['user_id'])
        session.add(newaibook)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAiBook'))
    else:
        # anti forgery attack
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in range(32))
        login_session['state'] = state
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiBook_new.html',
                               aicatalogs=aicatalogs,
                               STATE=state)


@aibook.route('/aicatalogs/aibook/list/<int:aibook_id>/edit',
              methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAiBook(aibook_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aibook = session.query(AiBook).filter_by(id=aibook_id).one()

        # check is the user the owner of this item?
        if aibook.user_id != login_session['user_id']:
            flash('You are not the owner of this ai book')
            return redirect(url_for('showAiBook'))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editaibook = session.query(AiBook).filter_by(id=aibook_id).one()

        editaibook.name = request.form['name']
        editaibook.author = request.form['author']
        editaibook.price = request.form['price']
        editaibook.description = request.form['description']
        editaibook.picture = image

        session.add(editaibook)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAiBook'))
    else:
        aibook = session.query(AiBook).filter_by(id=aibook_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if aibook.user_id != login_session['user_id']:
                flash('You are not the owner of this ai book')
                return redirect(url_for('showAiBook'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('AiBook_edit.html',
                                   aibook=aibook,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


@aibook.route('/aicatalogs/aibook/list/<int:aibook_id>/delete',
              methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAiBook(aibook_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aibook = session.query(AiBook).filter_by(id=aibook_id).one()

        # check is the user the owner of this item?
        if aibook.user_id != login_session['user_id']:
            flash('You are not the owner of this ai book')
            return redirect(url_for('showAiBook'))

        deleteaibook = session.query(AiBook).filter_by(id=aibook_id).one()

        session.delete(deleteaibook)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAiBook'))
    else:
        aibook = session.query(AiBook).filter_by(id=aibook_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if aibook.user_id != login_session['user_id']:
                flash('You are not the owner of this ai book')
                return redirect(url_for('showAiBook'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('AiBook_delete.html',
                                   aibook=aibook,
                                   aicatalogs=aicatalogs,
                                   STATE=state)

# Ai News page

# Blue print definition for catalog
ainews = Blueprint('ainews', __name__)


@app.route('/aicatalogs/ainews')
@app.route('/aicatalogs/ainews/list')
@ratelimit(limit=300, per=60 * 1)
def showAiNews():
    ainewss = session.query(AiNews).all()
    aicatalogs = session.query(AiCatalog).all()
    if 'username' not in login_session:
        return render_template('AiNews_show_public.html',
                               ainewss=ainewss,
                               aicatalogs=aicatalogs)
    else:
        return render_template('AiNews_show.html',
                               ainewss=ainewss,
                               aicatalogs=aicatalogs)


@ainews.route('/list/new', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAiNews():
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newainews = AiNews(name=request.form['name'],
                           description=request.form['description'],
                           picture=image,
                           user_id=login_session['user_id'])
        session.add(newainews)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAiNews'))
    else:
        # anti forgery attack
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in range(32))
        login_session['state'] = state
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiNews_new.html',
                               aicatalogs=aicatalogs,
                               STATE=state)


@ainews.route('/list/<int:ainews_id>/edit',
              methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAiNews(ainews_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        ainews = session.query(AiNews).filter_by(id=ainews_id).one()

        # check is the user the owner of this item?
        if ainews.user_id != login_session['user_id']:
            flash('You are not the owner of this ai news')
            return redirect(url_for('showAiNews'))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editainews = session.query(AiNews).filter_by(id=ainews_id).one()

        editainews.name = request.form['name']
        editainews.description = request.form['description']
        editainews.picture = image

        session.add(editainews)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAiNews'))
    else:
        ainews = session.query(AiNews).filter_by(id=ainews_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if ainews.user_id != login_session['user_id']:
                flash('You are not the owner of this ai news')
                return redirect(url_for('showAiNews'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('AiNews_edit.html',
                                   ainews=ainews,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


@ainews.route('/list/<int:ainews_id>/delete',
              methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAiNews(ainews_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        ainews = session.query(AiNews).filter_by(id=ainews_id).one()

        # check is the user the owner of this item?
        if ainews.user_id != login_session['user_id']:
            flash('You are not the owner of this ai news')
            return redirect(url_for('showAiNews'))

        deleteainews = session.query(AiNews).filter_by(id=ainews_id).one()

        session.delete(deleteainews)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAiNews'))
    else:
        ainews = session.query(AiNews).filter_by(id=ainews_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if ainews.user_id != login_session['user_id']:
                flash('You are not the owner of this ai news')
                return redirect(url_for('showAiNews'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            return render_template('AiNews_delete.html',
                                   ainews=ainews,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


# Ai Match page

# Blue print definition for catalog
aimatch = Blueprint('aimatch', __name__)


@app.route('/aicatalogs/aimatch')
@app.route('/aicatalogs/aimatch/list')
@ratelimit(limit=300, per=60 * 1)
def showAiMatch():
    aimatchs = session.query(AiMatch).all()
    aicatalogs = session.query(AiCatalog).all()
    if 'username' not in login_session:
        return render_template('AiMatch_show_public.html',
                               aimatchs=aimatchs,
                               aicatalogs=aicatalogs)
    else:
        return render_template('AiMatch_show.html',
                               aimatchs=aimatchs,
                               aicatalogs=aicatalogs)


@aimatch.route('/list/new', methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def newAiMatch():
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        newaimatch = AiMatch(name=request.form['name'],
                             participant_A=request.form['participant_A'],
                             participant_B=request.form['participant_B'],
                             place=request.form['place'],
                             description=request.form['description'],
                             picture=image,
                             user_id=login_session['user_id'])
        session.add(newaimatch)
        session.commit()
        flash('Successfully Created!')
        return redirect(url_for('showAiMatch'))
    else:
        # anti forgery attack
        state = ''.join(random.choice(string.ascii_uppercase +
                        string.digits) for x in range(32))
        login_session['state'] = state
        aicatalogs = session.query(AiCatalog).all()
        return render_template('AiMatch_new.html',
                               aicatalogs=aicatalogs,
                               STATE=state)


@aimatch.route('/list/<int:aimatch_id>/edit',
               methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def editAiMatch(aimatch_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()

        # check is the user the owner of this item?
        if aimatch.user_id != login_session['user_id']:
            flash('You are not the owner of this ai match')
            return redirect(url_for('showAiMatch'))

        # If no picture given fill it with default picture
        if request.form['picture'] == '':
            image = url_for('static', filename='no_pic.jpg')
        else:
            image = request.form['picture']

        editaimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()

        editaimatch.name = request.form['name']
        editaimatch.participant_A = request.form['participant_A']
        editaimatch.participant_B = request.form['participant_B']
        editaimatch.place = request.form['place']
        editaimatch.description = request.form['description']
        editaimatch.picture = image

        session.add(editaimatch)
        session.commit()
        flash('Successfully Edited!')
        return redirect(url_for('showAiMatch'))
    else:
        aimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if aimatch.user_id != login_session['user_id']:
                flash('You are not the owner of this ai match')
                return redirect(url_for('showAiMatch'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            aicatalogs = session.query(AiCatalog).all()
            return render_template('AiMatch_edit.html',
                                   aimatch=aimatch,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


@aimatch.route('/list/<int:aimatch_id>/delete',
               methods=['GET', 'POST'])
@login_required
@ratelimit(limit=300, per=60 * 1)
def deleteAiMatch(aimatch_id):
    if request.method == 'POST':
        # check token valid
        if request.args.get('state') != login_session['state']:
            response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        aimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()

        # check is the user the owner of this item?
        if aimatch.user_id != login_session['user_id']:
            flash('You are not the owner of this ai match')
            return redirect(url_for('showAiMatch'))

        deleteaimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()

        session.delete(deleteaimatch)
        session.commit()
        flash('Successfully Deleted!')
        return redirect(url_for('showAiMatch'))
    else:
        aimatch = session.query(AiMatch).filter_by(id=aimatch_id).one()
        aicatalogs = session.query(AiCatalog).all()
        # check is the user the owner of this item?
        if aimatch.user_id != login_session['user_id']:
                flash('You are not the owner of this ai match')
                return redirect(url_for('showAiMatch'))
        else:
            # anti forgery attack
            state = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for x in range(32))
            login_session['state'] = state
            aicatalogs = session.query(AiCatalog).all()
            return render_template('AiMatch_delete.html',
                                   aimatch=aimatch,
                                   aicatalogs=aicatalogs,
                                   STATE=state)


# Add Blueprint to app


app.register_blueprint(api, url_prefix='/api/v1')
app.register_blueprint(catalog, url_prefix='/aicatalogs')
app.register_blueprint(ai, url_prefix='/aicatalogs/ai')
app.register_blueprint(aibook, url_prefix='/aicatalogs/aibook')
app.register_blueprint(ainews, url_prefix='/aicatalogs/ainews')
app.register_blueprint(aimatch, url_prefix='/aicatalogs/aimatch')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'Super_secret_key'
    app.run(host='0.0.0.0', port=8000)
