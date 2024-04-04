from fastapi import *
from api import *

app = FastAPI(
    docs_url = "/",
    redoc_url = None
)

internal(app)
version_1(app)
