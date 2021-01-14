from safrs import SAFRSAPI

from api.json_encoder import SAFRSJSONEncoderExt
from database import models


def expose_models(app, HOST="localhost", PORT=5000, API_PREFIX="/api"):
    """ generate api.expose_object(<table>)
    """