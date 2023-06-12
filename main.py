from src.server.instance import server
from src.controllers.consulta import * 
from src.controllers.averia import *

server.api.add_namespace(ns_consulta)
server.api.add_namespace(ns_averia)

server.run()



