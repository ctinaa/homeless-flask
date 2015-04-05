#!/usr/bin/python 

from flask import * 
from flask_oauth import OAuth
from models import User, db 
import sqlite3 
# from sqlite3 import sqlite3
# from models import db
from sys import * 
from os import *

connection = "mysql://%s:%s@%s:3306/%s" % (
	'root', 'lahacks',
	'localhost', 'homeless')

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = connection 
app.secret_key = "super secret"
db.init_app(app)

with app.app_context():
	db.create_all()
	db.session.commit() 

@app.route('/')
def home(): 
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login3.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signon')
def signon():
    return render_template('signon.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

@app.route('/fb_test')
def fb(): 
	data = facebook.get('/me').data
	#if 'id' in data and 'firstname' in data and 'lastname' in data and 'email' in data: 			
	# user_id = data['id']
	user_firstname = data['first_name']
	user_lastname = data['last_name']
	user_email = data['email']
    	bio = '' 
    
	new_user = User(user_firstname, user_lastname, user_firstname, user_email, bio)

        if not User.query.filter(email=user_email).count():
            db.session.add(new_user)
            db.session.commit() 

	return render_template('profile.html', firstname=user_firstname, lastname=user_lastname)
#----------------------------------------
# facebook authentication
#----------------------------------------



FACEBOOK_APP_ID = '1411581279157960'
FACEBOOK_APP_SECRET = '7e0c69fba4ccf386f905e11451f53e46'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('fb')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('home'))
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
