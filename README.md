# mgmt590-rest-api
example rest api
#API

##Routes
The 5 routes provide multiple functionalities and they are as follows:

1) GET /models
2) PUT /models
3) DELETE /models?model=<model name>
4) POST /answer?model=<model name>
5) GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
 
## General Information about API
The API is a Question and Answer API which uses a context to answer a particular question. It gets the current models and the answers provided by those models with the timestamp. It also has the option of choosing one of the three model to get an answer for the question.

The first route gets the name of the models that are currently available. 
  
Route: 
  ```
  GET /models
  ```

The second route  
Second route is used to enter a new model in the available lists of model. When the API receives the PUT request to the handler, the model name is extracted from the request and that particular model is made available to use hence. 
  
Route: 
  ```
  PUT /models
  ```
```
JSON Body: {
"name": "bert-tiny",
"tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
"model": "mrm8488/bert-tiny-5-finetuned-squadv2"
}
```

  
The third route deletes a model from the table. It extracts the model name from the DELETE request and deletes that particular model.
 
Route: 
  ```
  DELETE /models?model=<model name>
  ```

  
The fourth route answers the questions on the basis of the context. It use a POST request and extracts the Question and context from the body of request. Any of the available models can be chosen. In the current case, the API will use the same model to answer the question. The default model, i.e, distilled-bert is used if no model name is mentioned. When the answer is predicted and returned to the client, the question, context, answer , name of the model used and time stamp is noted to maintain the record of. 

Route: 
  ```
  POST /answer?model=<model name>
  ```
```
JSON BODY:
  {
"question": "who did holly matthews play in waterloo rd?",
"context": "She attended the British drama school East 15 in 2005,
and left after winning a high-profile role in the BBC drama Waterloo
Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
Matthews has continued to act in BBC's Doctors, playing Connie
Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
}
 ```

The fifth route provides the history of the questions answered. A specific model can be selected and the name and details of its activity, i.e., the question, context, answer and timestamp is displayed. The start and end time is selected and the API returns the records in that window. If the model name is not entered in the request,the record for all the models are returned. Similarly, if the timeframe is not provided, the API returms all the instances where any of the models were used to answer a question. 


Route:
  ```
  GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>
  ```

  
## Where the API can be located (the base URL): 
 ```
https://aanchal-ktospphdaa-uc.a.run.app
 ```
Dependencies: 

 transformers==4.6.1

 flask==1.1.2

 torch==1.8.1
  
## How to build and run the API locally via Docker or Flask
The app runs locally through the localhost link on port 8080 and is accessed through Postman. All routes work in Postman. For details check Flask documentation. https://flask.palletsprojects.com/en/1.0.x/api/

## Launching the API
The API is launched using Flask. The address of the host is important before launching the API and The API can be hosted in the local machine and also using online services.

## Making the Handlers
Each handler has a route where the request arrives and the handler gets invoked. Handlers essentially facilitate the API. 
Another component is the function that starts once the handler gets invoked. Therefore a decorator is used to assign a route to the handler. The code is then written to write the function which starts after the handler receives the request.
