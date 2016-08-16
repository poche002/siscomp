from pecan import expose, request, response
from pecan.rest import RestController
from pecan.secure import secure
from co_server.model import model
import json
import clientSystemController


@secure('check_permissions')
class UserController(RestController):
    _custom_actions = {
        'get_one_by_email': ['GET'],
	'get_one_by_phone': ['GET'],
	'add_cs_to_user': ['PUT']
    }

    @expose('json')
    def get_one_by_email(self, email_param):
        user = model.get_user(email=email_param)
        if email_param:
            user_dict = {'user_id':user.user_id, 'password':user.password,'fullname':user.fullname, 'email':user.email,'phone':user.phone, 'admin':user.admin}
	    return user_dict 
	else:
	    response.status=400

    @expose('json')
    def get_one_by_phone(self, phone_param):
	user = model.get_user(phone=phone_param)
	if phone_param:
            user_dict = {'user_id':user.user_id, 'password':user.password,'fullname':user.fullname, 'email':user.email,'phone':user.phone, 'admin':user.admin}
	    return user_dict
	else:
	    response.status=400

    @expose('json')
    def add_cs_to_user(self, email_param, client_system_id):
	user= model.get_user(email=email_param)
	client= model.get_client_system(client_system_id)
	if email_param and client_system_id:
	    model.add_client_system_to_user(user.email, client.client_system_id)
	    response.status=201
	else:
	    response.status=400

    
    @expose('json')
    def get_one(self,user_id):
#        badges = []
	user = model.get_user(user_id)
        if  user_id:
#            for u in user.users:
#                badges.append({'badge_id':u.badge.badge_id,'amount_necessary':u.badge.amount_necessary,'cant_act':u.cant_act ,'description':u.badge.description, 'title':u.badge.title, 'image':u.badge.image, 'data1':u.badge.data1})
            user_dict = {'user_id':user.user_id, 'password':user.password,'fullname':user.fullname, 'email':user.email,'phone':user.phone, 'admin':user.admin, 'sistemas':user.client_systems}
            return user_dict
	else:
            response.status = 404

    @expose('json')
    def get_all(self):
        users = []
        for user in model.get_all_users():
            users.append(self.get_one(user.user_id))
        return users

    @expose('json')
    def post(self):

	try:
            body = request.json
            if model.get_user(body['user_id']):
                response.status = 409		#confict, user_id already in use
            else:
                if (body['user_id'] and body['password'] and body['fullname'] and body['email']):
                    model.add_user(body['user_id'], body['password'], body['fullname'], body['email'], body['phone'], body['admin'])
                    response.status = 201
                else:
                    response.status = 400
        except ValueError:
            response.status = 400

    @expose()
    def delete(self, user_id='none'):
        if model.del_user(user_id):
            response.status = 200
        else:
            response.status = 404

    @expose('json')
    def put(self, user_id_old):
        try:
            body = request.json
            if model.edit_user(user_id_old, body['user_id'], body['fullname'], body['password'], body['email']):
                response.status = 200
            else:
                response.status = 404
        except ValueError:
            response.status = 400
