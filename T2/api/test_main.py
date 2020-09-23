from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)

#---Testes Unitários---#
def test_read_main_returns_not_found():
    response=client.get('/')
    assert response.status_code==404
    assert response.json()=={'detail':'Not Found'}

def test_read_no_task():
    response=client.get('/task/')
    assert response.status_code==200
    assert response.json()=={}

def test_create_alter_and_verify_true_false_task_returns_ok():
    response=client.post('/task/create',json={})
    assert response.status_code==200
    response2=client.post('/task/create',json={})
    assert response2.status_code==200
    response_alter = client.patch(
        '/task/alter/'+response.json(),
        json=
        {
        "description": "no description",
        "completed": True
        })
    assert response_alter.status_code==200
    assert response_alter.json()==None
    response_get_true = client.get('/task/?completed=true')
    response_get_false = client.get('/task/?completed=false')
    assert response_get_true.status_code==200
    assert response_get_false.status_code==200
    assert response_get_true.json()=={response.json():{
        "description": "no description",
        "completed": True
        }}
    assert response_get_false.json()=={response2.json():{
        "description": "no description",
        "completed": False
        }}

def test_create_and_get_task_returns_ok():
    response=client.post('/task/create',json={})
    assert response.status_code==200
    response_get = client.get(
        '/task/'+response.json())
    assert response_get.status_code==200
    assert response_get.json()=={"description": "no description","completed": False}

def test_create_and_replace_task_returns_ok():
    response=client.post('/task/create',json={})
    assert response.status_code==200
    response_replace = client.put(
        '/task/replace/'+response.json(),
        json=
        {
        "description": "Jogar Valorante",
        "completed": True
        })
    assert response_replace.status_code==200
    assert response_replace.json()==None

def test_create_and_delete_task_returns_ok():
    response=client.post('/task/create',json={})
    assert response.status_code==200
    response_delete = client.delete(
        '/task/delete/'+response.json())
    assert response_delete.status_code==200
    assert response_delete.json()==None

def test_get_task_returns_not_found():
    _uuid = str(uuid.uuid4())
    response=client.get('/task/' + _uuid)
    assert response.status_code==404
    assert response.json()=={"detail": "Task not found"}

def test_put_task_returns_not_found():
    _uuid = str(uuid.uuid4())
    response=client.put('/task/replace/' + _uuid)
    assert response.status_code==422
    assert response.json()=={'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_patch_task_returns_not_found():
    _uuid = str(uuid.uuid4())
    response=client.patch('/task/alter/' + _uuid)
    assert response.status_code==422
    assert response.json()=={'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_delete_task_returns_not_found():
    _uuid = str(uuid.uuid4())
    response=client.delete('/task/delete/' + _uuid)
    assert response.status_code==404
