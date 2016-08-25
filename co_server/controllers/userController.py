from pecan import expose, request, response
from pecan.rest import RestController
from pecan.secure import secure
from co_server.model import model
import json
import clientSystemController

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


@secure('check_permissions')
class UserController(RestController):
    _custom_actions = {
    'get_one_by_email': ['GET'],
	'get_one_by_phone': ['GET'],
	'add_cs_to_user': ['PUT'],
	'get_emails':['GET']
    }

    # metodo para enviar emails
    @expose()
    def send_email(self, emails, subject, message):
		#mail de origen
                fromaddr = "mail"
                recipients = emails
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = ", ".join(recipients)
                msg['Subject'] = subject

                body = message
                msg.attach(MIMEText(body,'plain'))

                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
		#aca va la contraseña del mail
                server.login(fromaddr,"contraseña")
                text = msg.as_string()
                server.sendmail(fromaddr, recipients, text)
                server.quit()
    # devuelve un el email de un usuario perteneciente a un sistema cliente
    # el parametro admin_value es para filtrar por los distintos tipos de 
    # usuario: 0  administrador
    #          1  usuario comun
    #          2  contacto de emergencia
    #         >=3 ignora el tipo
    @expose()
    def get_email(self, user_id, client_system_id, admin_value):
        user = model.get_user(user_id)
        for u in user.client_systems:
            client = u.client_system_id
            if client == client_system_id:
                email = user.email
                if int(admin_value) >= 3:
                    return email
                elif user.admin == int(admin_value):
                    return email           
            
    # devuelve todos los mails de un sistema cliente        
    @expose('json')
    def get_emails(self, client_system_id, admin_value):
        users = []
        for user in model.get_all_users():
            aux = self.get_email(user.user_id,client_system_id, admin_value)
            if aux:
                users.append(aux)
        return users

    # vincula un usuario existente a un sistema cliente existente
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
	user = model.get_user(user_id)
        if  user_id:
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
