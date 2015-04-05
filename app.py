#!/usr/bin/python 

from flask import * 

app = Flask(__name__) 

@app.route('/')
def home(): 
	return render_template('index.html')

@app.route('/signin')
def signin():
	return render_template('signin.html')
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
