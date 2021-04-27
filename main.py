from fastapi import FastAPI, Response, status
from typing import List
from user_data.schemas_counting import ShowCounting, Counting
from user_data.database_connection import doc_collection
from google.cloud import firestore
import logging


# Instance Creation of the app
app = FastAPI()


@app.post('/update/', status_code=status.HTTP_202_ACCEPTED,
          response_model=ShowCounting)
async def update_or_create(input: Counting, response: Response):
    """ This Method Either creates the New Document for name or
            update the value if name already exists in docuemnts """
    logging.INFO("Inside main --update_or_create")
    dict_data = {'name': input.name, 'value': input.value}
    doc_ref = doc_collection.document(input.name)
    record = doc_ref.get()
    if record.exists:
        doc_ref.update({u'value': firestore.Increment(input.value)})
    else:
        doc_ref.set(dict_data)
        response.status_code = status.HTTP_201_CREATED
    # to send the latest response
    record = doc_ref.get()
    return record.to_dict()


@app.get('/allposts/', status_code=status.HTTP_200_OK,
         response_model=List[ShowCounting])
def showAlldata():
    logging.INFO("Inside main --showAlldata")
    all_docs = doc_collection.stream()
    results = []
    for doc in all_docs:
        results.append(doc.to_dict())
    return results
