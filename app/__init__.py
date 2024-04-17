from flask import Flask
from flask_restx import Api
from .routes import configure_api
import logging

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    api = Api(app, version='1.0', title='Citation Tool API', description='A simple Citation Generator API')
    
    # Setup logging
    logging.basicConfig(filename='citations.log', level=logging.INFO, format='%(asctime)s:%(message)s')
    
    configure_api(api)  # This should configure your API with namespaces and routes from routes.py
    
    return app

app = create_app()
api = Api(app, version='1.0', title='Citation Tool API', description='A simple Citation Generator API')

configure_api(api)  # This will configure your API with namespaces and routes from routes.py