from flask_restplus import Api
from .todo1 import users_api as ns1

api = Api(
    title='Task Management',
    version='1.0',
    description='A description of to do tasks',
    # All API metadatas
)

api.add_namespace(ns1)
