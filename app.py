#!/usr/bin/python 

from flask import * 
from flask_oauth import OAuth
# from models import db
# from settings import *
# from utilities import * 
from sys import * 
from os import *
app = Flask(__name__) 
app.secret_key = "super secret"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

db = SQLAlchemy() 

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(200))
	lastname = db.Column(db.String(200))
	username = db.Column(db.String(200), unique=True)
	email = db.Column(db.String(200), unique=True)
	# password = db.Column(db.String(200))
	# created_date = db.Column(db.DateTime)
	# updated_date = db.Column(db.DateTime)
	# active = db.Column(db.Boolean, default=True)
	def __init__(self, firstname, lastname, username, email):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.email = email
		# self.password = password
		# self.created_date = created_date
		# self.updated_date = updated_date
		# self.active = active 

with app.app_context():
	db.create_all()
	db.session.commit() 

@app.route('/')
def home(): 
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login3.html')

@app.route('/fb_test')
def fb(): 
	data = facebook.get('/me').data
	if 'id' in data and 'firstname' in data and 'lastname' in data and 'email' in data: 
		user_id = data['id']
		user_firstname = data['firstname']
		user_lastname = data['lastname']
		user_email = data['email']

	return render_template('fb_test.html', id=user_id, firstname=user_firstname)

#----------------------------------------
# facebook authentication
#----------------------------------------



FACEBOOK_APP_ID = '1626770800876369'
FACEBOOK_APP_SECRET = '34a81ae3bad388550d59284c9e2422c4'

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
    next_url = request.args.get('next') or url_for('home')
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
