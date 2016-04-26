# coding: utf-8

import sys
import settings

from flask import Flask
from flask.ext.cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import db

from jinja_filters import message_alert_glyph, messages_alert_tags

from routes import routes

from oauth_provider import CodeRunnerOAuth2Provider


app = Flask('CodeRunner', template_folder='templates')
app.debug = settings.DEBUG
app.secret_key = 'c0derunner'

# Cross headers
cors = CORS(app, resources={
    r'/api/*': {
        'origins': '*'
    }
})

# App config
app.config.update(settings.CONFIG)

# DB
db.init_app(app)

# Oauth
oauth = CodeRunnerOAuth2Provider(app)

# Migrate manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Jinja filters
app.jinja_env.filters['glyph_class'] = message_alert_glyph
app.jinja_env.filters['tag_class'] = messages_alert_tags


# Routes
for route, param in routes.items():
    if isinstance(param, list):
        if len(param) > 2:
            app.add_url_rule(route, param[0], param[1], **param[2])
        else:
            app.add_url_rule(route, param[0], param[1])

    else:
        app.add_url_rule(route, view_func=param)


if __name__ == '__main__':
    if len(sys.argv) == 1 or \
            sys.argv[1] == 'run':
        # Run server
        app.run(
            host=settings.SERVER_HOST,
            port=settings.SERVER_POST
        )
    else:
        # Run migration manager
        manager.run()
