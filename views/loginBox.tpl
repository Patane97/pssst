% if login is False:
    <h2>Login Failed, please try again</h2>
% else:
    <h2>Already have an account?</h2>
% end
<h1>Login</h1>
<form method="POST" action="/login" id='loginform'>
<label><b>Username</b></label>
    <input type="text"  name="nick" required>
<label><b>Password</b></label>
    <input type="password"  name="password">
    <input type='submit' value='Login'>
</form>