from datetime import datetime
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self):
        payload = request.get_json()
        new_person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self):
        """
        Retrieves all persons.
        """
        persons = PersonService.retrieve_all()
        return persons

@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id):
        """
        Retrieves a single person by ID.
        """
        person = PersonService.retrieve(person_id)
        return person

@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id):
        """
        Retrieves connections for a person within a date range and distance.
        """
        start_date = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
