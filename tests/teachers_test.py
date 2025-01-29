import pytest
from core import db
from core.models.assignments import Assignment

#in order to make sure test cases like grade test work at every test case
@pytest.fixture
def next_available_id():
    max_id = db.session.query(db.func.max(Assignment.id)).scalar()
    return max_id if max_id is not None else 1

def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

#grading assignemnt test case
def test_grade_assignment(client, h_teacher_1, next_available_id):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            'id': next_available_id,
            'grade': 'A'
        }
    )

    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == 'A'
    assert data['state'] == 'GRADED'


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment_nonexistent_assignment(client, h_teacher_1):
    """
    failure case: grading an assignment that doesn't exist
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 999,  # Assuming assignment with id 999 does not exist, should get this checked
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_grade(client, h_teacher_1):
    """
    failure case: grading an assignment with an invalid grade
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,  # Assuming assignment with id 1 is in submitted state, could be source of error baaki jaga bhi
            "grade": "Z"  # Invalid grade
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'
