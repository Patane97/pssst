
<img src="{{avatar}}" id="avatar">
<h3>Logged in as {{user}}!</h3>

<form method="POST" action="/logout" id='logoutform'>
    <input type='submit' value='Logout'>
</form>

<form method="POST" action="/my_posts" id='mypostsform'>
    <input type='submit' value='My Posts'>
</form>