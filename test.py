from zeep import Client
from zeep import xsd
from zeep.cache import SqliteCache
from zeep.transports import Transport

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
    return result

print(consultaSaldo('212', '5516273'))
