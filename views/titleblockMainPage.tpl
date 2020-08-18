<div id="titleblock">
    <div id="colLeft">
        % if user is None:
            <a href="/register">
            <img src="/img/welcomeImg.png" id="joinImg" >
            </a>
        % else:
            % include("addPost.tpl")
        % end
    </div>
    <div id="colRight">
        <div id="loginBox">
        % if user is None:
            % include("loginBox.tpl")
        % else:
            % include("loggedInBox.tpl")
        % end
        </div>
    </div>
</div>