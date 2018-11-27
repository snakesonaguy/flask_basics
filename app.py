from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(

    SECRET_KEY='secretkey',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Dd5Ro2k2@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/new')
def query_strings(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1>The greeting is: {0}. </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Steven'):
    return '<h1>Hello there {} !</h1>'.format(name)

@app.route('/text/<string:word>')
def use_string(word):
    return '<h1>The string is {}.<h1>'.format(word)

@app.route('/number/<int:num>')
def use_num(num):
    return '<h1>The number is {}.</h1>'.format(str(num))

@app.route('/adding/<int:num1>/<int:num2>')
def add_nums(num1, num2):
    return '<h1>The sum is: {}.</h1>'.format(str(num1 + num2))

@app.route('/floatadd/<float:num3>/<float:num4>')
def add_floats(num3, num4):
    return '<h1>The sum of the floats is: {}.</h1>'.format(num3 + num4)

@app.route('/template')
def user_template():
    return render_template('temp1.html')

@app.route('/watch')
def movies():
    movie_list = ['Movie1', 'Movie2', 'Movie3']
    return render_template('movies.html', movies=movie_list, name='Steven')

@app.route('/tables')
def movies_plus():
    movie_dict = {'Movie1':1.2, 'Movie2': 3.4, 'Movie3':4.3}
    return render_template('table_data.html', movies=movie_dict, name='Melissa')

@app.route('/filter')
def filter_data():
    movie_dict = {'Movie1': 2.2, 'Movie2': 3.4, 'Movie3': 1.3}
    return render_template('filter.html', movies=movie_dict, name=None, film='Movie4')


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):

        self.name = name

    def __repr__(self):
        return 'Publisher Name: {}'.format(self.name)

class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}.'.format(self.title, self.author)




if __name__ == '__main__':
    db.create_all()
    app.run()