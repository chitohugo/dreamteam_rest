# coding=utf-8
from flask import request, g, jsonify
from instance.database import db, Employee, Department, Role, employees_schema, employee_schema, employee_assign_schema
from sqlalchemy.exc import IntegrityError, ProgrammingError
from common.validations import get_object_or_404, get_department, get_role


class ModelEmployee(object):
    def list(self):
        response = Employee.query.all()
        data = employees_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 200})

    def listEmployee(self, id):
        instance = Employee
        response = get_object_or_404(instance, id)
        if response is not None:
            data = employee_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def assignEmployee(self, req):
        instance = Employee
        instanceD = Department
        instanceR = Role
        department = get_department(instanceD, req['department_id'])
        role = get_role(instanceR, req['role_id'])
        response = get_object_or_404(instance, req['id'])
        if response and department and role is not None:
            response.department_id = req['department_id']
            response.role_id = req['role_id']
            db.session.commit()
            data = employee_assign_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def insert(self, req):
        try:
            response = Employee(email=req['email'], first_name=req['first_name'],
                                last_name=req['last_name'], username=req['username'], password=req['password'])
            db.session.add(response)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'errors': 'The username o email: Exist. Please check it!', 'status': 500, 'data': '{}'})
        except ProgrammingError:
            return jsonify({'errors': 'The email is not valid. Please check it', 'status': 500, 'data': '{}'})
        data = employee_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 201})

    def update(self, req):
        instance = Employee
        response = get_object_or_404(instance, req['id'])
        if response is not None:
            response.email = req['email']
            response.username = req['username']
            response.first_name = req['first_name']
            response.last_name = req['last_name']
            response.department_id = req['department_id']
            response.role_id = req['role_id']
            response.password = req['password']
            response.is_admin = req['is_admin']
            db.session.commit()
            data = employee_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def delete(self, id):
        instance = Employee
        response = get_object_or_404(instance, id)
        if response is not None:
            db.session.delete(response)
            db.session.commit()
            data = employee_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})
