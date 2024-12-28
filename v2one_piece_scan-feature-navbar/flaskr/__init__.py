#Gérez explicitement les erreurs potentielles liées au chargement de configurations ou à la création du répertoire.


#Encouragez l'utilisation de variables d'environnement pour les clés secrètes et les configurations sensibles.

#Ajoutez des vérifications pour garantir que les modules importés (comme db et text_routes) sont correctement chargés.

#Permettez facilement l'enregistrement de blueprints supplémentaires dans le futur.

import os
from flask import Flask

def create_app(test_config=None):
    """
    Flask factory function. This function creates and configures the Flask app.

    Args:
        test_config (dict, optional): A configuration dictionary for testing.

    Returns:
        Flask app instance.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'dev'),  # Use env variable or default to 'dev'
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Load the test config if passed in, otherwise load config.py
    if test_config is None:
        try:
            app.config.from_pyfile('config.py', silent=True)  # Load config.py if available
        except FileNotFoundError:
            app.logger.warning("No config.py file found, using default configuration.")
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        app.logger.error(f"Error creating instance folder: {e}")
        raise

    # Initialize the database
    try:
        from . import db
        db.init_app(app)
    except ImportError as e:
        app.logger.error(f"Database initialization failed: {e}")
        raise

    # Register the blueprint(s)
    try:
        from . import text_routes
        app.register_blueprint(text_routes.bp)
    except ImportError as e:
        app.logger.error(f"Failed to register blueprint: {e}")
        raise

    app.logger.info("Application setup complete.")
    return app
