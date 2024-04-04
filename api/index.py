from fastapi import *
from internal import internal
from v1 import version_1

app = FastAPI(
    docs_url = "/",
    redoc_url = None
)

internal(app)
version_1(app)
