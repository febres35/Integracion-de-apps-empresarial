from src.server.instance import server
from src.controllers.consulta import * 

server.api.add_namespace(ns_consulta)
server.run()



