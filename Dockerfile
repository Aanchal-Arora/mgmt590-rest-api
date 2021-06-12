FROM tensorflow/tensorflow

FROM pytorch/pytorch

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN pip install google-cloud-storage

COPY answer.py answer.py

CMD ["python", "answer.py"]

