import json
import random
import time
import aioredis
from aiohttp import web
from aiohttp_session import setup, get_session, redis_storage




from util import get_sum

app = web.Application()
routes = web.RouteTableDef()




@routes.post('/api/v1/set/')
async def set_array(request):
    data = await request.post()
    input_file = data['file'].file
    content = input_file.read()
    num = await get_sum(json.loads(content)['array'])
    return web.json_response(data={"ID": random.randint(0, 10000), "Sum": num})


@routes.post('/api/v1/sum/')
async def get_sum_by_id(request):
    data = await request.post()
    input_file = data['file'].file
    content = input_file.read()
    num = await get_sum(json.loads(content)['array'])
    return web.json_response(data={"Sum": num})


@routes.get('/api/v1/visit/')
async def handler(request):
    session = await get_session(request)

    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.time()

    text = 'Last visited: {}'.format(last_visit)

    response = web.Response(text=text)

    return response


async def make_app():
    app = web.Application()

    redis = await aioredis.create_pool(('localhost', 6379))
    storage = redis_storage.RedisStorage(redis)
    setup(app, storage)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(make_app(), port=9000)
