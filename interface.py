"""
Created on Feb 20, 2015

@author: steve cassidy
"""

import re

def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""
    content = content.replace('&', '&amp;')
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    content = re.sub(r'((http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)', r"<a href='\1'>\1</a>", content)
    content = re.sub(r'\@((\w+\.\w+)|(\w+))', r"<a href='/users/\1'>@\1</a>", content)
    content = re.sub(r'\#(\w+)', r"<strong class='hashtag'>#\1</strong>", content)

    return content

def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content) 
    """
    cur = db.cursor()
    if usernick is None:
        cur.execute("""SELECT id, timestamp, usernick, avatar, content
                        FROM posts, users 
                        WHERE usernick=users.nick
                        ORDER BY timestamp DESC""")
    else:
        cur.execute("""SELECT id, timestamp, usernick, avatar, content
                        FROM posts, users 
                        WHERE usernick=users.nick AND usernick=?
                        ORDER BY timestamp DESC""", (usernick,))
    return cur.fetchmany(size=limit)

def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cur = db.cursor()
    cur.execute("""SELECT id, timestamp, usernick, avatar, content
                    FROM posts, users
                    WHERE usernick=users.nick AND content LIKE ?
                    ORDER BY timestamp DESC""", ("%@"+usernick+"%",))
    return cur.fetchmany(size=limit)

def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""
    cur = db.cursor()
    if len(message) < 150:
        from datetime import datetime
        cur.execute("""INSERT INTO posts(timestamp, usernick, content) VALUES(?,?,?)""", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usernick, post_to_html(message)))
        db.commit()
        return cur.lastrowid
    return None

def user_avatar(db, usernick):
    """returns the users avatar link"""
    cur = db.cursor()
    cur.execute("""SELECT avatar
                    FROM users
                    WHERE nick=?""", (usernick,))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    return None

def post_search(db, searchkey, limit=50):
    """returns a list of posts that contain searchkey within their content"""
    cur = db.cursor()
    print(searchkey)
    cur.execute("""SELECT id, timestamp, usernick, avatar, content
                    FROM posts, users
                    WHERE usernick=users.nick AND content LIKE ?
                    ORDER BY timestamp DESC""", ("%"+searchkey+"%",))
    return cur.fetchmany(size=limit)