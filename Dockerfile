FROM elilillyco-lilly-docker.jfrog.io/python:3.10

WORKDIR /app

COPY . ./
RUN pip3 install -r ./requirements.txt
RUN make proto

ENV GRPC_TRACE=ALL
ENV GRPC_VERBOSITY=DEBUG

CMD [ "python3", "/app/server.py" ]
