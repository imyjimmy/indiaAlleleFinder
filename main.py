import sqlite3
from flask import Flask, url_for, request, render_template, g
app = Flask(__name__)

DATABASE = './db/database.db'

#@app.before_request
#def before_request():
#	g.db = connect_db()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_to_database()
	return db

def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/')
@app.route('/index.html')
def index():
	#return 'Welcome to India Allele Finder'
	return render_template('index.html') #will be the search page

@app.route('/search')
def search():
	query = request.args.get('search')
	#return "heyy! %s" % query
	return render_template('search.html', query=query)


###THE FOLLOWING IS EXAMPLE CODE###
@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
#	return "Hello World!"
	return render_template('hello.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_login_form()

def do_the_login():
	return "login url"

def show_login_form():
	return "login form url"

@app.route('/user/<username>')
def showUserProfile(username):
	return 'User: ' + username

with app.test_request_context():
	print url_for('index')
	print url_for('login')
	print url_for('login', next='/')
	print url_for('showUserProfile', username='John Doe')

@app.route('/post/<int:postID>')
def showPost(postID):
	return 'Post %d' % postID

if __name__ == "__main__":
	app.run(debug=True)

