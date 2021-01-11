import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from admin.admin_view_ext import AdminViewExt
from api import create_api_models
from database import db  # , session  FIXME eh?
from flask import Flask
from api.json_encoder import SAFRSJSONEncoderExt
from logic import declare_logic
from safrs import SAFRSAPI, ValidationError
from database import models
from database.models import user, book

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")


def create_app(config_filename=None, host="localhost"):
    app = Flask("API Logic Server")
    app.config.from_object("config.Config")
    #    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")
    from database import db  # , session  FIXME eh?
    use_file = True
    if use_file:  # this is a little obscure - can we bring inline?
        db.db.init_app(app)
        session = db.session
    else:
        # db: SQLAlchemy = SQLAlchemy()  REMOVE
        db = safrs.DB  # opens (what?) database, returning session
        Base: declarative_base = db.Model
        session: Session = db.session
        print("got session: " + str(session))

    import logic

    def constraint_handler(message: str, constraint: object,
                           logic_row: LogicRow):  # message: str, constr: constraint, row: logic_row):
        raise ValidationError(message)

    LogicBank.activate(session=session, activator=declare_logic, constraint_event=constraint_handler)

    with app.app_context():

        # create_api(app, host)   REMOVE
        create_api_models.create_api(app, host)
        create_admin_ui(app)

    return app


# create the api endpointsx  REMOVE
def create_api(app, HOST="localhost", PORT=5000, API_PREFIX="/api"):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX, json_encoder=SAFRSJSONEncoderExt)
    api.expose_object(models.User)
    api.expose_object(models.Book)
    api.expose_object(models.StoreModel)
    api.expose_object(models.ItemModel)
    print("Created API: http://{}:{}{}".format(HOST, PORT, API_PREFIX))


def create_admin_ui(app):
    try:
        admin = Admin(app, url="/admin")
        for model in [models.User, models.Book, models.StoreModel, models.ItemModel]:
            #  admin.add_view(sqla.ModelView(model, db.session))
            admin.add_view(AdminViewExt(model, db.session))
    except Exception as exc:
        print(f"Failed to add flask-admin view {exc}")


def create_app_for_test(config_filename=None, host="localhost"):
    app = Flask("LogicBank Demo App")
    app.config.from_object("config.Config")
    db.init_app(app)
    #  https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
    app.app_context().push()
    return app
