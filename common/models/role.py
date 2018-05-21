# coding=utf-8
from flask import request, g, jsonify
from instance.database import Role
from instance.database import db, role_schema, roles_schema
from common.validations import get_role


class ModelRole(object):
    def list(self):
        response = Role.query.all()
        data = roles_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 200})

    def listRole(self, id):
        instance = Role
        response = get_role(instance, id)
        if response is not None:
            data = role_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def insert(self, req):
        response = Role(name=req['name'], description=req['description'])
        db.session.add(response)
        db.session.commit()
        data = role_schema.dump(response).data
        return jsonify({'data': data, 'errors': {}, 'status': 201})

    def update(self, req):
        instance = Role
        response = get_role(instance, req['id'])
        if response is not None:
            response.description = req['description']
            response.name = req['name']
            db.session.commit()
            data = role_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})

    def delete(self, id):
        instance = Role
        response = get_role(instance, id)
        if response is not None:
            db.session.delete(response)
            db.session.commit()
            data = role_schema.dump(response).data
            return jsonify({'data': data, 'errors': {}, 'status': 200})
        return jsonify({'data': '{}', 'errors': 'Not found', 'status': 404})
