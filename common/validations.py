# coding=utf-8
from sqlalchemy.orm import exc


def get_object_or_404(instance, id):
    try:
        response = instance.query.filter_by(id=id).first()
        return response
    except (exc.NoResultFound, exc.MultipleResultsFound):
        raise


def get_department(instance, id):
    try:
        response = instance.query.filter_by(id=id).first()
        return response
    except (exc.NoResultFound, exc.MultipleResultsFound):
        raise


def get_role(instance, id):
    try:
        response = instance.query.filter_by(id=id).first()
        return response
    except (exc.NoResultFound, exc.MultipleResultsFound):
        raise
