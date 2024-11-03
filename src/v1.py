from fastapi import *
from fastapi.responses import RedirectResponse
from .versions import *

def version_1(app: FastAPI):

    router = APIRouter(
        prefix = "/v1",
        tags = ["v1"],
        responses = { 404: {"description": "Not found"} }
    )

    @router.get("/git", status_code = 308)
    @router.get("/git/{version:str}", status_code = 308)
    @router.get("/git/{branch:str}/{target:str}", status_code = 308)
    async def git(version: str = head, branch: str = None, target: str = None):
        if version not in versions:
            return { 404: {"description": "Invalid version"} }

        if (branch != None and target != None):
            return RedirectResponse(f"https://github.com/PlazmaMC/Plazma/tree/{branch}/{target}")

        return RedirectResponse(f"https://github.com/PlazmaMC/Plazma/tree/{versions[version]}/{version}")

    @router.get("/build", status_code = 308)
    @router.get("/build/{version:str}", status_code = 308)
    async def build(version: str = head):
        if version not in versions:
            return { 404: {"description": "Invalid version"} }

        return RedirectResponse(f"https://img.shields.io/github/actions/workflow/status/PlazmaMC/Plazma/release.yml?style=for-the-badge&label=%20&branch={versions[version]}/{version}")

    def badge():
        colors = ["gray", "blue", "success", "aqua", "red", "purple", "yellow", "white"]

        @router.get("/badge/{color:int}/{content:str}", status_code = 308)
        @router.get("/badge/{color:int}/{name:str}/{content:str}", status_code = 308)
        @router.get("/badge/{color:int}/{name:str}/{content:str}/{logo:str}", status_code = 308)
        async def badge(color: int, content: str, name: str = "", logo: str = ""):
            if len(colors) < color:
                return { 404: {"description": "Invalid color code"} }

            return RedirectResponse(f"https://img.shields.io/badge/{name}-{content}-{colors[color]}?style=for-the-badge&logo={logo}")
    badge()

    @router.get("/badge/percent/{percent:int}", status_code = 308)
    async def percent(percent: int):
        color = "gray"
        if percent == 100:
            color = "success"
        elif percent >= 75:
            color = "yellow"
        elif percent >= 50:
            color = "orange"
        elif percent >= 25:
            color = "red"
        elif percent >= 0:
            color = "maroon"

        return RedirectResponse(f"https://img.shields.io/badge/-{percent}%25-{color}?style=for-the-badge")

    def download():
        types = [
            ["paperclip", "mojmap" ],  # 00
            ["paperclip", "reobf"],  # 01
            ["bundler"  , "mojmap" ],  # 10
            ["bundler"  , "reobf"]   # 11
        ]

        @router.get("/download", status_code = 308)
        @router.get("/download/{version:str}", status_code = 308)
        async def download(version: str = head, target: int = 0):
            if target == None:
                target = 0

            if len(types) < target:
                return { 404: {"description": "Invalid target type"} }

            return RedirectResponse(f"https://github.com/PlazmaMC/Plazma/releases/download/build/{version}/latest/plazma-{types[target][0]}-{version}-R0.1-SNAPSHOT-{types[target][1]}.jar")
    download()

    app.include_router(router)
