from safrs import SAFRSAPI

from api.json_encoder import SAFRSJSONEncoderExt
from database import models


def expose_models(app, HOST="localhost", PORT=5000, API_PREFIX="/api"):
    """ generated file - expose endpoints
    """
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX, json_encoder=SAFRSJSONEncoderExt)
    api.expose_object(models.User)
    api.expose_object(models.Book)
    api.expose_object(models.StoreModel)
    api.expose_object(models.ItemModel)
    print("Created API: http://{}:{}{}".format(HOST, PORT, API_PREFIX))
