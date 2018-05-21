# coding=utf-8
from flask import Flask
from flask_restful import Resource, Api
from resources.employee import Employee, EmployeeDetail
from resources.department import Department, DepartamentDetail
from resources.role import Role, RoleDetail

# initialization

app = Flask(__name__)
api = Api(app)

# extensions


# Endpoint Employee
api.add_resource(Employee, '/employee', '/employee/')
api.add_resource(EmployeeDetail, '/employee', '/employee/<string:id>', '/employee/assign/')

# Endpoint Department
api.add_resource(Department, '/department', '/department/')
api.add_resource(DepartamentDetail, '/department', '/department/<string:id>')

# Endpoint Role
api.add_resource(Role, '/role', '/role/')
api.add_resource(RoleDetail, '/role', '/role/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
