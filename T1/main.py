from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi  import FastAPI , HTTPException
from pydantic import BaseModel, Field
from typing   import List, Optional
import uuid


#---Models---#
class NomeBase(BaseModel):
    nome        :   str

class DescricaoBase(BaseModel):
    descricao   :   str

class ConcluidaBase(BaseModel):
    concluida   :   bool

class TarefaEntry(BaseModel):
    nome        :   str             = Field(..., example="Estudar")
    descricao   :   Optional[str]   = Field(..., example="Fazer o H1 de Cloud")
    concluida   :   bool            = Field(..., example=False)

app = FastAPI()

db  = {} 

#---Handler Error ---#
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# ---Todas as tarefas ---#
@app.get("/tarefas/")
def find_all_tarefas():
    return db

#---Todas as tarefas completed or not completed ---#
@app.get("/tarefas/{completed}")
def find_tarefas_completed_filter(completed: bool=None):
    if completed:
        db_completed={}
        for ID in db:
            if db[ID]["concluida"]:
                db_completed[ID]=db[ID]
        return db_completed

    elif not(completed):
        db_incompleted={}
        for ID in db:
            if not(db[ID]["concluida"]):
                db_incompleted[ID]=db[ID]
        return db_incompleted
    return {}

#---Criar tarefas ------#
@app.post("/tarefas")
def register_tarefa(tarefa: TarefaEntry):
    ID = str(uuid.uuid1())
    tarefa.concluida = False
    db[ID] = tarefa.dict()
    return db[ID]

#---Alterar tarefas NOME ---#
@app.patch("/tarefa/{tarefa_id}/nome", response_model=NomeBase)
def update_nome_tarefa(tarefa_id: str, tarefa: NomeBase):
    if tarefa_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        stored_tarefa = db[tarefa_id]   
        stored_tarefa_model = TarefaEntry(**stored_tarefa)
        update_data = tarefa.dict(exclude_unset=True)
        updated_tarefa = stored_tarefa_model.copy(update=update_data)
        db[tarefa_id] = updated_tarefa.dict()
        return updated_tarefa
    return {}

#---Alterar tarefas DESCRICAO ---#
@app.patch("/tarefa/{tarefa_id}/descricao", response_model=DescricaoBase)
def update_descricao_tarefa(tarefa_id: str, tarefa: DescricaoBase):
    if tarefa_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        stored_tarefa = db[tarefa_id]   
        stored_tarefa_model = TarefaEntry(**stored_tarefa)
        update_data = tarefa.dict(exclude_unset=True)
        updated_tarefa = stored_tarefa_model.copy(update=update_data)
        db[tarefa_id] = updated_tarefa.dict()
        return updated_tarefa
    return {}

#---Alterar tarefas STATUS ---#
@app.patch("/tarefa/{tarefa_id}/concluida", response_model=ConcluidaBase)
def update_concluida_tarefa(tarefa_id: str, tarefa: ConcluidaBase):
    if tarefa_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        stored_tarefa = db[tarefa_id]   
        stored_tarefa_model = TarefaEntry(**stored_tarefa)
        update_data = tarefa.dict(exclude_unset=True)
        updated_tarefa = stored_tarefa_model.copy(update=update_data)
        db[tarefa_id] = updated_tarefa.dict()
        return updated_tarefa
    return {}

#---Deletar tarefas ---#
@app.delete("/tarefa/{tarefa_id}")
def delete_tarefa(tarefa_id: str):
    if tarefa_id not in db:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        del db[tarefa_id]
    return {}

