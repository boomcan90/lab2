# authors: Arjun Singh Brar - 1001189
#          Dhanya Janaki    - 1001288

from flask import Flask, render_template, redirect, url_for, request, send_file
import flask
import flask_login
import feedparser
import unicodedata
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='/static', static_folder='static')
Bootstrap(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'newuser': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html', d={})
        #return '''
         #      <form action='login' method='POST'>
          #      <input type='text' name='email' id='email' placeholder='email'></input>
           #     <input type='password' name='pw' id='pw' placeholder='password'></input>
            #    <input type='submit' name='submit'></input>
             #  </form>
              # '''

    email = flask.request.form['username']
    if not email in users.keys():
        return render_template('login.html', d={'error': 'Invalid username!'})
    if flask.request.form['password'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('hello', name=flask_login.current_user.id))

    return render_template('login.html', d={'error': 'Invalid Username or passworr'})

@app.route('/')
@flask_login.login_required
def index():
    return flask.redirect(flask.url_for('hello', name=flask_login.current_user.id))

@app.route('/hello/<name>')
@flask_login.login_required
def hello(name):
    return render_template('colorclock.html', name=name)

@app.route('/feed')
@flask_login.login_required
def feed():
    RSS_URLS = ['http://www.polygon.com/rss/group/news/index.xml']
    entries = []
    for url in RSS_URLS:
        entries.extend(feedparser.parse(url).entries)

    entries_sorted = sorted(
                           entries,
                           key=lambda e: e.published_parsed,
                           reverse=True)
    return render_template(
            'feed.html',
            entries=entries_sorted
            )

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__=='__main__':
    app.config["SECRET_KEY"] = "TEAMROCKET"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)



