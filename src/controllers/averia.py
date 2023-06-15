from flask import Flask
from flask_restx import Resource, Namespace
from src.server.instance import server

app = server.app
api = server.api

ns_averia = Namespace('Averia', path='/api/1.0/averia', description='Crea y consulta averias')


@ns_averia('/crear')
class crear(Resource):
    def post():
        return 
