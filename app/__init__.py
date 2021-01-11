import safrs
from logic_bank.logic_bank import LogicBank
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from admin.admin_view_ext import AdminViewExt
from database import db  # , session  FIXME eh?
from flask import Flask
from api.json_encoder import SAFRSJSONEncoderExt
from logic import declare_logic

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")
from safrs import SAFRSAPI, ValidationError
from database import models
from database.models import user, book


def create_app(config_filename=None, host="localhost"):
    app = Flask("API Logic Server")
    app.config.from_object("config.Config")
    #    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite://")
    from database import db  # , session  FIXME eh?
    use_file = True
    if use_file:
        db.db.init_app(app)
        session = db.session
    else:
        # db: SQLAlchemy = SQLAlchemy()
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
        """ FIXEM db assumed to exist
        db.create_all()
        # Populate the db with users and a books and add the book to the user.books relationship
        #  session.commit()
        for i in range(1):
            user = User(name=f"user{i}", email=f"email{i}@email.com")
            book = Book(name=f"test book {i}")
            user.books.append(book)
            session.commit()
        """

        create_api(app, host)
        create_admin_ui(app)

    return app


# create the api endpointsx
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
