# use sqlite for user auth?
import sqlite3
from contextlib import closing # with statement for database
from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash
from functools import wraps
import os

app = Flask(__name__)
os.environ['CURAGA_CONFIG'] = 'settings/base.py'
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CURAGA_CONFIG')


# return a db handle
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# imports schema into db
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    db = get_db()

    cursor = db.execute('select * from users where name=? and password=?',
                        [username, password]
                        )
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False
    # return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def home():
    ip_address = request.remote_addr
    return render_template('home.html')


@app.route("/upload")
@requires_auth
def upload():
    """accepts a post request that stores a file on the server
    and makes a record of the package's existance in the db"""
    # print request.authorization.username
    # db = get_db()
    # db.execute('insert into packages (name) values (?)', [])
    # db.commit()
    return "upload"


@app.route("/package")
def package():
    """accepts a get request and returns a script that when piped
    to the shell will download the package"""

    # log the ip address that downloads the package
    ip_address = request.remote_addr
    return "package"


@app.route("/auth/register")
def register():
    return "Auth"


if __name__ == "__main__":
    app.run()