from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({"hello": "world"})

async def otherpage(request):
    return JSONResponse({"other": "page"})


app = Starlette(debug=True, routes=[
    Route("/", homepage),
    Route("/other", otherpage),
    ])
