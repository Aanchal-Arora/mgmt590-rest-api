import sqlite3
import os
import time
from sqlite3 import Error
from flask import Flask, app
from flask import jsonify, request
from transformers.pipelines import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
from transformers import __version__
print(__version__)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("pythonsqlite.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


conn = sqlite3.connect("pythonsqlite.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS models;")
conn.commit()

create_table = "CREATE TABLE models (name char(50), tokenizer char(50), model char(50));"
c.execute(create_table)

insert_table = "INSERT INTO models VALUES ('distilled-bert','distilbert-base-uncased-distilled-squad','distilbert-base-uncased-distilled-squad'), ('deepset-roberta','deepset/roberta-base-squad2','deepset/roberta-base-squad2');"
c.execute(insert_table)
conn.commit()
conn.close()

app = Flask(__name__)


@app.route("/models", methods=["GET", "PUT", "DELETE"])
def models():
    if request.method == "GET":
        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()
        c.execute("SELECT * FROM models")
        model = c.fetchall()
        listmodels = []

        for i in model:
            output = {"name": i[0], "tokenizer": i[1], "model": i[2]}
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

    elif request.method == "PUT":
        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()

        insert_put = request.json
        name = insert_put["name"]
        tokenizer = insert_put["tokenizer"]
        model = insert_put["model"]

        c.execute("INSERT INTO models VALUES (?, ?, ?)", (name, tokenizer, model))
        conn.commit()
        c.execute("SELECT * FROM models")
        model_all = c.fetchall()
        listmodels = []

        for i in model_all:
            output = {"name": i[0], "tokenizer": i[1], "model": i[2]}
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)

    elif request.method == "DELETE":
        modelname = request.args.get("model")

        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()
        c.execute("DELETE FROM models WHERE name = ?", (modelname,))
        conn.commit()
        c.execute("SELECT * FROM models")
        model_all = c.fetchall()
        listmodels = []

        for i in model_all:
            output = {"name": i[0], "tokenizer": i[1], "model": i[2]}
            listmodels.append(output)
        conn.close()
        return jsonify(listmodels)


conn = sqlite3.connect("pythonsqlite.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS answer;")
conn.commit()

create_table = "CREATE TABLE if not exists answer (timestamp INTEGER, answer varchar(100), question varchar(100), context varchar(1000), model TEXT);"
c.execute(create_table)

conn.commit()
conn.close()


@app.route("/answer", methods=["POST", "GET"])
def answer():
    if request.method == "POST":
        conn = sqlite3.connect("pythonsqlite.db")
        c = conn.cursor()

        model_name = request.args.get('model', default = "distilled-bert")
        c.execute("SELECT * from models WHERE name = ?", (model_name,))
        models_table = c.fetchall()
        print(models_table)
        temp = models_table[0]
        print(temp)
        name = temp[0]
        print(name)
        token = temp[1]
        print(token)
        model = temp[2]
        print(model)
        data = request.json

        ts = int(time.time())
        # Import model
        hg_comp = pipeline('question-answering', model=model, tokenizer=token)
        # Answer the answer
        answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']
        # Create the response body.

        c.execute("INSERT INTO answer VALUES (?, ?, ?, ?, ?)", (ts, answer, data['question'], data['context'], model_name))
        conn.commit()

        out = {
            "model": model_name,
            "timestamp": ts,
            "question": data['question'],
            "context": data['context'],
            "answer": answer
        }
        return jsonify(out)

    elif request.method == "GET":
        conn = sqlite3.connect("pythonsqlite.db")
        cursor = conn.cursor()

        modelname = request.args.get("model", default=None)
        start = request.args.get("start")
        end = request.args.get("end")

        if modelname is not None:

            cursor.execute("SELECT * FROM answer where model='"+modelname +"' and timestamp between ? and ?",[start,end])
            conn.commit()
            model = cursor.fetchall()
            listmodels = []

            for i in model:
                output = {
                    "timestamp": i[0],
                    "modelname": i[4],
                    "answer": i[1],
                    "question": i[2],
                    "context": i[3],
                }
                listmodels.append(output)
        else:
            cursor.execute("SELECT * FROM answer where timestamp between ? and ?", (start, end))
            conn.commit()
            model = cursor.fetchall()
            listmodels = []

            for i in model:
                output = {
                    "timestamp": i[0],
                    "modelname": i[4],
                    "answer": i[1],
                    "question": i[2],
                    "context": i[3],
                }
                listmodels.append(output)

            conn.close()
        return jsonify(listmodels)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True)
