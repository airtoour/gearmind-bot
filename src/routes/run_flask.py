from src.db.config import app, db
from src.routes.signup import signup_bp


app.register_blueprint(signup_bp, url_prefix='/signup')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)