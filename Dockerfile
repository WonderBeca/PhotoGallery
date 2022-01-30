FROM python:3.7

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./src /app

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

ENV AWS_ACCESS_KEY_ID=''
ENV AWS_SECRET_ACCESS_KEY=''
ENV MONGO_URI=''

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
