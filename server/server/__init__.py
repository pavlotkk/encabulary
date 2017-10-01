def create_app(config=None):
    from flask import Flask

    from server.views import routs as view_routs
    from server.database import db

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    if config:
        app.config.update(config)

    db.init_app(app)

    app.register_blueprint(view_routs.view_blueprint)

    return app
