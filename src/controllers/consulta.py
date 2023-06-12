from flask import Flask
from flask_restx import Resource, Namespace
from src.server.instance import server



app = server.app
api = server.api

from src.models.telefono import in_telefono, out_Saldo

ns_consulta = Namespace('Consultas', description='Consultas -> saldo | abonado | planes', path='/api/1.0/consulta')
#api.add_namespace(ns_consulta)




saldoSoap = [
    {'producto' : '2125516273', 
     'data':{'Fvencimiento': '20230615',
      'saldoA': 'Decimal(\'0.0\')',
      'saldoV': 'Decimal(\'0, 0\')',
      'Fcorte': '20230605'}
    },
    {'producto' : '2544567233',
     'data':{'Fvencimiento': '20230815',
      'saldoA': 'Decimal(\'50,0\')',
      'saldoV': 'Decimal(\'23,0\')',
      'Fcorte': '20230530',}
    },
    {'producto' : '3215151274',
     'data':{'Fvencimiento': '20230415',
      'saldoA': 'Decimal(\'0.0\')',
      'saldoV': 'Decimal(\'0, 0\')',
      'Fcorte': '20230330',}
    }
]

@ns_consulta.route('/saldo')
@ns_consulta.doc(param={'cod': 'codigo de Area', 'tlf':'numero de telefono(producto)'})
class Saldo(Resource):

    @ns_consulta.expect(in_telefono, valitade=True)
    @ns_consulta.marshal_with(out_Saldo)
    def post(self,):
        """ 
        
        Retorna la consulta de saldo de un cliente \
        de la aplicacion PIC "PFL"\
        @param = json
        atributos: 
            [codigo de area]
            [numero de telefono]
        """
        producto =api.payload
        query = producto['cod']+producto['tlf']
        result = {}
        for p in saldoSoap:
            if (p['producto'] == query):
                result = p
                break
        temp = result['data']['Fvencimiento']
        result['data']['Fvencimiento']= self.__cleanDate__(temp)
        temp = result['data']['Fcorte'] 
        result['data']['Fcorte'] = self.__cleanDate__(temp)
        return result, 200
    
    def __cleanDate__(self, AAAAMMDD):
        AAAAMMDD = str(AAAAMMDD)
        if (len(AAAAMMDD) == 8):
            return f'{AAAAMMDD[0:4]}-{AAAAMMDD[4:6]}-{AAAAMMDD[6:8]}'

        return AAAAMMDD
    
@ns_consulta.route('/abonado')
class Abonado(Resource):

    def post(self, ):
        pass


@ns_consulta.route('/planes')
class Planes(Resource):
    def post(self, ):
        pass







