import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Defining our DB URI
app.config['SLQALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(user=os.getenv('POSTGRES_USER'),  passwd=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port=5432, table=os.getenv('POSTGRES_DB')) 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # connecting to our db
migrate = Migrate(app, db) # migrating the schema

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

# Route initialization
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            return f"User {username} created successfully"
        else:
            return error, 418

    ## TODO: Return a restister page
    return "Register Page not yet implemented", 501

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    ## TODO: Return a login page
    return "Login Page not yet implemented", 501

@app.route('/health')
def health():
    return "Works"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about/ishika')
def about_ishika():
    return render_template('ishika.html', fellowName='Ishika');

@app.route('/about/frankie')
def about_frankie():
    return render_template('frankie.html', fellowName='Frankie');

@app.route('/about/sebastian')
def about_sebastian():
    return render_template('sebastian.html', fellowName='Sebastian');
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/post')
def post():
    return render_template('post.html', title="Post")
