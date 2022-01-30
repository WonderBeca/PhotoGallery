FROM python:3.7

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./src /app

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

ENV AWS_ACCESS_KEY_ID='AKIAZOS7CG6XSDOH3G5F'
ENV AWS_SECRET_ACCESS_KEY='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'
ENV MONGO_URI='mongodb+srv://rebecaaaaa:TPUGSnMYEbHfzhN3@cluster0.ojots.mongodb.net'

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]