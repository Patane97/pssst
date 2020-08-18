'''
Created on Mar 26, 2012

@author: steve
'''

import bottle

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cur = db.cursor()
    cur.execute("""SELECT password
                    FROM users 
                    WHERE nick=?""", (usernick,))
    result = cur.fetchone()
    if result is None or db.crypt(password) != result[0]:
        return False
    else:
        return True

def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cur = db.cursor()
    """checking if usernick exists"""
    cur.execute("""SELECT *
                    FROM users
                    WHERE nick=?""",(usernick,))
    result = cur.fetchone()
    if result is None:
        return None

    """checking if sessionid already exists"""
    cur.execute("""SELECT sessionid
                    FROM sessions
                    WHERE usernick=?""",(usernick,))
    result = cur.fetchone()
    if result is not None:
        return result[0]

    """adding new session to sessions table & creating session cookie"""
    import uuid
    sessionid = str(uuid.uuid4())
    cur.execute("""INSERT INTO sessions 
                    VALUES(?,?)""",(sessionid, usernick))
    db.commit()

    bottle.response.set_cookie(COOKIE_NAME, sessionid)

    return sessionid

def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    cur.execute("""DELETE FROM sessions
                    WHERE usernick=?""",(usernick,))
    db.commit()

def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    sessionid = bottle.request.get_cookie(COOKIE_NAME)
    cur = db.cursor()
    cur.execute("""SELECT usernick
                    FROM sessions
                    WHERE sessionid=?""",(sessionid,))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    return None