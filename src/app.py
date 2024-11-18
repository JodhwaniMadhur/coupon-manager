from flask import Flask
from config import Config
from models import db
from routes import api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
    
    


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[app.config["RATELIMIT_DEFAULT"]]
    )
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(api, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)