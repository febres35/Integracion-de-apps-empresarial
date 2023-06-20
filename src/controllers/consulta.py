from flask import Flask
from flask_restx import Resource, Namespace
from src.server.instance import server

from zeep import Client
from zeep import xsd
from zeep.cache import SqliteCache
from zeep.transports import Transport

app = server.app
api = server.api

from src.models.telefono import in_telefono
from src.models.saldo import  out_Saldo
from src.models.abonado import out_abonado
from src.models.plan import out_planes

ns_consulta = Namespace('Consultas', description='Consultas -> saldo | abonado | planes', path='/api/1.0/consulta')


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
        producto = api.payload
        cod = producto['cod']
        tlf = producto['tlf']
        result = self.consultaSaldo(cod, tlf)
        print(result)

        return  200
    
    def __cleanDate__(self, AAAAMMDD):
        AAAAMMDD = str(AAAAMMDD)
        if (len(AAAAMMDD) == 8):
            return f'{AAAAMMDD[0:4]}-{AAAAMMDD[4:6]}-{AAAAMMDD[6:8]}'

        return AAAAMMDD
    
    def consultaSaldo(codigoArea, telefono):

        wsdl = "http://10.1.189.230:8801/mule/services/PG503obtenerSaldoCuenta?wsdl" #endpoint soap
        transport = Transport()
        transport.session.verify=False
        transport.timeout=1500
        cliente = Client(wsdl=wsdl, transport=transport) #Instancia del objeto de cliente
        #Request=  cliente.get_type('ns1:F2V5AscObtenerSaldoCuentaRQ') #Extraccion de tipo de dato que lleva como parametro el metodo F2V5AscObtenerSaldoCuenta
        #Request = Request(aplicacion='PFL', codigoArea=codigoArea, telefono=telefono) #pase de parametro con los que se va a realizar la consulta
        print(cliente)
        query = {
            'aplicacion': 'PFL',
            'codigoArea': codigoArea,
            'telefono': telefono
        }
        result = cliente.service.f2V5_Asc_obtenerSaldoCuenta(query)

        respuesta = {
            'producto': query['codigoArea'] + result.telefono,
            'data': {
                'Fvencimiento': result.fechaVencimiento,
                'saldoA': result.saldoActual,
                'saldoV': result.saldoVencido,
                'Fcorte': result.fechaCorte,
            }
        }
        #return respuesta, 200

    


@ns_consulta.route('/abonado')
class Abonado(Resource):

    @ns_consulta.expect(in_telefono, valitade=True)
    @ns_consulta.marshal_with(out_abonado)
    def post(self, ):
        pass


@ns_consulta.route('/planes')
class Planes(Resource):

    @ns_consulta.expect(in_telefono, valitade=True)
    @ns_consulta.marshal_with(out_planes)
    def post(self, ):
        pass







