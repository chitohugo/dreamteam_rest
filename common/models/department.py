# coding=utf-8
from flask import request, g, jsonify
from instance.database import Department
from instance.database import db, department_schema, departments_schema
from common.validations import get_department


class ModelDepartment(object):
    def list(self):
        response = Department.query.all()
        data = departments_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 200})

    def listDepartment(self, id):
        instance = Department
        response = get_department(instance, id)
        if response is not None:
            data = department_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def insert(self, req):
        response = Department(name=req['name'], description=req['description'])
        db.session.add(response)
        db.session.commit()
        data = department_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 201})

    def update(self, req):
        instance = Department
        response = get_department(instance, req['id'])
        if response is not None:
            response.description = req['description']
            response.name = req['name']
            db.session.commit()
            data = department_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def delete(self, id):
        instance = Department
        response = get_department(instance, id)
        if response is not None:
            db.session.delete(response)
            db.session.commit()
            data = department_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})
