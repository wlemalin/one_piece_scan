import os
from flask import Flask

def create_app(test_config=None):
    """
    Flask factory function see flask tutorial. 
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # don't return error if config.py doesn t exist
    else:
        app.config.from_mapping(test_config) # load the test config if passed in

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Initialize the database
    from . import db
    db.init_app(app)
    

    # Register the blueprint
    from . import text_routes
    app.register_blueprint(text_routes.bp)

    return app
