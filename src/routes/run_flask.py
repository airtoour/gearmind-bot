from src.db.config import app, db
from src.routes.signup import signup_bp
from src.routes.login import logon_bp


app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)