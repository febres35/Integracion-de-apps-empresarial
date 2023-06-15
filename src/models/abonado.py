from flask_restx import fields
from src.server.instance import server


persona = server.api.model('Persona', {
    'CEDULA_RIF': fields.String( description='DI de la persona' ),
    'NOMBRE': fields.String(  description='Nombre de la persona' ),
    'APELLIDO': fields.String(  description='Apellido de la persona' ),
    'DIRECCION_COBRO' : fields.String(description='Direccion de cobro'),
    'ZONA_POSTAL': fields.String( description='Codigo Postal'),
    
})

infoTecnica = server.api.model('InformacionTecnica', {
    'CODERROR' : fields.String( description='codigo de error de la peticion'),
    'DESCERROR': fields.String( description='Descripcion de respuesta'),
    'OPERADOR_LDI' : fields.String( description='codigo de Operador_LDI'),
    'OPERADOR_LDN' : fields.String( description='codigo de Operador_LDN'),
    'OPERADOR_LOCAL': fields.String( description='codigo de Operador_local'),
    'CENTRAL': fields.String( description='codigo de central'),
    'RUTA_COBRO' : fields.String( description='codigo de ruta de cobro' ),
    'BLOQUEO_SELECTIVO' : fields.String( description='Indicador' ),
    'BLOQUEO': fields.String( description='indicador'),
    'TIPO_LINEA': fields.String( description='idicador'),
    'INTENER_EQUIPADO': fields.String( description='indicador'),
    'CONDICION_NUMERO_PRIVADO': fields.String( description='Indica si el numero de telefono es privado o publico'),
})

productos = server.api.model('Productos', {
    'IDENTIFICADOR_LLAMADAS': fields.String( description='indicador'),
    'UNIDAD_NEGOCIOS': fields.String(description='Tipo de negocio | R: residencial, C: comercial'),
    'SERVICIO_ABA': fields.String( description='Descripcion de servicio de internet'),
    'MODALIDAD_LINEA': fields.String( description='Modalidad de Linea'),
    'PLAN_TARIFARIO': fields.String( description='Nombre del plan de telefonia'),
    'TARIFA': fields.String(description='indicador'),                                   
})


out_abonado = server.api.model( 'Abonado', {
'CUENTA_CLIENTE': fields.String( description='numero de Cuenta cliente'),
'cliente': fields.Nested( persona),
'producto': fields.Nested(productos),
'informacion_tecnica': fields.Nested(infoTecnica),
})