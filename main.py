import sqlite3
from flask import Flask, url_for, request, render_template, g
app = Flask(__name__)

DATABASE = '/Users/imyjimmy/Dropbox/for_alex/indiaAlleleFinder/db/database.db'

app.config.from_object(__name__)

def connect_to_database():
	return sqlite3.connect(app.config['DATABASE'])

#@app.before_request
#def before_request():
#	g.db = connect_db()

def get_db():
	db = getattr(g, '_db', None)
	if db is None:
		db = g._db = connect_to_database()
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_db', None)
	if db is not None:
		db.close()

def execute_query(query, args=()):
	current = get_db().execute(query, args)
	rows = current.fetchall()
	current.close()
	return rows

@app.route('/')
@app.route('/index.html')
def index():
	#return 'Welcome to India Allele Finder'
	return render_template('index.html') #will be the search page

@app.route('/viewdb')
def viewdb():
	rows = execute_query("""SELECT * FROM alleles""")
	return '<br>'.join(str(row) for row in rows)

@app.route('/gene/<gene>')
def sort_by_gene(gene):
	rows = execute_query("""SELECT * FROM alleles WHERE GenerefGene = ?""", [gene])
	return '<br>'.join(str(row) for row in rows)

@app.route('/chr/<chromosome>')
def sort_by_chr(chromosome):
	rows = execute_query("""SELECT * FROM alleles WHERE Chr = ?""", [chromosome])
	return '<br>'.join(str(row) for row in rows)

@app.route('/search')
def search():
	query = request.args.get('search')
	results = processQuery(query)
	print("results: " + str(results))
	html = '<br>'.join(str(row) for row in results)
	return render_template('search.html', query=query, results=results, h=html)

def processQuery(query):
	gene_rows = execute_query("""SELECT * FROM alleles WHERE GenerefGene = ?""", [query])
	print('length of rows: ' + str(len(gene_rows)))
	# for row in gene_rows:
	#  	print("genes: " + str(row))
	return gene_rows

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

