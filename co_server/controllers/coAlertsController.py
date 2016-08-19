from pecan import expose, request, response
from pecan.rest import RestController
from co_server.model import model

import json
import clientSystemController


class CoAlertsController(RestController):
    _custom_actions = {
    'add_co_alert': ['POST']
    }
    
    @expose('json')
    def add_co_alert(self,client_system_id, measure_value):
        
        client = model.get_client_system(client_system_id)
        if client:
            model.add_co_alert(client_system_id, measure_value)
            response.status=200
        else:
            response.status=400
