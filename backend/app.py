import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from routes.visitantes import visitantes_bp
from flask_cors import CORS

load_dotenv()


def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    default_db_uri = os.getenv("DATABASE_URL")

    if not default_db_uri and all([db_user, db_password, db_host, db_name]):
        default_db_uri = (
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
        )
    elif not default_db_uri:
        # Fallback seguro para entornos locales sin variables definidas
        default_db_uri = "sqlite:///visitantes.db"

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=default_db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(visitantes_bp)

    if not app.config.get("TESTING"):
        with app.app_context():
            try:
                db.create_all()
                print("Base de datos inicializada correctamente")
            except Exception as e:
                print(f"No se pudo conectar a la base de datos: {e}")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


