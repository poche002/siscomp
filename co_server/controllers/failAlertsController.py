from pecan import expose, request, response
from pecan.rest import RestController
from co_server.model import model

import json
import clientSystemController


class FailAlertsController(RestController):
    _custom_actions = {
    'add_fail_system_alert': ['POST']
    }
    
    @expose('json')
    def add_fail_system_alert(self,client_system_id):
        
        client = model.get_client_system(client_system_id)
        if client:
            model.add_fail_system_alert(client_system_id)
            response.status=200
        else:
            response.status=400
