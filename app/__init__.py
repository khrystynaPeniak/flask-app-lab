from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name='config.DevConfig'):
    app = Flask(__name__)
    app.config.from_object(config_name)  # налаштування з об'єкта
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'users.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from . import views
        from app.users.models import User
        
        from .posts import post_bp
        from .users import user_bp

        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp)
        
        #from app.posts.models import Post
        #db.create_all()
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now()
            db.session.commit()
            
    return app