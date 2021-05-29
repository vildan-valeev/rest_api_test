import random

from sanic import Sanic
import json as jsn
from sanic_session import Session
from sanic.response import json
from sanic_session.memory import InMemorySessionInterface
from sanic_openapi import openapi2_blueprint, doc
from util import get_sum

app = Sanic(name='TEST_APP')
session = Session(app, interface=InMemorySessionInterface())
app.blueprint(openapi2_blueprint)


@app.route("/api/v1/set/", methods=['POST'])
@doc.consumes(doc.File(name="file"), location="formData", content_type="multipart/form-data")
@doc.description('Set  json file  with "Array" key in dict.')
async def set_array(request):
    # print(request.files)
    input_file = request.files.get('file')
    content = input_file.body
    result_num = await get_sum(jsn.loads(content)['array'])
    result_id = random.randint(0, 10000)
    request.ctx.session['ID'] = result_id
    request.ctx.session['SUM'] = result_num

    return json({"ID": result_id, "SUM": result_num})


@app.route("/api/v1/sum/", methods=['POST'])
@doc.consumes(doc.JsonBody(
        {
            "ID": doc.Integer(0000),
        }
    ),
    location="body",)
@doc.description('Getting result by ID')
async def get_sum_by_id(request):
    data = request.json
    # print(data['ID'])

    # print(request.ctx.session.sid)
    # print(session.interface.session_store)
    # print()
    # print(request.ctx.session.values())

    # -----  если есть уже расситанный в куках реквеста с совпадающим ID (повторное обращение за данными) ------
    print(data)
    print(request.ctx.session)
    if {'ID', 'SUM'}.issubset(request.ctx.session.keys()) and request.ctx.session['ID'] == data['ID']:
        resp = {'SUM': request.ctx.session['SUM']}
        return json(resp, status=200)

    print('RERE')
    # -----  если сессия реквеста не та или нету, но запрос по ID, то ищем sum в сохраненных session------
    for i in session.interface.session_store:
        # print(session.interface.session_store[i], type(session.interface.session_store[i]))
        dict_i = jsn.loads(session.interface.session_store[i])
        # print(dict_i, dict_i['ID'])

        if {'ID', 'SUM'}.issubset(dict_i.keys()) and data['ID'] == dict_i['ID']:
            resp = {'SUM': dict_i['SUM']}
            # print('BOOOOTT!!')
            return json(resp, status=200)

    return json({'Failure': 'ID not found. If you want to get SUM, send json file to ../api/v1/set/ endpoint'}, 404)


@app.get("/api/v1/visit/")
@doc.description('Click click ...)))')
async def index(request):
    if not request.ctx.session.get('foo'):
        request.ctx.session['foo'] = 0
    request.ctx.session['foo'] += 1
    print(request.ctx.session, request.ctx.session.sid)
    print(session.interface.session_store, type(session.interface.session_store), )
    return json({"foo": request.ctx.session['foo']})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000, debug=True)
