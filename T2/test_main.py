from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
uuid_  = ""

#---Testes Unitários---#
def test_read_main_returns_not_found():
    response=client.get('/')
    assert response.status_code==404
    assert response.json()=={'detail':'Not Found'}

def test_read_task_returns_not_found():
    response=client.get('/task')
    assert response.status_code==200
    assert response.json()=={}

def test_create_task_returns_ok():
    response=client.post('/task',json={})
    assert response.status_code==200

def test_get_task_returns_not_found():
    response=client.get('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert response.status_code==404
    assert response.json()=={"detail": "Task not found"}

def test_get_task_returns_ok():
    response=client.get('/task/')
    assert response.status_code==200

def test_put_task_returns_not_found():
    response=client.put('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert response.status_code==422
    assert response.json()=={'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_put_task_returns_ok():
    response=client.put('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6',json={})
    assert response.status_code==200

def test_patch_task_returns_not_found():
    response=client.patch('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert response.status_code==422
    assert response.json()=={'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_patch_task_returns_ok():
    response=client.patch('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6',json={})
    assert response.status_code==200

def test_delete_task_returns_not_found():
    response=client.delete('/task/')
    assert response.status_code==307

def test_delete_task_returns_ok():
    response=client.delete('/task/3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert response.status_code==200



# def test_all_tarefas_ok():
#     response=client.post('/tarefas/')
#     assert response.status_code==200
#     assert response.json()=={"nome": "Estudar","descricao": "Fazer o H1 de Cloud","concluida": False}