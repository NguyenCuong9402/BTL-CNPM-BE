import json
import uuid
from operator import or_

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from sqlalchemy import func, asc, and_

from app.api.v1.test_type.test_type_validator import CreateTestType, UpdateTestType
from app.gateway import authorization_require
from app.models import TestType, db, TestCase
from app.utils import send_result, send_error, validate_request, get_timestamp_now
from app.validator import TestTypeSchema

api = Blueprint('test_type', __name__)


@api.route("/<project_id>", methods=["GET"])
@authorization_require()
def get_test_type(project_id):
    try:
        token = get_jwt_identity()
        cloud_id = token.get('cloudId')
        test_types_count = db.session.query(TestType).filter(
            or_(TestType.project_id == project_id, TestType.project_key == project_id),
            TestType.cloud_id == cloud_id).count()
        if test_types_count == 0:
            test_type = TestType(
                id=str(uuid.uuid4()),
                name=DEFAULT_DATA['name'],
                kind=DEFAULT_DATA['kind'],
                is_default=DEFAULT_DATA['is_default'],
                index=DEFAULT_DATA['index'],
                project_id=project_id,
                cloud_id=cloud_id,
                created_date=get_timestamp_now()

            )
            db.session.add(test_type)
        db.session.commit()
        test_types = db.session.query(TestType).filter(
            or_(TestType.project_id == project_id, TestType.project_key == project_id),
            TestType.cloud_id == cloud_id, TestType.name != DEFAULT_DATA['name']).order_by(asc(TestType.name)).all()
        test_type_manual = TestType.query.filter(TestType.project_id == project_id, TestType.cloud_id == cloud_id,
                                                 TestType.name == DEFAULT_DATA['name']).first()
        result1 = [TestTypeSchema().dump(test_type_manual)]
        result2 = TestTypeSchema(many=True).dump(test_types)
        data = result1 + result2
        return send_result(data=data, message="OK")
    except Exception as ex:
        db.session.rollback()
        return send_error(message="Something wrong!")


@api.route("/<project_id>", methods=["POST"])
@authorization_require()
def create_test_type(project_id):
    try:
        token = get_jwt_identity()
        cloud_id = token.get('cloudId')
        is_valid, data, body_request = validate_request(CreateTestType(), request)
        if not is_valid:
            return send_error(data=data, code=200, is_dynamic=True)

        # Check coincided name
        coincided = check_coincided_name(name=body_request.get('name'), cloud_id=cloud_id, project_id=project_id)
        if coincided is True:
            return send_error(code=200, data={"name": "Test Type Option already exists. Please try again"},
                              message='Invalid request', show=False, is_dynamic=True)

        test_type = TestType(
            id=str(uuid.uuid4()),
            name=body_request['name'],
            kind="Steps",
            is_default=False,
            project_id=project_id,
            cloud_id=cloud_id,
            created_date=get_timestamp_now()
        )
        db.session.add(test_type)
        db.session.commit()
        return send_result(data=TestTypeSchema().dump(test_type), message="Test Type created", show=True)
    except Exception as ex:
        db.session.rollback()
        return send_error(message="Something wrong!", code=200, show=False)


@api.route("/<project_id>/<test_type_id>", methods=["DELETE"])
@authorization_require()
def delete(project_id, test_type_id):
    try:
        token = get_jwt_identity()
        cloud_id = token.get("cloudId")
        test_type = TestType.get_by_id(test_type_id)
        if test_type is None:
            return send_error(
                message="Test Type has been changed \n Please refresh the page to view the changes",
                code=200,
                show=False)
        test_type_name = test_type.name
        if test_type_name == DEFAULT_DATA['name']:
            return send_error(
                message="You can not delete the default test type \n Please refresh the page to view the changes",
                code=200,
                show=False)
        if test_type.is_default:
            reg = request.get_json()
            test_type_id_substitute = reg.get("test_type_id_substitute")
            test_type_substitute = TestType.get_by_id(test_type_id_substitute)
            if test_type_substitute is None:
                manual = TestType.query.filter(TestType.cloud_id == cloud_id, TestType.project_id == project_id,
                                               TestType.name == DEFAULT_DATA['name']).first()
                test_type.is_default = False
                manual.is_default = True
                db.session.flush()
                db.session.commit()
                return send_result(data="",
                                   message=f"Test Type {test_type_name} removed | Project Test Type settings saved",
                                   code=200, show=True)
            else:
                test_type.is_default = False
                test_type_substitute.is_default = True
                db.session.delete(test_type)
                db.session.flush()
        else:
            db.session.delete(test_type)
            db.session.flush()
        db.session.commit()
        return send_result(data="", message=f"Test Type {test_type_name} removed", code=200, show=True)
    except Exception as ex:
        db.session.rollback()
        return send_error(data='', message="Something was wrong!")


@api.route("/<project_id>/<test_type_id>", methods=["PUT"])
@authorization_require()
def update(project_id, test_type_id):
    try:
        token = get_jwt_identity()
        cloud_id = token.get('cloudId')
        test_type = TestType.get_by_id(test_type_id)
        if test_type is None:
            return send_error(
                message="Test Type has been changed \n Please refresh the page to view the changes",
                code=200,
                show=False)
        is_valid, data, body_request = validate_request(UpdateTestType(), request)
        if not is_valid:
            return send_error(data=data, code=200, is_dynamic=True)

        # Set other test type to no_default
        db.session.query(TestType).filter(
            or_(TestType.project_id == project_id, TestType.project_key == project_id),
            TestType.id != test_type_id,
            TestType.cloud_id == cloud_id).update({TestType.is_default: False})

        # Set this test type is default
        test_type.is_default = True
        db.session.commit()
        return send_result(data="", message="Project Test Type settings saved", code=200, show=True)
    except Exception as ex:
        db.session.rollback()
        return send_error(data='', message="Something was wrong!")


# @api.route("/tests/<project_id>", methods=["POST"])
# @authorization_require()
# def get_tests_by_test_type(project_id):
#     try:
#
#         return send_result(data=TestTypeSchema().dump(test_type), message="Test Type created", show=True)
#     except Exception as ex:
#         db.session.rollback()
#         return send_error(message="Something wrong!", code=200, show=False)


"""
Helper function
"""


def check_coincided_name(name='', self_id=None, project_id='', cloud_id=''):
    existed_test_step = TestType.query.filter(
        and_(TestType.name == name, TestType.id != self_id, TestType.cloud_id == cloud_id,
             TestType.project_id == project_id)).first()
    if existed_test_step is None:
        return False
    return True


DEFAULT_DATA = {
    "name": "Manual",
    "kind": "Steps",
    "is_default": True,
    "index": 0
}


def get_test_type_default(cloud_id: str, project_id: str):
    test_type = TestType.query.filter(TestType.cloud_id == cloud_id, project_id == project_id).count()
    if test_type == 0:
        test_type = TestType(
            id=str(uuid.uuid4()),
            name=DEFAULT_DATA['name'],
            kind=DEFAULT_DATA['kind'],
            is_default=DEFAULT_DATA['is_default'],
            index=DEFAULT_DATA['index'],
            project_id=project_id,
            cloud_id=cloud_id,
            created_date=get_timestamp_now()
        )
        db.session.add(test_type)
        db.session.flush()
    test_type_default = TestType.query.filter(TestType.cloud_id == cloud_id, project_id == project_id,
                                              TestType.is_default == 1).first()
    return test_type_default.id


@api.route("/<project_id>", methods=["PUT"])
@authorization_require()
def set_default_type_to_test(project_id):
    try:
        token = get_jwt_identity()
        cloud_id = token.get('cloudId')
        test_type_id = get_test_type_default(cloud_id, project_id)
        TestCase.query.filter(TestCase.project_id == project_id, TestCase.cloud_id == cloud_id,
                              TestCase.test_type_id.is_(None))\
            .update({"test_type_id": test_type_id})
        db.session.flush()
        db.session.commit()
        return send_result(message="oke")
    except Exception:
        db.session.rollback()
        return send_error(data='', message="Something was wrong!")