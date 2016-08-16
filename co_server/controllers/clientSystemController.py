from pecan.rest import RestController
from pecan import expose, request, response
from co_server.model import model
import json

class ClientSystemController(RestController):

    @expose('json')
    def get_one(self, client_id):
#        users = {}
#        badge = model.get_badge(badge_id)
	client = model.get_client_system(client_id)
        if client:
#            for b in client.clients:                              #lista de objetos user-badge
#                if b.cant_act >= badge.amount_necessary:
#                    users[b.user.user_id] = b.user.fullname
            client_dict = {'client_system_id':client.client_system_id,'detail':client.detail,'last_keepalive':client.last_keepalive,'state':client.state}
            #badge_dict = {badge.badge_id:{'amount_necessary':badge.amount_necessary,'description':badge.description, 'title':badge.title, 'image':badge.image, 'data1':badge.data1,'users':users}}
            return client_dict
        else:
            response.status = 404

    @expose('json')
    def get_all(self):
#        badges = []
	clients = []
#        for badge in model.get_all_badges():
#            badges.append(self.get_one(badge.badge_id))
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
	            model.add_client_system(body['client_system_id'], body['detail'])
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
    def put(self, client_id_old):
        try:
            body = request.json
            try:
                if model.edit_client_system(client_id_old, body['client_system_id'], body['detail'], body['last_keepalive'], body['state']):
                    response.status = 200
                else:
                    response.status = 404
            except KeyError:
                response.status = 400
        except ValueError:
            response.status = 400


