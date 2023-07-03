from flask_restx import fields
from src.server.instance import server



in_telefono = server.api.model('Telefono', {
    'cod': fields.String(decription="Codigo de area", required=True, min_length=3, max_length=3),
    'tlf': fields.String(decription = ' Telefono sin el codigo de area', required=True, min_length=7, max_length=7)
    })




