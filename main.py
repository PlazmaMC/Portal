from fastapi import *
from fastapi.responses import RedirectResponse

app = FastAPI(
    docs_url = None,
    redoc_url = None,
    default_response_class = responses.RedirectResponse
)

@app.get("/", status_code = 308)
@app.get("/{version:str}", status_code = 308)
async def main(version: str = None, redirect: bool = False):
    if redirect:
        return f"https://api.plazmamc.org/v1/git/{version}"

    return f"https://api.plazmamc.org/v1/build/{version}"
