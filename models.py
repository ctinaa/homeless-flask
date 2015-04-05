from flask.ext.sqlalchemy import SQLAlchemy 

db = SQLAlchemy() 

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(200))
	lastname = db.Column(db.String(200))
	username = db.Column(db.String(200), unique=True)
	email = db.Column(db.String(200), unique=True)
	bio = db.Column(db.Text())

	def __init__(self, firstname, lastname, username, email, bio):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.email = email
		self.bio = bio 