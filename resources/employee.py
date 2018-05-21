# coding=utf-8
from common.models.employee import ModelEmployee
from flask import request, g, jsonify
from flask_restful import Resource
from instance.database import employee_schema, employee_assign_schema, Employee
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256

employee = ModelEmployee()
instance = Employee

auth = HTTPBasicAuth()


class Employee(Resource):
    @auth.login_required
    def get(self):
        response = employee.list()
        return response

    def post(self):
        req = request.get_json()
        response = employee.insert(req)
        return response


class EmployeeDetail(Resource):
    @auth.login_required
    def get(self, id):
        if str.isdigit(str(id)):
            response = employee.listEmployee(id)
            print(response)
            return response
        return jsonify(data={}, status=404, errors='Parámetro incorrecto, inténtelo de nuevo')

    @auth.login_required
    def post(self):
        req = request.get_json()
        if str.isdigit(str(req['id'])):
            response = employee.assignEmployee(req)
            return response
        return jsonify(data={}, status=400, errors='Parámetro incorrecto, inténtelo de nuevo')

    @auth.login_required
    def put(self):
        req = request.get_json()
        if str.isdigit(str(req['id'])):
            response = employee.update(req)
            return response
        return jsonify(data={}, status=400, errors='Parámetro incorrecto, inténtelo de nuevo')

    @auth.login_required
    def delete(self, id):
        if str.isdigit(str(id)):
            response = employee.delete(id)
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
