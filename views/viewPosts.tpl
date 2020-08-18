<div id="psstColumns">
    % for post in posts:
    <div class='psst'>
        <div id='profileTab'>
            <a href="/users/{{post[2]}}">
            <img src="{{post[3]}}">
            <div id="name"> {{post[2]}} </div>
            </a>
        </div>
        <p>
        {{!post[4]}}
        </p>
        <div id='timestamp'>
            {{post[1]}}
        </div>
    </div>
    % end
</div>