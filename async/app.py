from aiohttp import web
from datetime import datetime
import asyncio
import random

app = web.Application()
routes = web.RouteTableDef()


@routes.get('/')
async def handle(request):
    print('get')
    name = request.match_info.get('name', "Anonymous")
    text = "GET REQUEST, " + name

    return web.json_response(data={"text": 'OK Sended'})


@routes.post('/sum/')
async def get_sum(request):
    print('post')
    data = await request.post()
    print(data)

    filename = data['file'].filename
    input_file = data['file'].file
    print(filename)
    # print(data['text'])
    content = input_file.read()
    print(input_file)
    print(content)
    return web.json_response(data={"Answer": True})


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=9000)
