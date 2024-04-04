from fastapi import *
from fastapi.responses import RedirectResponse

app = FastAPI(
    docs_url = None,
    redoc_url = None,
    default_response_class = responses.RedirectResponse
)

@app.get("/", status_code = 308)
async def doc():
    return f"https://api.plazmamc.org/"

@app.get("/c/{color:int}/{content:str}", status_code = 308)
@app.get("/c/{color:int}/{name:str}/{content:str}", status_code = 308)
async def main(color: int, content: str, name: str = ""):
    return f"https://api.plazmamc.org/v1/badge/{color}/{name}/{content}"

@app.get("/percent/{percent:int}", status_code = 308)
async def percent(percent: int):
    return f"https://api.plazmamc.org/v1/badge/percent/{percent}"

@app.get("/internal/{content:str}", status_code = 308)
async def internal(percent: int):
    return f"https://api.plazmamc.org/internal/badges/{percent}"
