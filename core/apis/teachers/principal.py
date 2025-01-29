#have to test this 
from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher

from .schema import TeacherSchema

# Create a Blueprint for principal-related routes
principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    # Fetch all teachers from the database
    teachers = Teacher.query.all()
    # Serialize the teacher data
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    # Return the serialized data in the API response
    return APIResponse.respond(data=teachers_dump)