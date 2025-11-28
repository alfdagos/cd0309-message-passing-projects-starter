import logging
import requests
import grpc
import app.person_pb2 as person_pb2
import app.person_pb2_grpc as person_pb2_grpc
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

# Env vars should be used here, but hardcoding for MVP simplicity as per k8s service names
PERSON_SERVICE_HOST = "person-service:5001"
CONNECTION_SERVICE_URL = "http://connection-service:5002"

class PersonService:
    @staticmethod
    def create(person: Dict) -> Dict:
        """
        Creates a new person via gRPC call to Person Service.
        """
        with grpc.insecure_channel(PERSON_SERVICE_HOST) as channel:
            stub = person_pb2_grpc.PersonServiceStub(channel)
            response = stub.Create(person_pb2.PersonMessage(
                first_name=person["first_name"],
                last_name=person["last_name"],
                company_name=person["company_name"]
            ))
            return {
                "id": response.id,
                "first_name": response.first_name,
                "last_name": response.last_name,
                "company_name": response.company_name
            }

    @staticmethod
    def retrieve(person_id: int) -> Dict:
        """
        Retrieves a person by ID via gRPC call to Person Service.
        """
        with grpc.insecure_channel(PERSON_SERVICE_HOST) as channel:
            stub = person_pb2_grpc.PersonServiceStub(channel)
            try:
                response = stub.Retrieve(person_pb2.PersonId(id=int(person_id)))
                return {
                    "id": response.id,
                    "first_name": response.first_name,
                    "last_name": response.last_name,
                    "company_name": response.company_name
                }
            except grpc.RpcError as e:
                logger.error(f"gRPC Error: {e}")
                return {}

    @staticmethod
    def retrieve_all() -> List[Dict]:
        """
        Retrieves all persons via gRPC call to Person Service.
        """
        with grpc.insecure_channel(PERSON_SERVICE_HOST) as channel:
            stub = person_pb2_grpc.PersonServiceStub(channel)
            response = stub.RetrieveAll(person_pb2.Empty())
            persons = []
            for p in response.persons:
                persons.append({
                    "id": p.id,
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "company_name": p.company_name
                })
            return persons

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date, end_date, meters=5) -> List[Dict]:
        """
        Retrieves connections via REST call to Connection Service.
        """
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "distance": meters
        }
        try:
            response = requests.get(f"{CONNECTION_SERVICE_URL}/persons/{person_id}/connection", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Connection Service Error: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error calling Connection Service: {e}")
            return []

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Dict:
        # For MVP, we might not implement this in Gateway if not used by Frontend
        return {}

    @staticmethod
    def create(location: Dict) -> Dict:
        # This should be handled by Location API directly from Mobile
        return {}
