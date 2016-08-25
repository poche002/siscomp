from pecan.rest import RestController
from pecan import expose, request, response
from co_server.model import model
import json
import coAlertsController
import userController

class ClientSystemController(RestController):
    _custom_actions = {
    'edit_keepalive': ['PUT'],
    'edit_detail': ['PUT'],
    }


    @expose('json')
    def get_one(self, client_id):
	client = model.get_client_system(client_id)
        if client:
            client_dict = {'client_system_id':client.client_system_id,'detail':client.detail,'last_keepalive':client.last_keepalive,'state':client.state, 'alerts':client.co_alerts, 'fali alerts':client.fail_sensor_alerts, 'users':client.users}
            return client_dict
        else:
            response.status = 404

    @expose('json')
    def get_all(self):
	clients = []
	for client in model.get_all_client_systems():
	    clients.append(self.get_one(client.client_system_id))   
        return clients

    @expose('json')
    def post(self):
        try:
            body = request.json
            if model.get_client_system(body['client_system_id']):
                response.status = 409
            else:
                try:
	            model.add_client_system(body['client_system_id'])
                except KeyError:
                    response.status = 400
        except KeyError:
            response.status = 400

    @expose()
    def delete(self, client_id='none'):
        if model.del_client_system(client_id):
            response.status = 200
	    return client_id
        else:
            response.status = 404
	    return client_id

    @expose('json')
    def edit_detail(self, client_id_old, detail):
         client= model.get_client_system(client_id_old)
         if client.client_system_id:
             if model.edit_client_system(client_id_old, client_id_old, detail):
                 response.status = 200
             else:
                 response.status = 404
         else:
             response.status = 404

    @expose('json')
    def edit_keepalive(self, client_system_id):
            client = model.get_client_system(client_system_id)
            users = userController.UserController()

            if client.client_system_id:
                model.keepalive_client_system(client_system_id)
                return "keepalive sent"
                
            else:
                response.status=400
    
