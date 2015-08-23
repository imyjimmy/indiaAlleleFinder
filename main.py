from flask import Flask, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
	#return 'Welcome to India Allele Finder'
	return render_template('index.html') #will be the search page

@app.route('/search')
def search():
	return "heyy!"
	#query = request.args.get('search')


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

