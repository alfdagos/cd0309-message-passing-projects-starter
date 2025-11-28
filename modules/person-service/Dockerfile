FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install grpcio-tools

COPY . .

RUN python3 -m grpc_tools.protoc -I app/protos --python_out=app/ --grpc_python_out=app/ app/protos/person.proto

EXPOSE 5001

CMD ["python", "app/main.py"]
