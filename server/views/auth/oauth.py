from flask import redirect, url_for

from oauth_provider import CodeRunnerOAuth2Provider

from utils import current_user


oauth = CodeRunnerOAuth2Provider()


@oauth.token_handler
def access_token():
    return None


@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()

    if not user:
        return redirect(url_for('login'))

    # if user is authorized return True
    return True
