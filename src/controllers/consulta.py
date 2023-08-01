from flask import Flask
from flask_restx import Resource, Namespace, marshal
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

@ns_consulta.route('/saldo')
@ns_consulta.doc(param={'cod': 'codigo de Area', 'tlf':'numero de telefono(producto)'})
class Saldo(Resource):


    @ns_consulta.expect(in_telefono, valitade=True)    
    @ns_consulta.marshal_with(out_Saldo)
    def post(self,):
        producto = api.payload
        cod = producto['cod']
        tlf = producto['tlf']
        result = self.consultaSaldo(cod, tlf)
        print(result)
        
        return  result, 200

    def consultaSaldo(self, codigoArea, telefono):

        wsdl = "http://10.1.189.230:8801/mule/services/PG503obtenerSaldoCuenta?wsdl" #endpoint soap
        transport = Transport()
        transport.session.verify=False
        transport.timeout=1500
        cliente = Client(wsdl=wsdl, transport=transport)
        query = {
            'aplicacion': 'PFL',
            'codigoArea': codigoArea,
            'telefono': telefono
        }
        result = cliente.service.f2V5_Asc_obtenerSaldoCuenta(query)
        respuesta = {"producto": str(query['codigoArea'] + result.cuentas.telefono),
                     "data": {
                         "Fvencimiento": self.__cleanDate__(result.cuentas.fechaVencimiento),
                         "saldoA": str(result.cuentas.saldoActual),
                         "saldoV": str(result.cuentas.saldoVencido),
                         "Fcorte": self.__cleanDate__(result.cuentas.fechaCorte),
                         "UltimoPago": str(result.pagos.MONTO_ULTI_PAG),
                         "UltimaFacturacion": self.__cleanDate__(result.cuentas.fechaUltimaFacturacion),
                         }
        }
        print(result)
        return respuesta
    

    
    def __cleanDate__(self, AAAAMMDD):
        AAAAMMDD = str(AAAAMMDD)
        if (len(AAAAMMDD) == 8):
            return f'{AAAAMMDD[0:4]}-{AAAAMMDD[4:6]}-{AAAAMMDD[6:8]}'

        return AAAAMMDD
    


    


@ns_consulta.route('/abonado')
class Abonado(Resource):

    @ns_consulta.expect(in_telefono, valitade=True)
    @ns_consulta.marshal_with(out_abonado)
    def post(self, ):
        producto = api.payload
        numeroDeServicio = producto['cod']+producto['tlf']
        result = self.abonado(numeroDeServicio)
        return result, 200


    def abonado(self, numeroDeServicio):
        wsdl = 'http://161.196.61.40:8800/mule/services/AP738ConsultaAbonadoActivoNumeroTelefono?wsdl'
        transport = Transport()
        transport.session.verify=False
        transport.timeout=1500
        cliente = Client(wsdl=wsdl, transport=transport)
        response = cliente.service.consultaAbonadoActivoNumeroTelefono(in0={
            'NU_SERVICIO':numeroDeServicio
        })
        result = {
        "CUENTA_CLIENTE": response.CUENTA_CLIENTE,
        "cliente": {
            "CEDULA_RIF": response.CEDULA_RIF,
            "NOMBRE": response.NOMBRE_CLIENTE,
            "DIRECCION_COBRO": response.DIRECCION_COBRO,
            "ZONA_POSTAL": response.ZONA_POSTAL
        },
        "producto": {
            "IDENTIFICADOR_LLAMADAS": response.IDENTIFICADOR_LLAMADAS,
            "UNIDAD_NEGOCIOS": response.UNIDAD_NEGOCIOS,
            "SERVICIO_ABA": response.SERVICIO_ABA,
            "MODALIDAD_LINEA": response.MODALIDAD_LINEA,
            "PLAN_TARIFARIO": response.PLAN_TARIFARIO,
            "TARIFA": response.TARIFA,
        },
        "informacion_tecnica": {
            "CODERROR": response.CODERROR,
            "DESCERROR": response.DESCERROR,
            "OPERADOR_LDI": response.OPERADOR_LDI,
            "OPERADOR_LDN": response.OPERADOR_LDN,
            "OPERADOR_LOCAL": response.OPERADOR_LOCAL,
            "CENTRAL": response.CENTRAL,
            "RUTA_COBRO": response.RUTA_COBRO,
            "BLOQUEO_SELECTIVO": response.BLOQUEO_SELECTIVO,
            "BLOQUEO": response.BLOQUEO,
            "TIPO_LINEA": response.TIPO_LINEA,
            "INTENER_EQUIPADO": response.INTENER_EQUIPADO,
            "CONDICION_NUMERO_PRIVADO": response.CONDICION_NUMERO_PRIVADO,
        }
        }
        print(response)
        return result
    
@ns_consulta.route('/planes')
class Planes(Resource):

    @ns_consulta.expect(in_telefono, valitade=True)
    @ns_consulta.marshal_with(out_planes)
    def post(self, ):
        producto = api.payload
        cod = producto['cod']
        tlf = producto['tlf']
        result = self.planes(cod, tlf)
        return result, 200
        

    def planes(self, cod, ext):
        wsdl = 'http://10.1.189.230:8801/mule/services/AP724ConsultaPlanesABAdisponibles?wsdl'
        transport = Transport(cache=SqliteCache())
        transport.load_timeout = 1500
        transport.session.verify = False
        client = Client(wsdl, transport=transport)
        request = {
            'cod_area': cod,
            'telefono': ext,
            }
        response = client.service.consultarPlanes(arg0=request)
        print(response)
        p = response.PLAN.Planes
        planes = []

        for plan in p:
            if(plan['CODIGOS_PLANES_DISPONIBLES'] != 'None'):
                velocidad = str(plan['CODIGOS_PLANES_DISPONIBLES']).split("_")      
                planes.append({
                "ID_PLAN": plan['CODIGOS_PLANES_DISPONIBLES'],
                "NOMBRE_PLAN": plan['DESCRIPCION_DE_LOS_PLANES'],
                "VELOCIDAD": ''.join(velocidad[2:3]),#volver string la lista.
                }),

            
            
        print(planes)
        result = {
            "respuestaDelSistema": {
                "codRespuesta": response.CODIGO_ERROR,
                "mensaje": response.DESCRIPCION_ERROR
            },
            "plan": {
                "planes": planes[1:]
            },
            "velocidad": {
                "MAXIMA_VELOCIDAD": response.MAXIMA_VELOCIDAD,
                "VELOCIDAD_ACTUAL": response.VELOCIDAD_ACTUAL
            }
        }
        #5513457
        return result







