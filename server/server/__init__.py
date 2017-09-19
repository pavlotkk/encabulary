from flask import Flask

import server.views as views
from server.config import config
from server.database import db_session

app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(views.index_blueprint)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
