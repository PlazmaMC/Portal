from fastapi import *

app = FastAPI(
    docs_url = None,
    redoc_url = None,
    default_response_class = responses.RedirectResponse
)

@app.get("/")
@app.get("/{version:str}")
async def main(version: str = "", target: int = 0):
    if version == "":
        return "https://api.plazmamc.org/v1/download"
    return f"https://api.plazmamc.org/v1/download/{version}?target={target}"
