import os
import json
import logging
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import ST_Point
from app.models import Location
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-consumer")

KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def consume():
    """
    Consumes location messages from Kafka and persists them to the database.
    """
    consumer = KafkaConsumer(
        'location_topic',
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='location_consumer_group'
    )

    logger.info("Starting Location Consumer...")

    for message in consumer:
        logger.info(f"Received message: {message.value}")
        data = message.value
        
        session = Session()
        try:
            new_location = Location(
                person_id=data['person_id'],
                creation_time=data['creation_time'],
                coordinate=ST_Point(float(data['latitude']), float(data['longitude']))
            )
            session.add(new_location)
            session.commit()
            logger.info("Location saved to DB")
        except Exception as e:
            logger.error(f"Error saving location: {e}")
            session.rollback()
        finally:
            session.close()

if __name__ == "__main__":
    consume()
