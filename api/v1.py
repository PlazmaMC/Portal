from fastapi import *
from fastapi.responses import RedirectResponse
from versions import *

def version_1(app: FastAPI):

    router = APIRouter(
        prefix = "/v1",
        tags = ["v1"],
        responses = { 404: {"description": "Not found"} }
    )

    @router.get("/git", response_class = RedirectResponse, status_code = 308)
    @router.get("/git/{version:str}", response_class = RedirectResponse, status_code = 308)
    @router.get("/git/{branch:str}/{target:str}", response_class = RedirectResponse, status_code = 308)
    async def git(version: str = head, branch: str = None, target: str = None):
        if version not in versions:
            return { 404: {"description": "Invalid version"} }

        if (branch != None and target != None):
            return f"https://github.com/PlazmaMC/Plazma/tree/{branch}/{target}"

        return f"https://github.com/PlazmaMC/Plazma/tree/{versions[version]}/{version}"

    @router.get("/build", response_class = RedirectResponse, status_code = 308)
    @router.get("/build/{version:str}", response_class = RedirectResponse, status_code = 308)
    async def build(version: str = head):
        if version not in versions:
            return { 404: {"description": "Invalid version"} }

        return f"https://img.shields.io/github/actions/workflow/status/PlazmaMC/Plazma/release.yml?style=for-the-badge&#x26;label=%20&#x26;branch={versions[version]}/{version}"

    @router.get("/builds", response_class = RedirectResponse, status_code = 308)
    @router.get("/builds/{version:str}", response_class = RedirectResponse, status_code = 308)
    async def builds(version: str = head):
        if version not in versions:
            return { 404: {"description": "Invalid version"} }

        return f"https://img.shields.io/github/actions/workflow/status/PlazmaMC/Plazma/release.yml?style=for-the-badge&label=%20&branch={versions[version]}/{version}"

    def badges():
        colors = ["gray", "blue", "lime", "aqua", "red", "purple", "yellow", "white"]

        @router.get("/badges/{color:int}/{content:str}", response_class = RedirectResponse, status_code = 308)
        async def badges(color: int, content: str):
            if len(colors) < color:
                return { 404: {"description": "Invalid color code"} }

            return f"https://img.shields.io/badge/{content}-{colors[color]}?style=for-the-badge"
    badges()

    @router.get("/badge/percentage/{percent:int}", response_class = RedirectResponse, status_code = 308)
    async def percentage(percent: int):
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

        return f"https://img.shields.io/badge/-{percent}%25-{color}?style=for-the-badge"

    def download():
        types = [
            ["paperclip", "reobf" ],  # 00
            ["paperclip", "mojmap"],  # 01
            ["bundler"  , "reobf" ],  # 10
            ["bundler"  , "mojmap"]   # 11
        ]

        @router.get("/download", response_class = RedirectResponse, status_code = 308)
        @router.get("/download/{version:str}", response_class = RedirectResponse, status_code = 308)
        @router.get("/download/{version:str}/{target:int}", response_class = RedirectResponse, status_code = 308)
        async def download(version: str = head, target: int = 0):
            if target == None:
                target = 0

            if len(types) < target:
                return { 404: {"description": "Invalid target type"} }

            return f"https://github.com/PlazmaMC/Plazma/releases/download/build/{version}/latest/plazma-{types[target][0]}-{version}-R0.1-SNAPSHOT-{types[target][1]}.jar"
    download()

    app.include_router(router)
