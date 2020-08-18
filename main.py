__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, redirect, response

import interface, users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()

@application.route('/')
def index(login=None):
    user = users.session_user(COMP249Db())
    info = {
        'title': 'Psst!',
        'message': 'Welcome to Psst!',
        'user': user,
        'avatar': interface.user_avatar(COMP249Db(), user),
        'login': login
    }
    info['posts'] = interface.post_list(COMP249Db())
    return template('views/index.html', info)

@application.route('/about')
def about():
    user = users.session_user(COMP249Db())
    info = {
        'title': 'Psst!',
        'message': 'About',
        'header': 'About Psst!',
        'user': user,
        'avatar': interface.user_avatar(COMP249Db(), user),
        'login': login
    }
    return template('views/about.html', info)

@application.route('/search', method='POST')
def myPosts():
    user = users.session_user(COMP249Db())
    searchkey = request.forms.get('searchbar')
    info = {
        'title': 'Psst!',
        'message': "Search",
        'header': 'Posts with "'+searchkey+'"',
        'user': user,
        'avatar': interface.user_avatar(COMP249Db(), user),
        'login': login
    }
    info['posts'] = interface.post_search(COMP249Db(), searchkey)
    print(info['posts'])
    return template('views/search.html', info)

@application.route('/users/<name:path>')
def userpage(name):
    user = users.session_user(COMP249Db())
    info = {
        'title': 'Psst!',
        'message': name + "'s posts",
        'header': 'Posts by ' + name,
        'user': user,
        'avatar': interface.user_avatar(COMP249Db(), user),
        'login': login
    }
    info['posts'] = interface.post_list(COMP249Db(), name)
    return template('views/user.html', info)

@application.route('/mentions/<name:path>')
def mentionspage(name):
    user = users.session_user(COMP249Db())
    info = {
        'title': 'Psst!',
        'message': name + "'s mentions",
        'header': 'Posts that mention ' + name,
        'user': user,
        'avatar': interface.user_avatar(COMP249Db(), user),
        'login': login
    }
    info['posts'] = interface.post_list_mentions(COMP249Db(), name)
    return template('views/mentions.html', info)


@application.route('/login', method='POST')
def login():

    usern = request.forms.get('nick')
    passw = request.forms.get('password')

    if users.check_login(COMP249Db(), usern, passw) is True:
        users.delete_session(COMP249Db(), usern)
        session = users.generate_session(COMP249Db(), usern)
        return redirect('/')
    return index(False)

@application.route('/logout', method='POST')
def logout():
    users.delete_session(COMP249Db(), users.session_user(COMP249Db()))
    return redirect('/')

@application.route('/post', method='POST')
def post():
    user = users.session_user(COMP249Db())
    message = request.forms.get('post')
    if not message.isspace():
        interface.post_add(COMP249Db(), user, message)
    return redirect('/')


@application.route('/my_posts', method='POST')
def myPosts():
    user = users.session_user(COMP249Db())
    link = '/users/' + user
    return redirect(link)

@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')

@application.route('/img/<filename:path>')
def img(filename):
    return static_file(filename=filename, root='img')


if __name__ == '__main__':
    application.run(debug=True, port=8010)
