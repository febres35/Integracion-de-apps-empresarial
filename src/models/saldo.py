from flask_restx import fields
from src.server.instance import server

child_outSaldo = server.api.model( 'data', {
    'Fvencimiento': fields.String(), 
    'saldoA': fields.String(), 
    'saldoV': fields.String(), 
    'Fcorte': fields.String()
})
out_Saldo = server.api.model('Saldo', {
    'producto': fields.String(),
    'data': fields.Nested(child_outSaldo)})
