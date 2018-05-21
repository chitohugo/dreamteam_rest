# coding=utf-8
from common.models.department import ModelDepartment
from flask import request, jsonify
from flask_restful import Resource
from instance.database import Employee
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256

department = ModelDepartment()
auth = HTTPBasicAuth()
instance = Employee


class Department(Resource):
    @auth.login_required
    def get(self):
        response = department.list()
        return response

    @auth.login_required
    def post(self):
        req = request.get_json()
        response = department.insert(req)
        return response


class DepartamentDetail(Resource):
    @auth.login_required
    def get(self, id):
        if str.isdigit(str(id)):
            response = department.listDepartment(id)
            return response
        return jsonify(data={}, status=404, errors='Parámetro incorrecto, inténtelo de nuevo')

    @auth.login_required
    def put(self):
        req = request.get_json()
        if str.isdigit(str(req['id'])):
            response = department.update(req)
            return response
        return jsonify(data={}, status=400, errors='Parámetro incorrecto, inténtelo de nuevo')

    @auth.login_required
    def delete(self, id):
        if str.isdigit(str(id)):
            response = department.delete(id)
            return response
        return jsonify(data={}, status=400, errors='Parámetro incorrecto, inténtelo de nuevo')


@auth.verify_password
def verify_password(email, password):
    user = instance.query.filter_by(email=email).first()
    try:
        if user is not None and pbkdf2_sha256.verify(password, user.password_hash):
            return True
    except ValueError:
        return False
