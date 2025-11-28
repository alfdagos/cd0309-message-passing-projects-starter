import logging
import time
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Person
from config import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-service")

# Setup Database
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class PersonService(person_pb2_grpc.PersonServiceServicer):
    def Create(self, request, context):
        """
        Creates a new person record in the database.
        """
        session = Session()
        try:
            new_person = Person(
                first_name=request.first_name,
                last_name=request.last_name,
                company_name=request.company_name
            )
            session.add(new_person)
            session.commit()
            
            return person_pb2.PersonMessage(
                id=new_person.id,
                first_name=new_person.first_name,
                last_name=new_person.last_name,
                company_name=new_person.company_name
            )
        except Exception as e:
            logger.error(f"Error creating person: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return person_pb2.PersonMessage()
        finally:
            session.close()

    def Retrieve(self, request, context):
        """
        Retrieves a person record by ID.
        """
        session = Session()
        try:
            person = session.query(Person).filter(Person.id == request.id).first()
            if person:
                return person_pb2.PersonMessage(
                    id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    company_name=person.company_name
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Person not found")
                return person_pb2.PersonMessage()
        finally:
            session.close()

    def RetrieveAll(self, request, context):
        """
        Retrieves all person records.
        """
        session = Session()
        try:
            persons = session.query(Person).all()
            person_list = []
            for person in persons:
                person_list.append(person_pb2.PersonMessage(
                    id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    company_name=person.company_name
                ))
            return person_pb2.PersonList(persons=person_list)
        finally:
            session.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonService(), server)
    server.add_insecure_port('[::]:5001')
    logger.info("Person Service started on port 5001")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    serve()
