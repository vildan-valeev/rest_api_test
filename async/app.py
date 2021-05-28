import json

from aiohttp import web
from datetime import datetime
import asyncio
import random

from util import get_sum

app = web.Application()
routes = web.RouteTableDef()


@routes.post('/sum/')
async def sum(request):
    data = await request.post()
    input_file = data['file'].file
    content = input_file.read()
    num = await get_sum(json.loads(content)['array'])
    return web.json_response(data={"Sum": num})


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=9000)
