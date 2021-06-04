# mgmt590-lec1

## Functionalities of The Code

We have created several routes for the question-answer code. These are -
GET /moodels
PUT /models
DELETE /models?model=<model name>
POST /answer?model=<model name>
GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
 

## General Information about API
The API used is a Question-Answering API which generates answers for the questions from the given context. 
We have created multiple models and have added the functionality to add or delete models. We can choose any model which has been added in the database to answer the questions

Of the several routes created, the first one (GET /models) helps us to get the list of all the available models
Route:   
  GET /models
  
Response:
  [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    }
  ]


The second route is used to add a new model to our existing database of models. The model details(model, model-name, tokenixer) of the model is extracted from request.json (Body)  
Route: 
  PUT /models
  
Body (request.json):
  {
    "name": "bert-tiny",
    "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
    "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
  }

Response:
  [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    },
    {
        "model": "mrm8488/bert-tiny-5-finetuned-squadv2",
        "name": "bert-tiny",
        "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2"
    }
  ]

  
The third route is to delete models from our dataset. The model name which is to be deleted is extracted from the DELETE request and deletes it from the database
Route:   
  DELETE /models?model=<model name>
  Example: DELETE /models?model=tiny-bert
  
Response:
  After selecting tiny-bert, the model will be deleted from the database  
  [
    {
        "model": "distilbert-base-uncased-distilled-squad",
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad"
    },
    {
        "model": "deepset/roberta-base-squad2",
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2"
    }
  ]
  

The fourth route is to answer the questions based on the context provided for the particular question. The post request is used to extract the Question and Context from the body (request.json)
We have provided an option for the user to choose any model to answer the particular question. The model will be fetched from our database of models.
By default, we have selected distilled-bert to answer the questions. The API uses the default model if no model is passed in the syntax.
Additionally, a time-stamp is also added to maintain the record of all the questions answered in a new database which can be later fetched

Route:   
  POST /answer?model=<model name>
  Example: POST/answer
  Example: POST/answer?model=deepset-roberta

Body (request.json):
  {
    "question": "who did holly matthews play in waterloo rd?",
    "context": "She attended the British drama school East 15 in 2005,
    and left after winning a high-profile role in the BBC drama Waterloo
    Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
    Matthews has continued to act in BBC's Doctors, playing Connie
    Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
    she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
  }
 
Response:
  {
    "answer": "Leigh-Ann Galloway",
    "context": "She attended the British drama school East 15 in 2005, and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack.",
    "model": "distilled-bert",
    "question": "who did holly matthews play in waterloo rd?",
    "timestamp": 1622161059
  }


The fifth functionality is to fetch the entire database of the questions answered so far.
It provides an option to select a specific model and know the details of its activity. In this case the name of model is extracted and activity of that model is returned. That is the question , context and answer along with time stamp of answering is returned. There is also option to select time frame . the start and the end time frame if selected, the API returns the records between that provided window. If there is no start and end time , API returns the records of all the instance wher a model was used to answetr a qyestion.In same way if the model name is not provided in request, the record for all models are returned.

Route:
  
  GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
  

  
## Where the API can be located (the base URL): 
 
 https://answer-api-jlzk3jod5q-uc.a.run.app
 

  
## How to build and run the API locally via Docker or Flask
The app will locally run thorugh localhost link on port 8080 and can be accessed through postman.All the routes will work as it is there.
  
## Launching the API
Launching part can easily be done by Flask. We have to import flask then there is code which is mentioned with comments in our code. One very crucial thing that happens during launching is to decide the address of host. We can also host the API in our own local machine. We can also use multiple online service to host.

## Making the Handlers
Actually Handlers are the part which facilitates in achieving the goals in API. Every handler has a route or path where request comes and thus handler gets invoke. the second part of Handler is fuction that starts executing once handler gets invoked. So we use a decorator to assign a route to handler. Then we write code to form the fuction wwhich will start once handler receives any request. Here is an illustration:
