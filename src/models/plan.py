from flask_restx import fields
from src.server.instance import server


respuesta = server.api.model('Respuesta', {
    'codRespuesta' : fields.String(description='Codigo de error'),
    'mensaje': fields.String(description='Decripcion del codigo'),
    })

velocidad = server.api.model('Velocidad', {
    'MAXIMA_VELOCIDAD': fields.String(description='Kb | Velocidad maxima de navecacion'),
    'VELOCIDAD_ACTUAL': fields.String(description='Kb | Velocidad del plan actual'),
    })

plan = server.api.model('Plan', {
    'ID_PLAN': fields.String(description='Identificador del plan'),
    'NOMBRE_PLAN': fields.String(description='Nombre del plan'),
    'VELOCIDAD': fields.String(description='Velocidad del plan'),
    })


out_planes = server.api.model('Planes', {
    'respuestaDelSistema': fields.Nested(respuesta),
    'plan': fields.Raw(list(plan)),
    'velocidad': fields.Nested(velocidad),
    })

