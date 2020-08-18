<div id="titleblock">
    <div id="colLeft">
        <h1 id="header">{{header}}</h1>
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