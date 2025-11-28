import os
import json
import logging
from flask import request
from flask_accepts import accepts
from flask_restx import Namespace, Resource
from kafka import KafkaProducer
from app.schemas import LocationSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-api")

api = Namespace("UdaConnect", description="Connections via geolocation.")

KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self):
        """
        Accepts location data and publishes it to Kafka.
        """
        json_data = request.get_json()
        logger.info(f"Received location data: {json_data}")
        
        producer.send('location_topic', value=json_data)
        
        return {"message": "Location accepted"}, 202
