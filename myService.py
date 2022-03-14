from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp
import os
import routes
from routes import middleware
import webob.exc
import webob.dec
import json
from os import walk
import logging
import mysql.connector

# 这下目录穿越了 :P

@wsgify
def error(req):
    dump = json.dumps({'result':'fail'})
    return Response(dump)

# curl -i -H "X_PROJECT_NAME: admin" -H "X_ROLES: admin" -d "dir=test2" http://127.0.0.1:7000/drive/admin/
@wsgify
def file_dir_create(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == params['project']:
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'admin' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    if 'webob._parsed_post_vars' in env:
        req_file = env['webob._parsed_post_vars'][0]['file']
        with open(f"drive/{params['project']}/{params['path']}{req_file.filename}",'wb') as f:
            f.write(req_file.file.read())
    else:
        req_dir = json.load(env['wsgi.input'])['dir']
        os.mkdir(f"drive/{params['project']}/{params['path']}{req_dir}")
    dump = json.dumps({'result':'success'})
    return Response(dump)

# curl -i -H "X_PROJECT_NAME: admin" -H "X_ROLES: reader" -X GET http://127.0.0.1:7000/drive/admin/flag.txt
@wsgify
def file_read(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == params['project']:
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'reader' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    with open(f"drive/{params['project']}/{params['path']}",'rb') as f:
        content = f.read()
    #dump = json.dumps({'result':content.decode('utf-8')})
    return Response(content)

# curl -i -H "X_PROJECT_NAME: admin" -H "X_ROLES: admin" -X DELETE http://127.0.0.1:7000/drive/admin/flag.txt
@wsgify
def file_delete(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == params['project']:
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'admin' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    try:
        os.remove(f"drive/{params['project']}/{params['path']}")
    except IOError:
        dump = json.dumps({'result':'fail'})
        return Response(dump)
    else:
        dump = json.dumps({'result':'success'})
        return Response(dump)

# curl -i -H "X_PROJECT_NAME: admin" -H "X_ROLES: reader" -X GET http://127.0.0.1:7000/drive/admin/
@wsgify
def dir_read(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == params['project']:
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'reader' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    resp_dir = []
    resp_file = []
    for (dirpath, dirnames, filenames) in walk(f"drive/{params['project']}/{params['path']}"):
        for i in dirnames:
            stat = os.stat(dirpath + i)
            resp_dir.append({'name':i, 'size':stat.st_size, 'time':stat.st_mtime})
        for i in filenames:
            stat = os.stat(dirpath + i)
            resp_file.append({'name':i, 'size':stat.st_size, 'time':stat.st_mtime})
        break
    resp = {'dir':resp_dir, 'file':resp_file}
    dump = json.dumps({'result':resp})
    return Response(dump)


# curl -i -H "X_PROJECT_NAME: admin" -H "X_ROLES: admin" -X DELETE http://127.0.0.1:7000/drive/admin/test/
@wsgify
def dir_delete(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == params['project']:
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'admin' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    try:
        os.rmdir(f"drive/{params['project']}/{params['path']}")
    except IOError:
        dump = json.dumps({'result':'fail'})
        return Response(dump)
    else:
        dump = json.dumps({'result':'success'})
        return Response(dump)

# curl -i -H "X_USER_NAME: admin" -X GET http://127.0.0.1:7000/drive/
@wsgify
def root_read(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    # Check Keystone Context
    if not env['HTTP_X_PROJECT_NAME'] == 'admin':
        return Response('WRONG HTTP_X_PROJECT_NAME', status=403)
    if not 'admin' in env['HTTP_X_ROLES']:
        return Response('WRONG HTTP_X_ROLES', status=403)
    resp_dir = []
    resp_file = []
    for (dirpath, dirnames, filenames) in walk(f"drive/"):
        for i in dirnames:
            stat = os.stat(dirpath + i)
            resp_dir.append({'name':i, 'size':stat.st_size, 'time':stat.st_mtime})
        for i in filenames:
            stat = os.stat(dirpath + i)
            resp_file.append({'name':i, 'size':stat.st_size, 'time':stat.st_mtime})
        break
    resp = {'dir':resp_dir, 'file':resp_file}
    dump = json.dumps({'result':resp})
    return Response(dump)

@wsgify
def info_create(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    info = json.load(env['wsgi.input'])['info']
    sql = f"INSERT into user (name, info) VALUES ('{env['HTTP_X_USER_NAME']}', '{info}')"
    cursor.execute(sql)
    sql = f"UPDATE user SET info = '{info}' WHERE name = '{env['HTTP_X_USER_NAME']}'"
    cursor.execute(sql)
    db.commit()
    dump = json.dumps({'result':'success'})
    return Response(dump)

@wsgify
def info_read(req):
    params = req.environ['wsgiorg.routing_args'][1]
    env = req.environ
    sql = f"SELECT info FROM user WHERE name = '{env['HTTP_X_USER_NAME']}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        dump = json.dumps({'result':result[0][0]})
    else:
        dump = json.dumps({'result':''})
    return Response(dump)

@wsgify
def dispatch(req):
    match = req.environ['wsgiorg.routing_args'][1]
    if not match:
        return webob.exc.HTTPNotFound()
    app = match['controller']
    return app

def app_factory(global_config, **local_config):
    mapper = routes.Mapper()
    # Frontend --> Auth --> FSAPI (CRUD)
    mapper.connect("/drive/{project}/{path:.*[^/]}", controller=error, conditions=dict(method=["POST"]))
    mapper.connect("/drive/{project}/{path:.*[^/]}", controller=file_read, conditions=dict(method=["GET"]))
    mapper.connect("/drive/{project}/{path:.*[^/]}", controller=file_delete, conditions=dict(method=["DELETE"]))
    mapper.connect("/drive/{project}/{path:.*}", controller=file_dir_create, conditions=dict(method=["POST"]))
    mapper.connect("/drive/{project}/{path:.*}", controller=dir_read, conditions=dict(method=["GET"]))
    mapper.connect("/drive/{project}/{path:.*}", controller=dir_delete, conditions=dict(method=["DELETE"]))
    mapper.connect("/drive/", controller=root_read, conditions=dict(method=["GET"]))
    # User Profile
    mapper.connect("/user", controller=info_create, conditions=dict(method=["POST"]))
    mapper.connect("/user", controller=info_read, conditions=dict(method=["GET"]))
    # mapper.connect("/user/{user}", controller=user_delete, conditions=dict(method=["DELETE"]))
    router = routes.middleware.RoutesMiddleware(dispatch, mapper)
    return router

logging.basicConfig(level=logging.NOTSET)

db = mysql.connector.connect(
  host="localhost",
  user="keystone",
  passwd="keystone",
  database="sibyl"
)
cursor = db.cursor()

here = os.path.abspath('.')
app = loadapp('config:config.ini', relative_to=here)
httpserver.serve(app, host='127.0.0.1', port=7000)
