# coding=utf-8
from flask import Flask, g
from flask_validator import ValidateInteger, ValidateString, ValidateEmail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost/dreamteam_rest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.SMALLINT, default=False, nullable=False)

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Employee.email, True, True, "The e-mail is not valid. Please check it")

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = pbkdf2_sha256.hash(password)

    # def verify(self, password):
    #     """
    #     Check if hashed password matches actual password
    #     """
    #     return pbkdf2_sha256.verify(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class EmployeeAssignSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'username', 'department_id', 'role_id')


class DepartmentSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'description')


class RoleSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'description')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
employee_assign_schema = EmployeeAssignSchema()

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
db.create_all()

# dep = Department('1', 'Informatica', 'TIC')
# db.session.add(dep)
# # db.session.add(Role('', 'Admin', 'Administrador'))
# db.session.commit()
