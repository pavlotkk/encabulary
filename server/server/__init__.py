def create_app(config=None):
    from flask import Flask

    import server.views as views
    import server.api as api
    from server.database import db

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    if config:
        app.config.update(config)

    db.init_app(app)

    app.register_blueprint(views.index_blueprint)
    app.register_blueprint(api.api_blueprint)

    return app
