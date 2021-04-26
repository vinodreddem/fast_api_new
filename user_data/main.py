from fastapi import FastAPI, Response, status
from typing import List
# from .schemas_counting import Counting, ShowCounting
from . import schemas_counting
from .database_connection import db, doc_collection
from google.cloud import firestore


#Instance Creation of the app
app = FastAPI()


@app.post('/update/',status_code = status.HTTP_202_ACCEPTED, response_model = schemas_counting.ShowCounting)
async def update_or_create(input : schemas_counting.Counting, response :Response):
    """ This Method Either creates the New Document for name or update the value if name already exists in docuemnts """
    dict_data = {'name':input.name, 'value':input.value }
    doc_ref = doc_collection.document(input.name)
    record = doc_ref.get()
    print (record.get(u'value'))   
    if record.exists:
        doc_ref.update({u'value':firestore.Increment(input.value)})
    else:     
        doc_ref.set(dict_data)
        response.status_code = status.HTTP_201_CREATED
    
    #to send the latest response 
    record = doc_ref.get()
    return record.to_dict()

@app.get('/allposts/',status_code=status.HTTP_200_OK, response_model = List[schemas_counting.ShowCounting])
def showAlldata():
    all_docs = doc_collection.stream()
    results = []
    for doc in all_docs:
        results.append(doc.to_dict())
    return results
